import streamlit as st
import numpy as np
import pandas as pd
import time
from datetime import datetime
import csv
import os

os.chdir(r"C:\Users\abods\OneDrive\Desktop\bridge monitor")

# --- Page config ---
st.set_page_config(page_title="Smart Bridge Monitor", layout="wide")

# --- Thresholds ---
THRESHOLDS = {
    "vibration": 5.0,
    "strain": 200,
    "temperature": 45
}

# --- Title ---
st.title("Smart Bridge Health Monitor")
st.caption("Al Maqta Bridge, Abu Dhabi — Live Sensor Simulation")

# --- Sidebar controls ---
st.sidebar.header("Controls")
spike = st.sidebar.toggle("Simulate Overload Event")
speed = st.sidebar.slider("Reading interval (seconds)", 1, 5, 2)
readings_count = st.sidebar.slider("Number of readings", 10, 100, 20)

# --- Generate reading ---
def generate_reading(spike=False):
    if spike:
        return {
            "vibration": round(np.random.uniform(4.5, 8.0), 2),
            "strain": int(np.random.uniform(170, 260)),
            "temperature": int(np.random.uniform(43, 50))
        }
    return {
        "vibration": round(np.random.uniform(1.5, 3.0), 2),
        "strain": int(np.random.uniform(120, 160)),
        "temperature": int(np.random.uniform(36, 40))
    }

# --- Run button ---
if st.button("Start Monitoring"):

    # Setup CSV
    with open("bridge_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "vibration", "strain", "temperature", "alert"])

    # Placeholders
    col1, col2, col3 = st.columns(3)
    vib_metric = col1.empty()
    str_metric = col2.empty()
    tmp_metric = col3.empty()

    st.divider()
    chart_placeholder = st.empty()
    alert_placeholder = st.empty()

    history = []

    for i in range(readings_count):
        reading = generate_reading(spike=spike)
        alert = any(reading[s] > THRESHOLDS[s] for s in reading)
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Save to CSV
        with open("bridge_data.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                reading["vibration"],
                reading["strain"],
                reading["temperature"],
                "ALERT" if alert else "OK"
            ])

        # Update metrics
        vib_metric.metric(
            "Vibration (mm/s)",
            reading["vibration"],
            delta=round(reading["vibration"] - THRESHOLDS["vibration"], 2),
            delta_color="inverse"
        )
        str_metric.metric(
            "Strain (μɛ)",
            reading["strain"],
            delta=reading["strain"] - THRESHOLDS["strain"],
            delta_color="inverse"
        )
        tmp_metric.metric(
            "Temperature (°C)",
            reading["temperature"],
            delta=reading["temperature"] - THRESHOLDS["temperature"],
            delta_color="inverse"
        )

        # Update history and chart
        history.append({
            "time": timestamp,
            "vibration": reading["vibration"],
            "strain": reading["strain"],
            "temperature": reading["temperature"]
        })
        df = pd.DataFrame(history).set_index("time")
        chart_placeholder.line_chart(df)

        # Alert box
        if alert:
            alert_placeholder.error(
                f"ALERT — Reading #{i+1}: "
                f"Vibration={reading['vibration']} mm/s | "
                f"Strain={reading['strain']} μɛ | "
                f"Temp={reading['temperature']}°C"
            )
        else:
            alert_placeholder.success(f"Reading #{i+1} — All sensors nominal")

        time.sleep(speed)

    st.balloons()
    st.success("Simulation complete. Data saved to bridge_data.csv")
