const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
    console.log("🚀 Deploying IoTIdentity Contract...");

    const IoTIdentity = await hre.ethers.getContractFactory("IoTIdentity");
    const iotIdentity = await IoTIdentity.deploy();
    await iotIdentity.waitForDeployment();
    const contractAddress = await iotIdentity.getAddress();

    console.log("✅ IoTIdentity deployed to:", contractAddress);

    const [owner] = await hre.ethers.getSigners();
    console.log("👤 Contract Owner:", owner.address);

    const contractInfo = {
        address: contractAddress,
        owner: owner.address,
        network: "localhost"
    };

    const backendPath = path.join(__dirname, "..", "backend", "contract-info.json");
    fs.writeFileSync(backendPath, JSON.stringify(contractInfo, null, 2));

    console.log("📄 Contract info saved to backend/contract-info.json");
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });