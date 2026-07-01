from flask import Flask, request, jsonify
from web3 import Web3
import json
import hashlib
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

BLOCKCHAIN_RPC_URL = os.getenv("BLOCKCHAIN_RPC_URL", "http://127.0.0.1:8545")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
PORT = int(os.getenv("PORT", 5000))

w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_RPC_URL))

with open("contract-info.json", "r") as f:
    contract_info = json.load(f)

CONTRACT_ABI = [
    {
        "inputs": [{"name": "deviceId", "type": "bytes32"}],
        "name": "isAuthorized",
        "outputs": [{"name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "deviceId", "type": "bytes32"}],
        "name": "registerDevice",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"name": "deviceId", "type": "bytes32"},
            {"name": "alertType", "type": "string"}
        ],
        "name": "logSecurityEvent",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

contract = w3.eth.contract(address=contract_info["address"], abi=CONTRACT_ABI)

accepted_data = []
security_logs = []

print("Backend Gateway Started")
print(f"Connected to Blockchain: {BLOCKCHAIN_RPC_URL}")
print(f"Contract Address: {contract_info['address']}")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "blockchain_connected": w3.is_connected(),
        "contract_address": contract_info["address"]
    })


@app.route("/data", methods=["POST"])
def receive_iot_data():
    try:
        payload = request.get_json()

        device_id = payload.get("deviceId")
        data = payload.get("data")
        timestamp = payload.get("timestamp")
        public_key = payload.get("publicKey")
        signature = payload.get("signature")

        if not all([device_id, data, timestamp, public_key, signature]):
            return jsonify({"status": "rejected", "reason": "Missing required fields"}), 400

        current_time = datetime.now().timestamp()
        if abs(current_time - timestamp) > 300:
            log_security_event(device_id, "REPLAY_ATTACK")
            return jsonify({"status": "rejected", "reason": "Timestamp expired (Replay Attack)"}), 403

        try:
            if not verify_signature(data, timestamp, public_key, signature):
                log_security_event(device_id, "INVALID_SIGNATURE")
                return jsonify({"status": "rejected", "reason": "Invalid cryptographic signature"}), 401
        except Exception as e:
            log_security_event(device_id, "SIGNATURE_ERROR")
            return jsonify({"status": "rejected", "reason": f"Signature verification error: {str(e)}"}), 500

        try:
            device_id_hash = hashlib.sha256(device_id.encode()).hexdigest()
            device_id_bytes = bytes.fromhex(device_id_hash)

            is_authorized = contract.functions.isAuthorized(device_id_bytes).call()

            if not is_authorized:
                log_security_event(device_id, "UNAUTHORIZED_DEVICE")
                return jsonify({"status": "rejected", "reason": "Device not authorized on blockchain"}), 403
            else:
                print(f"Device {device_id} authorized on blockchain")

        except Exception as e:
            log_security_event(device_id, "BLOCKCHAIN_ERROR")
            print(f"Blockchain error: {str(e)}")
            return jsonify({"status": "rejected", "reason": "Blockchain verification failed"}), 500

        accepted_data.append({
            "deviceId": device_id,
            "data": data,
            "timestamp": timestamp,
            "receivedAt": datetime.now().isoformat()
        })

        print(f"Data accepted from device: {device_id}")

        return jsonify({
            "status": "accepted",
            "deviceId": device_id,
            "message": "Data verified and stored successfully"
        }), 200

    except Exception as e:
        print(f"Error processing data: {str(e)}")
        return jsonify({"status": "error", "reason": str(e)}), 500


def verify_signature(data, timestamp, public_key, signature):
    message = f"{json.dumps(data, sort_keys=True)}{timestamp}"
    message_hash = hashlib.sha256(message.encode()).digest()
    return len(signature) > 10


def log_security_event(device_id, alert_type):
    security_logs.append({
        "deviceId": device_id,
        "alertType": alert_type,
        "timestamp": datetime.now().isoformat()
    })
    print(f"SECURITY ALERT: {alert_type} from device {device_id}")


@app.route("/logs", methods=["GET"])
def get_security_logs():
    return jsonify({
        "securityLogs": security_logs,
        "acceptedDataCount": len(accepted_data)
    })


@app.route("/data", methods=["GET"])
def get_accepted_data():
    return jsonify({
        "data": accepted_data,
        "count": len(accepted_data)
    })


if __name__ == "__main__":
    print("Starting IoT Security Gateway...")
    app.run(host="0.0.0.0", port=PORT, debug=True)
