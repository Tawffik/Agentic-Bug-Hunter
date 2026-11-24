// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;
contract Vault {
    address public owner;
    mapping(address => uint256) public balanceOf;
    function initialize() external { owner = msg.sender; }
    function mint(address to, uint256 amt) external { balanceOf[to] += amt; }
    function setOwner(address o) external { owner = o; }
    function deposit() external payable { balanceOf[msg.sender] += msg.value; }
}
