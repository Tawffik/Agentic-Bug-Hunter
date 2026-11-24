pragma solidity ^0.8.13;
contract Redeemer {
    mapping(address=>uint) public shares;
    function redeem() external {
        uint s = shares[msg.sender];
        (bool ok,) = msg.sender.call{value: s}(""); require(ok);
        shares[msg.sender] -= s;           // after external call
    }
}
