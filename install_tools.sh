#!/bin/bash
# =============================================================================
# Bug Bounty Tool Installer
# Installs all required tools via Homebrew and Go
# Usage: ./install_tools.sh [--with-cicd-scanner] [--with-credential-attack] [--with-web3] [--with-pro]
# =============================================================================

set -euo pipefail

INSTALL_CICD_SCANNER=false
INSTALL_CREDENTIAL_ATTACK=false
INSTALL_WEB3=false
INSTALL_PRO=false
for arg in "$@"; do
    case "$arg" in
        --help|-h)
            sed -n '2,6p' "$0"
            echo ""
            echo "Optional: --with-cicd-scanner --with-credential-attack --with-web3 --with-pro"
            exit 0
            ;;
        --with-cicd-scanner) INSTALL_CICD_SCANNER=true ;;
        --with-credential-attack) INSTALL_CREDENTIAL_ATTACK=true ;;
        --with-web3) INSTALL_WEB3=true ;;
        --with-pro) INSTALL_PRO=true ;;
    esac
done

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_ok()   { echo -e "${GREEN}[+]${NC} $1"; }
log_err()  { echo -e "${RED}[-]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[!]${NC} $1"; }

echo "============================================="
echo "  Bug Bounty Tool Installer"
echo "============================================="

# Check for Homebrew
if ! command -v brew &>/dev/null; then
    log_warn "Homebrew not found. Installing..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Check for Go (needed for some tools)
if ! command -v go &>/dev/null; then
    log_warn "Go not found. Installing via Homebrew..."
    brew install go
fi

# Ensure Go bin is in PATH early so go install binaries are visible
GOPATH="$(go env GOPATH 2>/dev/null || true)"
GOPATH="${GOPATH:-$HOME/go}"
if [[ ":$PATH:" != *":$GOPATH/bin:"* ]]; then
    export PATH="$PATH:$GOPATH/bin"
fi

# Tools to install via Homebrew
BREW_TOOLS=(
    "nmap"
    "subfinder"
    "httpx"
    "nuclei"
    "ffuf"
    "amass"
)

echo ""
echo "[*] Installing tools via Homebrew..."
for tool in "${BREW_TOOLS[@]}"; do
    if command -v "$tool" &>/dev/null; then
        log_ok "$tool already installed ($(command -v "$tool"))"
    else
        echo "    Installing $tool..."
        if brew install "$tool" 2>/dev/null; then
            log_ok "$tool installed successfully"
        else
            log_err "$tool failed to install via brew, trying alternative..."
        fi
    fi
done

# Tools to install via Go
echo ""
echo "[*] Installing tools via Go..."

# Pinned to specific tagged releases (not @latest) — verified current as of
# 2026-08-23 via each project's GitHub releases / the Go module proxy.
GO_TOOLS=(
    "github.com/lc/gau/v2/cmd/gau@v2.2.4"
    # dalfox v3.x is a Rust rewrite (Cargo.toml, no go.mod) and is not
    # go-installable — v2.13.0 is the latest tag still on the Go module line.
    "github.com/hahwul/dalfox/v2@v2.13.0"
    # subjack's own v2.x/v3.0.0 tags are invalid Go modules (go.mod module
    # path lacks the required /v2, /v3 suffix for those major versions), so
    # `go install .../subjack@v3.0.0` fails outright. The Go module proxy
    # resolves @latest to a pseudo-version pointing at that same v3.0.0
    # commit — pin to that resolved pseudo-version so the install is still
    # reproducible instead of silently floating on upstream's tagging bug.
    "github.com/haccer/subjack@v0.0.0-20260316055456-b53899ce6230"
)

GO_TOOL_NAMES=(
    "gau"
    "dalfox"
    "subjack"
)

