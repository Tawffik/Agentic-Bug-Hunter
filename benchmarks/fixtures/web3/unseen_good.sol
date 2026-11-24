// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;
contract SafePayments {
    address public admin;
    address public oracle;
    mapping(address=>uint256) public bal;
    modifier onlyOwner(){ require(msg.sender==admin,"no"); _; }
    modifier onlyRole(bytes32){ require(msg.sender==admin,"role"); _; }
    function initialize() external { require(admin==address(0),"init"); admin=msg.sender; }
    function pause() external onlyOwner { admin = msg.sender; }
    function withdrawAll() external onlyOwner { bal[msg.sender] = 0; }
    function setOracle(address o) external onlyOwner { oracle = o; }
    function mint(address to, uint256 a) external onlyRole("MINTER") { bal[to] += a; }
}
