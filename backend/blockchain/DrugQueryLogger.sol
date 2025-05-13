// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DrugQueryLogger {
    event DrugQueried(address indexed user, string drug, uint256 timestamp);

    function logQuery(string memory drug) public {
        emit DrugQueried(msg.sender, drug, block.timestamp);
    }
}