for i in "${!GO_TOOLS[@]}"; do
    tool_name="${GO_TOOL_NAMES[$i]}"
    tool_path="${GO_TOOLS[$i]}"
    if command -v "$tool_name" &>/dev/null; then
        log_ok "$tool_name already installed"
    else
        echo "    Installing $tool_name..."
        if go install "$tool_path" 2>/dev/null; then
            log_ok "$tool_name installed successfully"
        else
            log_err "$tool_name failed to install"
        fi
    fi
done

# sisakulint — GitHub Actions SAST (binary download)
echo ""
echo "[*] Installing sisakulint..."
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)
case "$ARCH" in
    x86_64)  ARCH="amd64" ;;
    aarch64) ARCH="arm64" ;;
    armv6l)  ARCH="armv6" ;;
esac
SISAKULINT_LATEST=$(curl -sI https://github.com/sisaku-security/sisakulint/releases/latest | grep -i '^location:' | grep -Eo 'v[0-9]+\.[0-9]+\.[0-9]+' | head -1 || true)
SISAKULINT_LATEST="${SISAKULINT_LATEST#v}"
SISAKULINT_CURRENT=""
if command -v sisakulint &>/dev/null; then
    SISAKULINT_CURRENT=$(sisakulint -version 2>&1 | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || true)
fi
if [ -n "$SISAKULINT_CURRENT" ] && [ "$SISAKULINT_CURRENT" = "$SISAKULINT_LATEST" ]; then
    log_ok "sisakulint v${SISAKULINT_CURRENT} already up to date ($(command -v sisakulint))"
elif [ -n "$SISAKULINT_LATEST" ]; then
    [ -n "$SISAKULINT_CURRENT" ] && echo "    Upgrading sisakulint v${SISAKULINT_CURRENT} → v${SISAKULINT_LATEST}..."
    SISAKULINT_ASSET="sisakulint_${SISAKULINT_LATEST}_${OS}_${ARCH}.tar.gz"
    SISAKULINT_URL="https://github.com/sisaku-security/sisakulint/releases/download/v${SISAKULINT_LATEST}/${SISAKULINT_ASSET}"
    SISAKULINT_CHECKSUMS_URL="https://github.com/sisaku-security/sisakulint/releases/download/v${SISAKULINT_LATEST}/sisakulint_${SISAKULINT_LATEST}_checksums.txt"
    SISAKULINT_TARBALL="/tmp/${SISAKULINT_ASSET}"
    SISAKULINT_CHECKSUMS="/tmp/sisakulint_${SISAKULINT_LATEST}_checksums.txt"
    echo "    Downloading sisakulint v${SISAKULINT_LATEST} (${OS}/${ARCH})..."
    # -f: fail (no output) on HTTP errors instead of saving the error body as if
    # it were the real binary/checksums file.
    if curl -fsSL "$SISAKULINT_URL" -o "$SISAKULINT_TARBALL" && \
       curl -fsSL "$SISAKULINT_CHECKSUMS_URL" -o "$SISAKULINT_CHECKSUMS"; then
        # sha256sum -c expects the checksummed filename relative to cwd, and the
        # published checksums.txt lists filenames for every OS/ARCH — filter to
        # just our asset's line before verifying.
        if (cd /tmp && grep -F " ${SISAKULINT_ASSET}" "$(basename "$SISAKULINT_CHECKSUMS")" | sha256sum -c - --strict) &>/dev/null; then
            log_ok "sisakulint v${SISAKULINT_LATEST} checksum verified"
            if tar -xzf "$SISAKULINT_TARBALL" -C /tmp/ && \
               { mv /tmp/sisakulint /usr/local/bin/sisakulint 2>/dev/null || \
                 sudo mv /tmp/sisakulint /usr/local/bin/sisakulint; }; then
                rm -f "$SISAKULINT_TARBALL" "$SISAKULINT_CHECKSUMS"
                log_ok "sisakulint v${SISAKULINT_LATEST} installed"
            else
                rm -f "$SISAKULINT_TARBALL" "$SISAKULINT_CHECKSUMS" /tmp/sisakulint
                log_err "sisakulint failed to install. Download manually from:"
                log_err "  https://github.com/sisaku-security/sisakulint/releases"
            fi
        else
            rm -f "$SISAKULINT_TARBALL" "$SISAKULINT_CHECKSUMS"
            log_err "sisakulint checksum verification FAILED — refusing to install a tarball"
            log_err "that doesn't match the published checksums.txt. Download manually from:"
            log_err "  https://github.com/sisaku-security/sisakulint/releases"
        fi
    else
        rm -f "$SISAKULINT_TARBALL" "$SISAKULINT_CHECKSUMS"
        log_err "sisakulint failed to download. Download manually from:"
        log_err "  https://github.com/sisaku-security/sisakulint/releases"
    fi
else
    if command -v sisakulint &>/dev/null; then
        log_warn "Could not fetch latest version — keeping sisakulint v${SISAKULINT_CURRENT}"
    else
        log_err "Could not fetch latest sisakulint version. Download manually from:"
        log_err "  https://github.com/sisaku-security/sisakulint/releases"
    fi
fi

# cicd_scanner — sisakulint wrapper script (optional: --with-cicd-scanner)
if [ "$INSTALL_CICD_SCANNER" = true ]; then
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    CICD_SCANNER_SRC="$SCRIPT_DIR/tools/cicd_scanner.sh"
    if [ -f "$CICD_SCANNER_SRC" ]; then
        INSTALL_DIR="/usr/local/bin"
        if cp "$CICD_SCANNER_SRC" "$INSTALL_DIR/cicd_scanner" 2>/dev/null || \
           sudo cp "$CICD_SCANNER_SRC" "$INSTALL_DIR/cicd_scanner"; then
            chmod +x "$INSTALL_DIR/cicd_scanner" 2>/dev/null || sudo chmod +x "$INSTALL_DIR/cicd_scanner"
            log_ok "cicd_scanner installed to $INSTALL_DIR/cicd_scanner"
        else
            mkdir -p "$HOME/bin"
            cp "$CICD_SCANNER_SRC" "$HOME/bin/cicd_scanner"
            chmod +x "$HOME/bin/cicd_scanner"
            log_ok "cicd_scanner installed to ~/bin/cicd_scanner"
            if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
                log_warn "Add ~/bin to your PATH: export PATH=\$HOME/bin:\$PATH"
            fi
        fi
    fi
else
    log_warn "cicd_scanner skipped (use --with-cicd-scanner to install)"
fi

# Credential-attack tools (optional: --with-credential-attack)
# Default off — adds ~500MB and pulls ~8 Python/Go deps.
if [ "$INSTALL_CREDENTIAL_ATTACK" = true ]; then
    echo ""
    echo "[*] Installing credential-attack tools..."

    log_warn "First run may take 10–20 min: brew auto-update + downloads ~500MB."
    log_warn "Output below comes from brew/pipx/go/curl directly — slow lines are normal."

    # --- Homebrew (theHarvester moved here: PyPI package has no CLI entry-point) ---
    BREW_CRED_TOOLS=("hashcat" "theharvester")
    for tool in "${BREW_CRED_TOOLS[@]}"; do
        # theHarvester's binary is capitalised, so its formula name never matches
        # `command -v`. Check that alias for theharvester ONLY — the previous
        # unconditional `|| command -v "theHarvester"` applied on every iteration,
        # so once theHarvester was present the loop reported "hashcat already
        # installed" and skipped the install. A false success, easy to miss.
        if [ "$tool" = "theharvester" ]; then
            _present() { command -v theharvester &>/dev/null || command -v theHarvester &>/dev/null; }
        else
            _present() { command -v "$tool" &>/dev/null; }
        fi
        if _present; then
            log_ok "$tool already installed"
        else
            echo "    [*] Installing $tool via brew..."
            if brew install "$tool"; then
                log_ok "$tool installed"
            else
                log_err "$tool failed to install via brew"
            fi
        fi
    done

    # --- uv/pipx (isolated Python venvs; prefer uv when present — faster, no separate install step) ---
    if command -v uv &>/dev/null; then
        log_ok "uv found ($(command -v uv)) — using it for isolated Python tool installs"
    elif ! command -v pipx &>/dev/null; then
        echo "    [*] Installing pipx via brew..."
        brew install pipx && pipx ensurepath
        log_warn "pipx installed — restart shell or 'source ~/.zshrc' for PATH"
    fi

    py_tool_install() {
        if command -v uv &>/dev/null; then
            uv tool install "$@"
        else
            pipx install "$@"
        fi
    }
    py_tool_upgrade() {
        if command -v uv &>/dev/null; then
            uv tool upgrade "$@"
        else
            pipx upgrade "$@"
        fi
    }

    PIPX_CRED_TOOLS=("cewler" "cupp" "trevorspray")
    for tool in "${PIPX_CRED_TOOLS[@]}"; do
        if command -v "$tool" &>/dev/null; then
            log_ok "$tool already installed"
        else
            echo "    [*] Installing $tool..."
            if py_tool_install "$tool"; then
                log_ok "$tool installed"
            else
                log_warn "$tool: install failed — try 'uv tool install $tool' or 'pipx install $tool' manually"
            fi
        fi
    done

    # --- Go (kerbrute — not in brew) ---
    if command -v kerbrute &>/dev/null; then
        log_ok "kerbrute already installed"
    else
        echo "    [*] Installing kerbrute via go..."
        # Pinned to v1.0.3 (latest tagged release as of 2026-08-23) instead
        # of @latest — see GO_TOOLS above for why we pin.
        if go install github.com/ropnop/kerbrute@v1.0.3; then
            log_ok "kerbrute installed"
        else
            log_err "kerbrute failed to install"
        fi
    fi

    # --- Git clone (tools without brew/pip packages) ---
    EXT_DIR="${HOME}/.local/share/bug-bounty/credential-attack"
    mkdir -p "$EXT_DIR"
    GIT_TOOLS=(
        "https://github.com/LandGrey/pydictor.git"
        "https://github.com/urbanadventurer/username-anarchy.git"
        "https://github.com/knavesec/CredMaster.git"
    )
    for repo in "${GIT_TOOLS[@]}"; do
        name=$(basename "$repo" .git)
        if [ -d "$EXT_DIR/$name" ]; then
            echo "    [*] Updating $name (git pull)..."
            if (cd "$EXT_DIR/$name" && git pull --quiet); then
                log_ok "$name updated at $EXT_DIR/$name"
            else
                log_warn "$name: git pull failed"
            fi
        else
            echo "    [*] Cloning $name..."
            if git clone --quiet "$repo" "$EXT_DIR/$name"; then
                log_ok "$name cloned to $EXT_DIR/$name"
            else
                log_err "$name: git clone failed"
            fi
        fi
    done

    # --- CrossLinked via uv/pipx (avoids PEP 668 pip3 --user breakage on macOS + Python 3.13) ---
    echo "    [*] Installing CrossLinked..."
    if py_tool_install crosslinked --quiet 2>/dev/null; then
        log_ok "CrossLinked installed"
    elif py_tool_upgrade crosslinked --quiet 2>/dev/null; then
        log_ok "CrossLinked upgraded"
    else
        log_warn "CrossLinked install failed — run 'uv tool install crosslinked' or 'pipx install crosslinked' manually"
    fi

    # --- SecLists hint (not auto-installed; ~750MB) ---
    if [ ! -d "/usr/share/seclists" ] && [ ! -d "$HOME/SecLists" ]; then
        log_warn "SecLists not found. Clone with:"
        log_warn "  git clone https://github.com/danielmiessler/SecLists.git ~/SecLists"
    fi

    # --- Hashcat rules ---
    RULES_DIR="$EXT_DIR/rules"
    mkdir -p "$RULES_DIR"
    if [ -f "$RULES_DIR/OneRuleToRuleThemAll.rule" ]; then
        log_ok "OneRuleToRuleThemAll.rule already present"
    else
        echo "    [*] Downloading OneRuleToRuleThemAll.rule..."
        if curl -fsSL https://raw.githubusercontent.com/NotSoSecure/password_cracking_rules/master/OneRuleToRuleThemAll.rule \
            -o "$RULES_DIR/OneRuleToRuleThemAll.rule"; then
            log_ok "OneRuleToRuleThemAll.rule downloaded to $RULES_DIR"
        else
            log_warn "OneRuleToRuleThemAll.rule download failed"
        fi
    fi
else
    log_warn "credential-attack tools skipped (use --with-credential-attack to install)"
fi

# Web3 / smart-contract tools (optional: --with-web3)
if [ "$INSTALL_WEB3" = true ]; then
    echo ""
    echo "[*] Installing Web3 / smart-contract tools..."

    # Python analyzers (all published by their upstream projects)
    WEB3_PIPX=(
        slither-analyzer
        solc-select
        crytic-compile
        halmos
        eth-wake
    )
    for pkg in "${WEB3_PIPX[@]}"; do
        if command -v pipx &>/dev/null; then
            if pipx install --force "$pkg" 2>/dev/null; then
                log_ok "$pkg installed"
            else
                log_warn "$pkg failed (run: pipx install $pkg)"
            fi
        else
            log_warn "pipx not found — install $pkg manually"
        fi
    done

    # Mythril needs an older Python than 3.13+ (cffi build failure on 3.14).
    if command -v pipx &>/dev/null; then
        MYTH_PY=()
        if command -v python3.12 &>/dev/null; then
            MYTH_PY=(--python python3.12)
        elif command -v python3.11 &>/dev/null; then
            MYTH_PY=(--python python3.11)
        fi
        if pipx install --force ${MYTH_PY[@]+"${MYTH_PY[@]}"} mythril 2>/dev/null; then
            log_ok "mythril installed"
        else
            log_warn "mythril failed (try: pipx install --python python3.12 mythril)"
        fi
    fi

    # Surya is a legacy ConsenSys tool with no wheel for modern Python. Prefer
    # slither/aderyn for call graphs; install surya only under Python 3.8-3.10.
    log_warn "surya skipped (legacy; no modern-Python wheel — use slither/aderyn or Python 3.8)"

    # Foundry (forge/cast/anvil)
    if command -v forge &>/dev/null; then
        log_ok "forge already installed"
    else
        if curl -L https://foundry.paradigm.xyz | bash; then
            if [ -x "$HOME/.foundry/bin/foundryup" ]; then
                "$HOME/.foundry/bin/foundryup" || log_warn "foundryup failed"
            fi
        else
            log_warn "Foundry installer failed"
        fi
    fi

    # Aderyn was retired upstream in 2026. Do not install it on new machines;
    # existing binaries keep working. Use Slither + Medusa/Halmos instead.
    if command -v aderyn &>/dev/null; then
        log_ok "aderyn already installed (upstream retired; existing install)"
    else
        log_warn "aderyn skipped (retired upstream 2026; use slither/medusa/halmos)"
    fi

    # Medusa (Go)
    if command -v medusa &>/dev/null; then
        log_ok "medusa already installed"
    elif command -v go &>/dev/null; then
        GOBIN="$GOPATH/bin" go install github.com/crytic/medusa@latest 2>/dev/null \
            || log_warn "medusa failed (run: go install github.com/crytic/medusa@latest)"
    else
        log_warn "go not found — install medusa manually"
    fi

    # Echidna (Haskell; binary release only — no pip/apt package).
    if command -v echidna &>/dev/null; then
        log_ok "echidna already installed"
    else
        ECHIDNA_VERSION="${ECHIDNA_VERSION:-2.4.0}"
        ECHIDNA_ARCH="x86_64"
        case "$(uname -m)" in aarch64|arm64) ECHIDNA_ARCH="aarch64" ;; esac
        ECHIDNA_OS="linux"
        case "$(uname -s)" in Darwin) ECHIDNA_OS="macos" ;; esac
        ECHIDNA_URL="https://github.com/crytic/echidna/releases/download/v${ECHIDNA_VERSION}/echidna-${ECHIDNA_VERSION}-${ECHIDNA_ARCH}-${ECHIDNA_OS}.tar.gz"
        mkdir -p "$HOME/.local/bin"
        if curl -fsSL "$ECHIDNA_URL" -o /tmp/echidna.tar.gz \
            && tar -xzf /tmp/echidna.tar.gz -C "$HOME/.local/bin" echidna \
            && chmod +x "$HOME/.local/bin/echidna"; then
            log_ok "echidna ${ECHIDNA_VERSION} installed to ~/.local/bin"
        else
            log_warn "echidna install failed (download: $ECHIDNA_URL)"
        fi
        rm -f /tmp/echidna.tar.gz
    fi

    # Solana CLI + Anchor (best-effort; large downloads)
    if command -v solana &>/dev/null; then
        log_ok "solana already installed"
    else
        sh -c "$(curl -sSfL https://release.anza.xyz/stable/install)" 2>/dev/null \
            || log_warn "Solana CLI install failed (see docs.anza.xyz/cli/install)"
    fi
    if command -v anchor &>/dev/null; then
        log_ok "anchor already installed"
    elif command -v cargo &>/dev/null; then
        cargo install --git https://github.com/coral-xyz/anchor avm --locked 2>/dev/null \
            && avm install latest 2>/dev/null \
            || log_warn "anchor/avm failed (run: cargo install --git https://github.com/coral-xyz/anchor avm --locked)"
    else
        log_warn "cargo not found — install anchor manually"
    fi

    # Solhint + MCP servers
    if command -v npm &>/dev/null; then
        npm install -g solhint 2>/dev/null || log_warn "solhint failed (run: npm install -g solhint)"
        # foundry-mcp: install it, but invoke dist/index.js with node.
        # The published bin has no shebang, so `npx foundry-mcp` fails.
        if npm install -g foundry-mcp 2>/dev/null; then
            log_ok "foundry-mcp installed (run: node \$(npm root -g)/foundry-mcp/dist/index.js)"
        else
            log_warn "foundry-mcp install failed (run: npm install -g foundry-mcp)"
        fi
        if npm install -g @marchev/claudit 2>/dev/null; then
            log_ok "claudit installed (Solodit MCP; set SOLODIT_API_KEY to use)"
        else
            log_warn "claudit failed (run: npm install -g @marchev/claudit)"
        fi
    else
        log_warn "npm not found — install solhint/foundry-mcp manually"
    fi

    # Pin a common solc version when solc-select is available
    if command -v solc-select &>/dev/null; then
        solc-select install 0.8.28 >/dev/null 2>&1 && solc-select use 0.8.28 >/dev/null 2>&1 \
            && log_ok "solc 0.8.28 selected" \
            || log_warn "solc-select install 0.8.28 failed (run manually)"
    fi

    # evm-agent-toolkit: source-build (its npm package is unpublished). Provides
    # structured Slither/Forge/cast/storage-layout/trace/calldata tools.
    EVM_MCP_DIR="${EVM_AGENT_TOOLKIT_DIR:-$HOME/.local/share/bughunter/evm-agent-toolkit}"
    if [ -f "$EVM_MCP_DIR/build/mcp/index.js" ]; then
        chmod +x "$EVM_MCP_DIR/build/mcp/index.js"
        mkdir -p "$HOME/.local/bin"
        ln -sf "$EVM_MCP_DIR/build/mcp/index.js" "$HOME/.local/bin/evm-agent-toolkit"
        log_ok "evm-agent-toolkit already built ($EVM_MCP_DIR)"
    elif command -v git &>/dev/null && command -v npm &>/dev/null; then
        if [ -d "$EVM_MCP_DIR/.git" ]; then
            git -C "$EVM_MCP_DIR" pull --ff-only >/dev/null 2>&1 || true
        else
            git clone --depth 1 https://github.com/0xendale/evm-agent-toolkit "$EVM_MCP_DIR" >/dev/null 2>&1 || true
        fi
        if (cd "$EVM_MCP_DIR" && npm install --no-audit --no-fund >/dev/null 2>&1 && npm run build >/dev/null 2>&1) \
            && [ -f "$EVM_MCP_DIR/build/mcp/index.js" ]; then
            chmod +x "$EVM_MCP_DIR/build/mcp/index.js"
            mkdir -p "$HOME/.local/bin"
            ln -sf "$EVM_MCP_DIR/build/mcp/index.js" "$HOME/.local/bin/evm-agent-toolkit"
            log_ok "evm-agent-toolkit built ($EVM_MCP_DIR/build/mcp/index.js)"
        else
            log_warn "evm-agent-toolkit build failed (see bughunter/mcp/web3-mcp/README.md)"
        fi
    else
        log_warn "evm-agent-toolkit skipped (git/npm missing; see bughunter/mcp/web3-mcp/README.md)"
    fi

    log_warn "solidity-audit-mcp: build from upstream — the npm name is a reserved placeholder"
    log_warn "  git clone https://github.com/mariano-aguero/solidity-audit-mcp && npm install && npm run build"
