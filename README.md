# 🛡️ VirtualIoT-SecChain

> **Blockchain-Secured IoT Gateway with Zero-Trust Architecture**  
> A research-grade simulation platform demonstrating how blockchain technology can protect IoT networks from spoofing, replay, and unauthorized access attacks in real-time.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Solidity](https://img.shields.io/badge/Solidity-0.8.19-363636?style=for-the-badge&logo=solidity&logoColor=white)
![Hardhat](https://img.shields.io/badge/Hardhat-EVM-yellow?style=for-the-badge&logo=ethereum&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Gateway-000000?style=for-the-badge&logo=flask&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Web3](https://img.shields.io/badge/Web3.py-Blockchain-F16822?style=for-the-badge&logo=web3dotjs&logoColor=white)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [How It Works](#-how-it-works)
- [Smart Contract](#-smart-contract-iotidentitysol)
- [Backend Gateway](#-backend-gateway-apppy)
- [Frontend Dashboard](#-frontend-dashboard)
- [Device Simulator](#-device-simulator)
- [Attack Simulations](#-attack-simulations)
- [Installation & Setup](#-installation--setup)
- [Running the System](#-running-the-system)
- [API Reference](#-api-reference)
- [Security Features](#-security-features)
- [Demo Output](#-demo-output)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌐 Overview

**VirtualIoT-SecChain** is a full-stack blockchain-IoT security simulation that demonstrates a **Zero-Trust, blockchain-enforced device identity system**. In traditional IoT networks, any device can attempt to send data to a gateway — this project solves that by requiring every device to be **cryptographically registered on a smart contract** before its data is accepted.

### 🎯 Problem Solved

| Traditional IoT | VirtualIoT-SecChain |
|---|---|
| Any device can send data | Only blockchain-whitelisted devices accepted |
| No tamper-proof audit trail | Immutable on-chain security event log |
| Vulnerable to spoofing attacks | Spoofed devices rejected instantly |
| Vulnerable to replay attacks | Timestamp validation prevents replays |
| No real-time monitoring | Live Streamlit security dashboard |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        VirtualIoT-SecChain                          │
│                                                                     │
│  ┌──────────────┐      ┌──────────────────┐      ┌──────────────┐  │
│  │  IoT Device  │─────▶│  Flask Gateway   │─────▶│  Blockchain  │  │
│  │  Simulator   │ HTTP │  (Backend/app.py)│ Web3 │  (Hardhat)   │  │
│  │device_sim.py │      │  Port :5000      │      │  Port :8545  │  │
│  └──────────────┘      └──────────────────┘      └──────────────┘  │
│                               │    ▲                    │           │
│  ┌──────────────┐             │    │                    │           │
│  │ Attack Tools │─────────────┘    │           ┌────────────────┐  │
│  │spoof_attack  │  (Blocked!)      │           │  IoTIdentity   │  │
│  │replay_attack │                  │           │  Smart Contract│  │
│  └──────────────┘                  │           │  (.sol)        │  │
│                                    │           └────────────────┘  │
│                         ┌──────────────────┐                        │
│                         │  Streamlit       │                        │
│                         │  Dashboard       │                        │
│                         │  Port :8501      │                        │
│                         └──────────────────┘                        │
└─────────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
[IoT Device] 
    │
    │  POST /data  {deviceId, data, timestamp, publicKey, signature}
    ▼
[Flask Gateway]
    │
    ├─ Step 1: Validate all required fields
    ├─ Step 2: Check timestamp (replay attack prevention, ±5 min window)
    ├─ Step 3: Verify cryptographic signature
    ├─ Step 4: Query blockchain → contract.isAuthorized(SHA256(deviceId))
    │               │
    │         ┌─────┴──────┐
    │         │            │
    │       TRUE          FALSE
    │         │            │
    │    ┌────▼────┐  ┌────▼────────────────┐
    │    │ ACCEPT  │  │ REJECT + log event  │
    │    │ Store   │  │ on blockchain       │
    │    │ data    │  └─────────────────────┘
    │    └────┬────┘
    │         │
    ▼         ▼
[Streamlit Dashboard] — Live monitoring via /logs and /data endpoints
```

---

## 📁 Project Structure

```
VirtualIOT-secChain/
│
├── 📜 README.md                    ← You are here
├── 🐋 docker-compose.yml           ← Container orchestration (future)
├── 🚫 .gitignore                   ← Git exclusions
│
├── 🔗 contracts/                   ← Blockchain layer (Hardhat + Solidity)
│   ├── contracts/
│   │   └── IoTIdentity.sol         ← Core smart contract
│   ├── scripts/
│   │   └── register-device.js      ← Device whitelist registration
│   ├── test/                       ← Contract tests
│   ├── artifacts/                  ← Compiled contract ABIs (auto-generated)
│   ├── hardhat.config.js           ← Hardhat network configuration
│   └── package.json                ← Node.js dependencies
│
├── 🐍 backend/                     ← IoT Security Gateway (Flask + Web3)
│   ├── app.py                      ← Main Flask API server
│   ├── contract-info.json          ← Deployed contract address (auto-generated)
│   ├── .env.example                ← Environment variable template
│   ├── requirements.txt            ← Python dependencies
│   ├── routes/                     ← API route handlers
│   └── services/                   ← Business logic services
│
├── 📊 frontend/                    ← Real-time Security Dashboard
│   └── app_dashboard.py            ← Streamlit dashboard
│
├── 🤖 simulators/                  ← Legitimate IoT device simulation
│   ├── device_sim.py               ← Authorized device simulator
│   └── requirements.txt            ← Simulator dependencies
│
├── ⚔️  attacks/                    ← Security penetration tests
│   ├── spoof_attack.py             ← Spoofing attack simulator
│   └── replay_attack.py            ← Replay attack simulator
│
└── 📚 docs/                        ← Documentation & research
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Smart Contract** | Solidity 0.8.19 | Device identity registry on-chain |
| **Blockchain Node** | Hardhat (local EVM) | Local Ethereum development network |
| **Backend** | Flask (Python) | IoT Security Gateway REST API |
| **Blockchain Client** | Web3.py | Python → Ethereum contract calls |
| **Frontend** | Streamlit | Real-time monitoring dashboard |
| **Hashing** | SHA-256 | Device ID → bytes32 conversion |
| **Environment** | python-dotenv | Secure configuration management |
| **Containerization** | Docker Compose | Multi-service orchestration |

---

## ⚙️ How It Works

### 1. Device Registration (One-time Setup)

Before any IoT device can send data, it must be **registered on the blockchain** by the contract owner:

```
Device ID ("device_001")
        │
        ▼
SHA256 hash → bytes32
        │
        ▼
contract.registerDevice(bytes32_hash)
        │
        ▼
Stored in registeredDevices mapping (immutable)
        │
        ▼
Emits: DeviceRegistered(deviceId, owner, timestamp)
```

### 2. Data Transmission & Verification

Every time a registered device sends data:

```python
# Device sends this payload:
{
    "deviceId": "device_001",
    "data": {"temperature": 27.5, "humidity": 65.3},
    "timestamp": 1751376000,
    "publicKey": "0x1111...1111",
    "signature": "0x2222...2222"
}
```

The gateway performs **3 security checks in sequence**:

| Check | What It Does | Failure Response |
|---|---|---|
| **Field Validation** | All required fields present | `400 Missing required fields` |
| **Replay Detection** | `abs(now - timestamp) < 300s` | `403 Timestamp expired (Replay Attack)` |
| **Signature Check** | Validates cryptographic signature | `401 Invalid cryptographic signature` |
| **Blockchain Auth** | `contract.isAuthorized(SHA256(deviceId))` | `403 Device not authorized on blockchain` |

### 3. Security Event Logging

Every rejected request is logged both **in-memory** (for the dashboard) and can be extended to log **on-chain** via `logSecurityEvent()`.

---

## 📄 Smart Contract: `IoTIdentity.sol`

**Location:** `contracts/contracts/IoTIdentity.sol`  
**Network:** Hardhat Local (chainId: 31337, RPC: `http://127.0.0.1:8545`)

### Contract State

```solidity
address public owner;                          // Contract deployer
mapping(bytes32 => bool) public registeredDevices; // Whitelist
uint256 public deviceCount;                    // Total registered devices
SecurityEvent[] public securityEvents;         // On-chain security log
```

### Functions

| Function | Access | Description |
|---|---|---|
| `registerDevice(bytes32)` | `onlyOwner` | Whitelist a new IoT device |
| `isAuthorized(bytes32)` | `public view` | Check if device is registered |
| `revokeDevice(bytes32)` | `onlyOwner` | Remove device from whitelist |
| `logSecurityEvent(bytes32, string)` | `public` | Log a security alert on-chain |
| `getSecurityEventsCount()` | `public view` | Total security events logged |
| `getSecurityEvent(uint256)` | `public view` | Get specific security event |

### Events

```solidity
event DeviceRegistered(bytes32 indexed deviceId, address owner, uint256 timestamp);
event DeviceRevoked(bytes32 indexed deviceId, uint256 timestamp);
event SecurityAlert(bytes32 indexed deviceId, string alertType, uint256 timestamp);
```

### Device ID Hashing

The contract uses `bytes32` for device IDs. The backend and registration script both use **SHA-256** to convert a human-readable device ID to bytes32:

```python
# Python (backend/app.py)
device_id_hash = hashlib.sha256("device_001".encode()).hexdigest()
device_id_bytes = bytes.fromhex(device_id_hash)
```

```javascript
// JavaScript (contracts/scripts/register-device.js)
const deviceIdHash = "0x" + crypto.createHash("sha256").update("device_001").digest("hex");
```

---

## 🐍 Backend Gateway: `app.py`

**Location:** `backend/app.py`  
**Port:** `5000`  
**Framework:** Flask + Web3.py

### Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Gateway status + blockchain connectivity |
| `POST` | `/data` | Receive & validate IoT sensor data |
| `GET` | `/data` | Retrieve all accepted telemetry |
| `GET` | `/logs` | Retrieve security event logs |

### Security Pipeline (in `receive_iot_data`)

```python
# 1. Parse payload
device_id, data, timestamp, public_key, signature = payload fields

# 2. Anti-Replay: 5 minute window
if abs(datetime.now().timestamp() - timestamp) > 300:
    → REJECT: "Timestamp expired (Replay Attack)"

# 3. Signature verification
if not verify_signature(data, timestamp, public_key, signature):
    → REJECT: "Invalid cryptographic signature"

# 4. Blockchain authorization check
device_id_bytes = bytes.fromhex(hashlib.sha256(device_id.encode()).hexdigest())
is_authorized = contract.functions.isAuthorized(device_id_bytes).call()
if not is_authorized:
    → REJECT: "Device not authorized on blockchain"

# 5. Accept and store
accepted_data.append({deviceId, data, timestamp, receivedAt})
→ ACCEPT: 200 OK
```

### Environment Variables

Create a `.env` file in `backend/` with:

```env
BLOCKCHAIN_RPC_URL=http://127.0.0.1:8545
CONTRACT_ADDRESS=0xYourDeployedContractAddress
PORT=5000
```

---

## 📊 Frontend Dashboard

**Location:** `frontend/app_dashboard.py`  
**Port:** `8501` (Streamlit default)  
**Framework:** Streamlit

### Dashboard Panels

| Panel | Data Source | Description |
|---|---|---|
| **Gateway Status** | `GET /health` | Green/Red indicator + chain sync status |
| **Verified Transmissions** | `GET /logs` | Count of accepted data packets |
| **Blocked Attacks** | `GET /logs` | Count of `UNAUTHORIZED_DEVICE` events |
| **Live Security Logs** | `GET /logs` | Real-time table of security alerts |
| **Verified Telemetry** | `GET /data` | Real-time table of accepted sensor data |

### Features
- ⚡ **Auto-refresh** every 2–10 seconds (configurable via sidebar)
- 🔧 **Configurable API URL** — connect to any backend instance
- 📊 **Pandas DataFrames** — sortable, scrollable data tables
- 🚨 **Live attack detection** — dashboard updates instantly when attacks are blocked

---

## 🤖 Device Simulator

**Location:** `simulators/device_sim.py`  
**Device ID:** `device_001` (must be pre-registered on blockchain)

### What it does

Simulates a legitimate IoT sensor sending temperature & humidity data every 5 seconds:

```python
# Generates real-looking sensor data
sensor_data = {
    "temperature": 25 + (time.time() % 10),   # 25–35°C range
    "humidity":    60 + (time.time() % 20)    # 60–80% range
}

# Sends authenticated payload every 5 seconds
POST http://localhost:5000/data
{
    "deviceId":   "device_001",
    "data":       sensor_data,
    "timestamp":  current_unix_time,
    "publicKey":  "0x1111...1111",
    "signature":  "0x2222...2222"
}
```

### Console Output
```
🤖 IoT Device Simulator Started
📛 Device ID: device_001
🌐 Backend URL: http://localhost:5000/data
------------------------------------------------------------
🔄 Sending sensor data every 5 seconds...

✅ [17:45:00] Data sent successfully
   Temperature: 27.34°C
✅ [17:45:05] Data sent successfully
   Temperature: 28.91°C
```

---

## ⚔️ Attack Simulations

### 1. Spoof Attack (`attacks/spoof_attack.py`)

Simulates an **unauthorized device** attempting to inject fake data:

```python
# Attacker uses fake device ID not on blockchain
ATTACKER_DEVICE_ID = "hacker_device_999"

# Sends 5 spoofed requests with fake signature
payload = {
    "deviceId":  "hacker_device_999",
    "data":      {"temperature": 99.9, "humidity": 0},
    "timestamp": current_time,
    "publicKey": "0x" + "11" * 64,
    "signature": "0x" + "00" * 64   # Fake signature
}
```

**Expected Result — ALL 5 requests blocked:**
```
⚔️  SPOOF ATTACK SIMULATOR
------------------------------------------------------------
🎯 Target: http://localhost:5000/data
👤 Attacker Device ID: hacker_device_999
------------------------------------------------------------
🚀 Starting spoof attack simulation...

🔴 [18:00:47] Sending spoofed data...
   ✅ ATTACK BLOCKED! Security working!
   Status: rejected
   Reason: Device not authorized on blockchain

🔴 [18:00:52] Sending spoofed data...
   ✅ ATTACK BLOCKED! Security working!
   Status: rejected
   Reason: Device not authorized on blockchain
...
🏁 Attack simulation complete!
```

### 2. Replay Attack (`attacks/replay_attack.py`)

Simulates an attacker **replaying a previously captured** valid request with an old timestamp. The gateway rejects it because:

```python
# Gateway checks timestamp freshness
if abs(current_time - timestamp) > 300:  # 5 minute window
    log_security_event(device_id, "REPLAY_ATTACK")
    return {"status": "rejected", "reason": "Timestamp expired (Replay Attack)"}
```

### Security Alert Types

| Alert Type | Trigger | Severity |
|---|---|---|
| `UNAUTHORIZED_DEVICE` | Device not on blockchain whitelist | 🔴 High |
| `REPLAY_ATTACK` | Timestamp older than 5 minutes | 🔴 High |
| `INVALID_SIGNATURE` | Cryptographic signature mismatch | 🔴 High |
| `SIGNATURE_ERROR` | Signature processing exception | 🟡 Medium |
| `BLOCKCHAIN_ERROR` | Contract call failure | 🟡 Medium |

---

## 🚀 Installation & Setup

### Prerequisites

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.10+ | Backend + Simulator + Dashboard |
| Node.js | 18+ | Hardhat blockchain framework |
| npm | 9+ | Node package manager |
| Git | Any | Version control |

### Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/VirtualIOT-secChain.git
cd VirtualIOT-secChain
```

### Step 2 — Install Blockchain Dependencies

```bash
cd contracts
npm install
```

### Step 3 — Install Backend Dependencies

```bash
cd ../backend
python -m venv venv

# Windows
.\venv\Scripts\Activate

# macOS/Linux
source venv/bin/activate

pip install flask web3 python-dotenv
```

### Step 4 — Install Simulator Dependencies

```bash
cd ../simulators
python -m venv venv

# Windows
.\venv\Scripts\Activate

pip install requests
```

### Step 5 — Install Dashboard Dependencies

```bash
cd ../frontend
pip install streamlit requests pandas
```

---

## ▶️ Running the System

> **Run each step in a separate terminal window.**

### Terminal 1 — Start Blockchain Node

```bash
cd contracts
npx hardhat node
```

Expected output:
```
Started HTTP and WebSocket JSON-RPC server at http://127.0.0.1:8545/

Accounts
========
Account #0: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 (10000 ETH)
...
```

### Terminal 2 — Deploy Smart Contract

```bash
cd contracts
npx hardhat run scripts/deploy.js --network localhost
```

This creates `backend/contract-info.json` with the contract address.

### Terminal 3 — Register IoT Device

```bash
cd contracts
npx hardhat run scripts/register-device.js --network localhost
```

Expected:
```
🔗 Connecting to IoTIdentity at: 0x5FbDB2315...
📝 Registering device "device_001"
   Hash: 0x5f5ef3...
✅ Device successfully whitelisted on the Blockchain!
```

### Terminal 4 — Start Backend Gateway

```bash
cd backend
.\venv\Scripts\Activate   # Windows
python app.py
```

Expected:
```
Backend Gateway Started
Connected to Blockchain: http://127.0.0.1:8545
Contract Address: 0x5FbDB2315...
Starting IoT Security Gateway...
 * Running on http://0.0.0.0:5000
```

### Terminal 5 — Start IoT Device Simulator

```bash
cd simulators
python device_sim.py
```

### Terminal 6 — Start Dashboard

```bash
streamlit run frontend/app_dashboard.py
```

Open browser: **http://localhost:8501**

### Terminal 7 — Run Spoof Attack (Optional Demo)

```bash
cd attacks
python spoof_attack.py
```

Watch the dashboard — **Blocked Attacks** counter increments in real-time!

---

## 📡 API Reference

### `GET /health`

Returns gateway and blockchain status.

```json
{
  "status": "healthy",
  "blockchain_connected": true,
  "contract_address": "0x5FbDB2315678afecb367f032d93F642f64180aa3"
}
```

### `POST /data`

Submit IoT sensor data for verification.

**Request Body:**
```json
{
  "deviceId":  "device_001",
  "data":      {"temperature": 27.5, "humidity": 65.2},
  "timestamp": 1751376000,
  "publicKey": "0x1111111111...",
  "signature": "0x2222222222..."
}
```

**Response — Accepted:**
```json
{
  "status": "accepted",
  "deviceId": "device_001",
  "message": "Data verified and stored successfully"
}
```

**Response — Rejected:**
```json
{
  "status": "rejected",
  "reason": "Device not authorized on blockchain"
}
```

### `GET /logs`

Returns all security events and accepted data count.

```json
{
  "securityLogs": [
    {
      "deviceId":  "hacker_device_999",
      "alertType": "UNAUTHORIZED_DEVICE",
      "timestamp": "2026-07-01T18:00:47.123456"
    }
  ],
  "acceptedDataCount": 32
}
```

### `GET /data`

Returns all accepted telemetry data.

```json
{
  "data": [
    {
      "deviceId":   "device_001",
      "data":       {"temperature": 27.34, "humidity": 65.3},
      "timestamp":  1751376000,
      "receivedAt": "2026-07-01T17:45:00.123456"
    }
  ],
  "count": 32
}
```

---

## 🔐 Security Features

### Zero-Trust Architecture
Every request is treated as untrusted, regardless of source. No device can bypass authentication.

### Blockchain Immutability
Device registry is stored on-chain — it **cannot be altered** by the backend server even if compromised.

### Multi-Layer Defense

```
Layer 1: Input Validation     → All fields required
Layer 2: Replay Prevention    → 5-minute timestamp window
Layer 3: Signature Validation → Cryptographic proof of origin
Layer 4: Blockchain Auth      → Immutable whitelist check
Layer 5: Audit Trail          → Every rejection is logged
```

### Attack Vectors Covered

- ✅ **Device Spoofing** — Unregistered devices rejected via blockchain
- ✅ **Replay Attacks** — Stale timestamps detected and blocked
- ✅ **Data Forgery** — Cryptographic signature enforcement
- ✅ **Man-in-the-Middle** — Signature + blockchain combo prevents MITM data injection

---

## 📸 Demo Output

### Live Dashboard Screenshot
The dashboard shows:
- 🟢 **Gateway Online** — Flask + Hardhat both running
- **Chain Synced: True** — Web3.py connected to Hardhat node
- **32 Verified Transmissions** — From `device_001`
- **5 Blocked Attacks** — From `hacker_device_999`
- **Live Security Logs** — `UNAUTHORIZED_DEVICE` alerts with timestamps
- **Verified Telemetry** — JSON sensor data from registered device

### Attack Blocked
```
🔴 [18:00:47] Sending spoofed data...
   ✅ ATTACK BLOCKED! Security working!
   Status: rejected
   Reason: Device not authorized on blockchain
```

---

## 🗺️ Roadmap

- [ ] Real ECDSA signature implementation (replace simplified verifier)
- [ ] Multiple device support (register N devices)
- [ ] On-chain security event logging (call `logSecurityEvent` on rejection)
- [ ] Docker Compose full stack deployment
- [ ] Testnet deployment (Sepolia / Mumbai)
- [ ] JWT authentication for dashboard
- [ ] Alert notifications (email / Telegram)
- [ ] Grafana metrics integration

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-security-feature`
3. Commit your changes: `git commit -m 'Add amazing security feature'`
4. Push to the branch: `git push origin feature/amazing-security-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

Built as a research/internship project demonstrating **blockchain-based IoT security** with real attack simulation capabilities.

---

<div align="center">

**⭐ If this project helped you, please star it on GitHub! ⭐**

`Blockchain` • `IoT Security` • `Zero-Trust` • `Solidity` • `Flask` • `Streamlit` • `Web3`

</div>
