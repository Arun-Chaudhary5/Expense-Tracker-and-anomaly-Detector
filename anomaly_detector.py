import pandas as pd
import math
from collections import deque
import heapq


class SlidingWindowStats:
    def __init__(self, window_size):
        self.window_size = window_size
        self.window = deque()
        self.count = 0
        self.mean = 0.0
        self.M2 = 0.0

    def add(self, value):
        self.count += 1
        delta = value - self.mean
        self.mean += delta / self.count
        delta2 = value - self.mean
        self.M2 += delta * delta2
        self.window.append(value)

    def remove_oldest(self):
        old_value = self.window.popleft()
        if self.count == 1:
            self.count = 0
            self.mean = 0.0
            self.M2 = 0.0
            return
        
        old_count = self.count

        new_count = old_count - 1
        new_mean = (self.mean * old_count - old_value) / new_count
        self.M2 -= (old_value - self.mean) * (old_value - new_mean)

        self.count = new_count
        self.mean = new_mean
        if self.M2 < 0 and abs(self.M2) < 1e-10:
            self.M2 = 0.0

    def get_std(self):
        if self.count < 2:
            return 0.0
        variance = self.M2 / self.count
        return math.sqrt(max(variance, 0.0))

def add_alert(alert_heap, alert, top_k, alert_id):
    item = (
        alert["Z_Score"],
        alert_id,
        alert
    )

    if len(alert_heap) < top_k:
        heapq.heappush(alert_heap, item)

    elif alert["Z_Score"] > alert_heap[0][0]:
        heapq.heapreplace(alert_heap, item)      

WINDOW_SIZE = 30
Z_THRESHOLD = 3.0

def detect_anomalies(df, window_size=30, z_threshold=3.0, top_k=10):

    stats = SlidingWindowStats(window_size)

    anomalies = []
    alert_heap = []
    alert_id = 0

    for index, row in df.iterrows():

        amount = row["Amount"]

        # Evaluate using previous window
        if stats.count == window_size:

            mean = stats.mean
            std = stats.get_std()

            if std > 0:
                z_score = abs((amount - mean) / std)
            else:
                z_score = 0.0

            if z_score > z_threshold:

                alert = {
                    "Date": row["Date"],
                    "Merchant": row["Merchant"],
                    "Amount": amount,
                    "Mean": round(mean, 2),
                    "Std": round(std, 2),
                    "Z_Score": round(z_score, 2)
                }

                anomalies.append(alert)

                add_alert(
                    alert_heap,
                    alert,
                    top_k,
                    alert_id
                )

                alert_id += 1

            stats.remove_oldest()

        stats.add(amount)

    anomaly_df = pd.DataFrame(anomalies)

    top_alerts = [
        item[2]
        for item in sorted(
            alert_heap,
            key=lambda item: item[0],
            reverse=True
        )
    ]

    top_alerts_df = pd.DataFrame(top_alerts)

    return anomaly_df, top_alerts_df

def main():

    df = pd.read_csv("data/transactions.csv")

    df = df.sort_values("Date").reset_index(drop=True)

    anomaly_df, top_alerts_df = detect_anomalies(df)

    anomaly_df.to_csv(
        "data/anomalies.csv",
        index=False
    )

    top_alerts_df.to_csv(
        "data/top_alerts.csv",
        index=False
    )

    print("\nTOP 10 SEVERE ALERTS:\n")
    print(top_alerts_df)

    print(f"\nTotal anomalies detected: {len(anomaly_df)}")


if __name__ == "__main__":
    main()