else
    log_warn "Web3 tools skipped (use --with-web3 to install)"
fi

# Update nuclei templates
echo ""
echo "[*] Updating nuclei templates..."
if command -v nuclei &>/dev/null; then
    nuclei -update-templates 2>/dev/null || true
    log_ok "Nuclei templates updated"
fi

# Ensure Go bin is in PATH
if [[ ":$PATH:" != *":$GOPATH/bin:"* ]]; then
    log_warn "Add Go bin to your PATH:"
    echo "    export PATH=\$PATH:$GOPATH/bin"
    echo "    # Add to ~/.zshrc"
fi

# Python runtime/test dependencies used by helper tools.
echo ""
echo "[*] Installing Python dependencies..."
if [ -f requirements.txt ] && command -v uv &>/dev/null; then
    UV_PIP_ARGS=()
    if [ -z "${VIRTUAL_ENV:-}" ] && [ ! -d .venv ]; then
        # No active/discoverable venv — install into the system Python, same as
        # plain `python3 -m pip install` would target in this case.
        UV_PIP_ARGS+=(--system)
    fi
    # bash 3.2 (macOS default) aborts under set -u when expanding an empty array
    # as "${UV_PIP_ARGS[@]}" — which is the common case, since the array is only
    # populated when no venv is present. Same idiom as tools/_auth_helper.sh.
    if uv pip install ${UV_PIP_ARGS[@]+"${UV_PIP_ARGS[@]}"} -r requirements.txt; then
        log_ok "Python dependencies installed (via uv)"
    else
        log_warn "Python dependencies could not be installed automatically"
        log_warn "Run manually when network is available: uv pip install ${UV_PIP_ARGS[*]} -r requirements.txt"
    fi
