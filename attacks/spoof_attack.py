import requests
import json
import time
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:5000/data"
ATTACKER_DEVICE_ID = "hacker_device_999"

print("⚔️  SPOOF ATTACK SIMULATOR")
print("-" * 60)
print(f"🎯 Target: {BACKEND_URL}")
print(f"👤 Attacker Device ID: {ATTACKER_DEVICE_ID}")
print("-" * 60)

def send_spoofed_data():
    """Try to send data as an unauthorized device"""
    
    # Fake sensor data
    fake_data = {
        "temperature": 99.9,
        "humidity": 0,
        "pressure": 0
    }
    
    # Create timestamp
    timestamp = int(datetime.now().timestamp())
    
    # Fake signature (not valid)
    fake_signature = "0x" + "00" * 64
    
    # Create payload
    payload = {
        "deviceId": ATTACKER_DEVICE_ID,
        "data": fake_data,
        "timestamp": timestamp,
        "publicKey": "0x" + "11" * 64,
        "signature": fake_signature
    }
    
    # Send to backend
    try:
        print(f"\n🔴 [{datetime.now().strftime('%H:%M:%S')}] Sending spoofed data...")
        response = requests.post(BACKEND_URL, json=payload, timeout=5)
        
        if response.status_code == 200:
            print(f"   ⚠️  ATTACK SUCCESSFUL! Data accepted!")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ✅ ATTACK BLOCKED! Security working!")
            print(f"   Status: {response.json().get('status')}")
            print(f"   Reason: {response.json().get('reason')}")
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Backend not reachable!")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

print("\n🚀 Starting spoof attack simulation...")
print("This will try to send data from an UNREGISTERED device\n")

try:
    for i in range(5):
        send_spoofed_data()
        time.sleep(2)
    
    print("\n🏁 Attack simulation complete!")
    print("Check backend logs for security alerts!")
    
except KeyboardInterrupt:
    print("\n\n🛑 Attack stopped by user")