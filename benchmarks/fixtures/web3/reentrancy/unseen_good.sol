pragma solidity ^0.8.13;
contract SafeRedeemer {
    mapping(address=>uint) public shares;
    bool private locked;
    modifier guard(){ require(!locked,"re"); locked=true; _; locked=false; }
    function redeem() external guard {
        uint s = shares[msg.sender];
        shares[msg.sender] = 0;
        (bool ok,) = msg.sender.call{value: s}(""); require(ok);
    }
}
