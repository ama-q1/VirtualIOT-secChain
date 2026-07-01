import requests
import json
import time
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:5000/data"
DEVICE_ID = "device_001"

print("🤖 IoT Device Simulator Started")
print(f"📛 Device ID: {DEVICE_ID}")
print(f"🌐 Backend URL: {BACKEND_URL}")
print("-" * 60)

def send_sensor_data():
    """Generate and send sensor data to backend"""
    # Generate fake sensor data
    sensor_data = {
        "temperature": 25 + (time.time() % 10),
        "humidity": 60 + (time.time() % 20)
    }
    
    # Create timestamp
    timestamp = int(datetime.now().timestamp())
    
    # Create payload (simplified - no crypto for testing)
    payload = {
        "deviceId": DEVICE_ID,
        "data": sensor_data,
        "timestamp": timestamp,
        "publicKey": "0x" + "11" * 64,
        "signature": "0x" + "22" * 64
    }
    
    # Send to backend
    try:
        response = requests.post(BACKEND_URL, json=payload, timeout=5)
        
        if response.status_code == 200:
            print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Data sent successfully")
            print(f"   Temperature: {sensor_data['temperature']:.2f}°C")
        else:
            print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] Data rejected")
            print(f"   Reason: {response.json().get('reason', 'Unknown')}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] Backend not reachable!")
    except Exception as e:
        print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] Error: {str(e)}")

print("\n🔄 Sending sensor data every 5 seconds...")
print("Press Ctrl+C to stop\n")

try:
    while True:
        send_sensor_data()
        time.sleep(5)
except KeyboardInterrupt:
    print("\n\n🛑 Simulator stopped by user")