elif command -v python3 &>/dev/null && [ -f requirements.txt ]; then
    if python3 -m pip install -r requirements.txt; then
        log_ok "Python dependencies installed"
    else
        log_warn "Python dependencies could not be installed automatically"
        log_warn "Run manually when network is available: python3 -m pip install -r requirements.txt"
    fi
else
    log_warn "python3/uv or requirements.txt not found — skipping Python dependencies"
fi

# Pro workflow tools (optional: --with-pro)
# Browser automation, cloud CLIs, proxy, and mobile runtime.
if [ "$INSTALL_PRO" = true ]; then
    echo ""
    echo "[*] Installing pro workflow tools..."
    export PATH="$HOME/.local/bin:$PATH"

    # Playwright (Python library + Chromium). Needed by dom_xss_harness.py and
    # browser_capture.py for real-browser confirmation.
    if command -v python3 &>/dev/null; then
        if python3 -m pip install --user --quiet playwright 2>/dev/null \
            || python3 -m pip install --user --quiet --break-system-packages playwright 2>/dev/null; then
            python3 -m playwright install chromium >/dev/null 2>&1 \
                && log_ok "playwright + chromium installed" \
                || log_warn "playwright installed; run: python3 -m playwright install chromium"
        else
            log_warn "playwright install failed (python3 -m pip install --user playwright)"
        fi
    fi

    # AWS CLI (cloud post-access / S3 / IAM)
    if command -v aws &>/dev/null; then
        log_ok "aws already installed"
    elif command -v pipx &>/dev/null; then
        pipx install awscli >/dev/null 2>&1 && log_ok "awscli installed" \
            || log_warn "awscli failed (pipx install awscli)"
    else
        log_warn "awscli skipped (pipx missing)"
    fi

    # mitmproxy (traffic capture / replay)
    if command -v mitmproxy &>/dev/null; then
        log_ok "mitmproxy already installed"
    elif command -v pipx &>/dev/null; then
        pipx install mitmproxy >/dev/null 2>&1 && log_ok "mitmproxy installed" \
            || log_warn "mitmproxy failed (pipx install mitmproxy)"
    else
        log_warn "mitmproxy skipped (pipx missing)"
    fi

    # Android platform-tools (ADB) + Frida (mobile runtime)
    if command -v adb &>/dev/null; then
        log_ok "adb already installed"
    elif command -v apt-get &>/dev/null; then
        sudo apt-get update -qq >/dev/null 2>&1 || true
        sudo apt-get install -y -qq adb >/dev/null 2>&1 \
            && log_ok "adb installed" \
            || log_warn "adb failed (sudo apt-get install adb)"
    else
        log_warn "adb skipped (no apt-get)"
    fi
    if command -v frida &>/dev/null; then
        log_ok "frida already installed"
    elif command -v pipx &>/dev/null; then
        pipx install frida-tools >/dev/null 2>&1 && log_ok "frida-tools installed" \
            || log_warn "frida-tools failed (Python 3.14 may be unsupported)"
    else
        log_warn "frida skipped (pipx missing)"
    fi

    log_warn "gcloud/az: install separately if the target is GCP/Azure (too large for this installer)"
