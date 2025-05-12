import random
import time

def simulate_iot_data():
    return {
        "hour": time.localtime().tm_hour,
        "day": time.localtime().tm_wday + 1,
        "temperature": round(random.uniform(22, 32), 1),
        "appliance_usage": round(random.uniform(100, 2000), 1)
    }

while True:
    data = simulate_iot_data()
    print("Simulated IoT Data:", data)
    time.sleep(10)