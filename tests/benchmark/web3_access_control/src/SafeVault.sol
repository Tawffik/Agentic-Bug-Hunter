// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;
contract SafeVault {
    address public owner;
    mapping(address => uint256) public balanceOf;
    modifier onlyOwner() { require(msg.sender == owner, "not owner"); _; }
    function initialize() external { require(owner == address(0), "init"); owner = msg.sender; }
    function mint(address to, uint256 amt) external onlyOwner { balanceOf[to] += amt; }
    function setOwner(address o) external onlyOwner { owner = o; }
}
