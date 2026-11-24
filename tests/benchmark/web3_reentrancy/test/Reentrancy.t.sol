// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;
import "forge-std/Test.sol";
import {Bank, Attacker} from "../src/Bank.sol";
contract ReentrancyTest is Test {
    function test_reentrancy_drains_bank() public {
        Bank bank = new Bank();
        address victim = address(0xBEEF);
        vm.deal(victim, 5 ether);
        vm.prank(victim); bank.deposit{value: 5 ether}();
        Attacker atk = new Attacker(bank);
        uint256 before = address(atk).balance;
        atk.attack{value: 1 ether}();
        assertGt(address(atk).balance, 1 ether, "attacker profit > deposit");
        assertEq(address(bank).balance, 0, "bank drained");
        emit log_named_uint("attacker_balance_wei", address(atk).balance);
    }
}