else
    log_warn "Pro workflow tools skipped (use --with-pro to install)"
fi

# Verification
echo ""
echo "============================================="
echo "[*] Installation Verification"
echo "============================================="

ALL_TOOLS=(subfinder httpx nuclei ffuf nmap amass gau dalfox subjack sisakulint)
if [ "$INSTALL_CREDENTIAL_ATTACK" = true ]; then
    ALL_TOOLS+=(hashcat theHarvester cewler cupp trevorspray kerbrute)
fi
if [ "$INSTALL_WEB3" = true ]; then
    ALL_TOOLS+=(forge cast anvil slither solc-select crytic-compile aderyn medusa echidna halmos myth solhint claudit evm-agent-toolkit)
fi
if [ "$INSTALL_PRO" = true ]; then
    ALL_TOOLS+=(playwright aws mitmproxy adb frida)
fi
INSTALLED=0
MISSING=0

for tool in "${ALL_TOOLS[@]}"; do
    if command -v "$tool" &>/dev/null; then
        log_ok "$tool: $(which "$tool")"
        ((++INSTALLED))
    else
        log_err "$tool: NOT FOUND"
        ((++MISSING))
    fi
 done

echo ""
echo "============================================="
echo "  Installed: $INSTALLED / ${#ALL_TOOLS[@]}"
[ "$MISSING" -gt 0 ] && echo "  Missing: $MISSING (check errors above)"
echo "============================================="
