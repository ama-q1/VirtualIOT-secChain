const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
    // Read contract address from backend folder
    const backendPath = "A:\\VirtualIOT-secChain\\backend\\contract-info.json";
    const contractInfo = JSON.parse(fs.readFileSync(backendPath, "utf8"));

    console.log("🔗 Connecting to IoTIdentity at:", contractInfo.address);

    const IoTIdentity = await hre.ethers.getContractFactory("IoTIdentity");
    const contract = await IoTIdentity.attach(contractInfo.address);

    // Device ID to register
    const deviceId = "device_001";

    // Calculate SHA256 hash of deviceId to match smart contract bytes32 parameter
    const crypto = require("crypto");
    const deviceIdHash = "0x" + crypto.createHash("sha256").update(deviceId).digest("hex");

    console.log(`📝 Registering device "${deviceId}"`);
    console.log(`   Hash: ${deviceIdHash}`);

    // Register device on blockchain
    const tx = await contract.registerDevice(deviceIdHash);
    await tx.wait();

    console.log("✅ Device successfully whitelisted on the Blockchain!");
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error("❌ Registration failed:", error);
        process.exit(1);
    });