// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract IoTIdentity {
    address public owner;
    mapping(bytes32 => bool) public registeredDevices;
    uint256 public deviceCount;

    struct SecurityEvent {
        bytes32 deviceId;
        string eventType;
        uint256 timestamp;
        address reportedBy;
    }
    SecurityEvent[] public securityEvents;

    event DeviceRegistered(bytes32 indexed deviceId, address owner, uint256 timestamp);
    event DeviceRevoked(bytes32 indexed deviceId, uint256 timestamp);
    event SecurityAlert(bytes32 indexed deviceId, string alertType, uint256 timestamp);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function registerDevice(bytes32 deviceId) public onlyOwner {
        require(!registeredDevices[deviceId], "already registered");
        registeredDevices[deviceId] = true;
        deviceCount++;
        emit DeviceRegistered(deviceId, msg.sender, block.timestamp);
    }

    function isAuthorized(bytes32 deviceId) public view returns (bool) {
        return registeredDevices[deviceId];
    }

    function revokeDevice(bytes32 deviceId) public onlyOwner {
        require(registeredDevices[deviceId], "not registered");
        registeredDevices[deviceId] = false;
        deviceCount--;
        emit DeviceRevoked(deviceId, block.timestamp);
    }

    function logSecurityEvent(bytes32 deviceId, string calldata alertType) public {
        securityEvents.push(SecurityEvent(deviceId, alertType, block.timestamp, msg.sender));
        emit SecurityAlert(deviceId, alertType, block.timestamp);
    }

    function getSecurityEventsCount() public view returns (uint256) {
        return securityEvents.length;
    }

    // FIXED: Renamed 'event' to 'evt' because 'event' is reserved
    function getSecurityEvent(uint256 index) public view returns (bytes32, string memory, uint256, address) {
        require(index < securityEvents.length, "out of bounds");
        SecurityEvent memory evt = securityEvents[index];
        return (evt.deviceId, evt.eventType, evt.timestamp, evt.reportedBy);
    }
}
