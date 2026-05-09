import pandas as pd
import matplotlib.pyplot as plt

# Load your CSV data
df = pd.read_csv("bridge_data.csv")

# --- Chart 1: Vibration over time ---
plt.figure(figsize=(10, 4))
plt.plot(df["timestamp"], df["vibration"], color="steelblue", linewidth=1.5, label="Vibration")
plt.axhline(y=5.0, color="red", linestyle="--", linewidth=1, label="Threshold (5.0)")
plt.title("Bridge Vibration Over Time")
plt.xlabel("Time")
plt.ylabel("mm/s")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig("vibration_chart.png")
plt.show()

# --- Chart 2: Strain over time ---
plt.figure(figsize=(10, 4))
plt.plot(df["timestamp"], df["strain"], color="darkorange", linewidth=1.5, label="Strain")
plt.axhline(y=200, color="red", linestyle="--", linewidth=1, label="Threshold (200)")
plt.title("Bridge Strain Over Time")
plt.xlabel("Time")
plt.ylabel("Microstrain")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig("strain_chart.png")
plt.show()

# --- Chart 3: Alert summary ---
alert_counts = df["alert"].value_counts()
plt.figure(figsize=(5, 5))
plt.pie(alert_counts, labels=alert_counts.index, autopct="%1.1f%%",
        colors=["tomato", "mediumseagreen"])
plt.title("Alert vs Normal Readings")
plt.savefig("alert_summary.png")
plt.show()

print("Charts saved to your folder.")