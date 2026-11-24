pragma solidity ^0.8.13;
contract SafeBank {
    mapping(address=>uint) public bal;
    uint256 private _lock;
    modifier nonReentrant(){ require(_lock==0,"re"); _lock=1; _; _lock=0; }
    function deposit() external payable { bal[msg.sender]+=msg.value; }
    function withdraw() external nonReentrant {
        uint a = bal[msg.sender];
        bal[msg.sender] = 0;               // CEI: state first
        (bool ok,) = msg.sender.call{value:a}(""); require(ok);
    }
}
