import numpy as np
import time
import csv
from datetime import datetime
import os
os.chdir(r"C:\Users\abods\OneDrive\Desktop\bridge monitor")

# Thresholds (based on real SHM engineering values)
THRESHOLDS = {
    "vibration": 5.0,   # mm/s
    "strain": 200,       # microstrain
    "temperature": 45    # Celsius
}






def generate_reading(spike=False):
    if spike:
        return {
            "vibration": round(np.random.uniform(4.5, 8.0), 3),
            "strain": int(np.random.uniform(170, 260)),
            "temperature": int(np.random.uniform(43, 50))
        }
    return {
        "vibration": round(np.random.uniform(1.5, 3.0), 3),
        "strain": int(np.random.uniform(120, 160)),
        "temperature": int(np.random.uniform(36, 40))
    }








def check_alerts(reading):
    alert_triggered = False
    for sensor, value in reading.items():
        if value > THRESHOLDS[sensor]:
            print(f"  *** ALERT: {sensor} = {value} (threshold: {THRESHOLDS[sensor]}) ***")
            alert_triggered = True
    if not alert_triggered:
        print("  Status: all sensors nominal")





with open("bridge_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "vibration", "strain", "temperature", "alert"])





#Run
print("Smart Bridge Monitor — Simulation")
print("=" * 40)

for i in range(20):
    print(f"\nReading #{i + 1}")
    
    ## reading = generate_reading(spike=False) # change to spike=False for normal


    reading = generate_reading(spike=(i % 3 == 0))  ## this line to alternate between spike and normal
    print(f"  Vibration:   {reading['vibration']} mm/s")
    print(f"  Strain:      {reading['strain']} microstrain")
    print(f"  Temperature: {reading['temperature']} C")
    
    check_alerts(reading)

    # Save reading to CSV
    alert = any(reading[s] > THRESHOLDS[s] for s in reading)
    with open("bridge_data.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%H:%M:%S"),
            reading["vibration"],
            reading["strain"],
            reading["temperature"],
            "ALERT" if alert else "OK"
        ])


    time.sleep(1)

print("\n" + "=" * 40)
print("Simulation complete.")