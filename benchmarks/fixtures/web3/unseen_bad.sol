// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;
contract Payments {
    address public admin;
    address public oracle;
    uint256 public fee;
    mapping(address=>uint256) public bal;
    function pause() external { admin = msg.sender; }            // unguarded
    function withdrawAll() external { bal[msg.sender] = 0; }     // unguarded
    function setOracle(address o) external { oracle = o; }       // unguarded
    function mint(address to, uint256 a) external { bal[to] += a; } // unguarded
    function deposit() external payable { bal[msg.sender] += msg.value; } // user-facing, ok
}
