# Expense Tracker & Anomaly Detector

An end-to-end transaction analytics application that classifies merchant transactions, detects anomalous spending patterns using a fixed-size sliding window with incremental statistics, prioritizes severe anomalies using a min-heap, and visualizes results through an interactive Streamlit dashboard.

The project was built to explore practical applications of data structures and algorithms in a transaction-processing pipeline.

---

## Features

### Merchant Classification

A rule-based merchant classification engine that categorizes transaction descriptions into spending categories such as:

- Food
- Clothing
- Electronics
- Travel
- Entertainment
- Health
- Education
- Real Estate
- Jewelry
- Sports
- Beauty
- Books
- Home

Merchant descriptions are normalized using regex-based text cleaning and classified using a specificity-weighted keyword scoring system.

The classifier achieved:

- **100% accuracy on the generated training dataset (sanity check)**
- **90.48% accuracy on 147 noisy held-out merchant variants**

The held-out evaluation introduces realistic bank-statement noise including prefixes, suffixes, capitalization changes, and merchant-name truncation.

---

### Sliding-Window Anomaly Detection

Transactions are processed chronologically and evaluated against the previous `W` transaction amounts.

For each transaction, the detector:

1. Maintains statistics for the previous fixed-size window.
2. Computes the historical mean and standard deviation.
3. Calculates the absolute Z-score of the incoming transaction.
4. Flags transactions whose Z-score exceeds a configurable threshold.
5. Removes the oldest transaction.
6. Adds the current transaction to the window.

The default configuration uses:

```text
Window Size = 30
Z-Score Threshold = 3.0
```

Importantly, the current transaction is evaluated **before being inserted into the sliding window**, preventing it from influencing its own anomaly score.

---

### Incremental Statistics with Welford's Algorithm

Instead of recomputing the mean and variance by scanning the complete window for every transaction, the detector maintains:

```text
count
mean
M2
```

New values are inserted using Welford's online update equations.

Since a fixed-size sliding window must also remove old values, the implementation uses reverse-Welford updates when the oldest transaction leaves the window.

A `deque` is used to maintain transaction order and support `O(1)` removal from the front.

This reduces statistical maintenance from:

```text
O(N × W)
```

to:

```text
O(N)
```

before Top-K alert prioritization, where:

```text
N = number of transactions
W = sliding-window size
```

---

### Heap-Based Alert Prioritization

The detector may generate many anomalies, while an analyst may only need to inspect the most severe alerts.

The project maintains a bounded min-heap containing the Top-K anomalies ranked by Z-score.

For every detected anomaly:

- Push the alert if the heap contains fewer than `K` elements.
- Compare the new alert with the minimum-severity alert at the heap root.
- Replace the root only when the new anomaly is more severe.

This avoids sorting every anomaly.

Complexity:

```text
Full sorting:       O(A log A)

Bounded min-heap:   O(A log K)
Heap space:         O(K)
```

where:

```text
A = number of detected anomalies
K = number of priority alerts
```

---

## Interactive Dashboard

The Streamlit dashboard provides:

- Total transaction count
- Total spending
- Number of detected anomalies
- Anomaly rate
- Category-wise spending analytics
- Monthly spending trends
- Severity-ranked Top-K alerts
- Complete anomaly table
- Category-filtered transaction explorer
- Configurable sliding-window size
- Configurable Z-score threshold
- Configurable number of priority alerts

Run the dashboard using:

```bash
python -m streamlit run src/dashboard.py
```

---

## Project Architecture

```text
Synthetic Transaction Dataset
            |
            v
Merchant Classification
            |
            v
Predicted Spending Categories
            |
            v
Chronological Transaction Stream
            |
            v
Fixed-Size Sliding Window
            |
            v
Welford Add + Reverse-Welford Remove
            |
            v
Z-Score Anomaly Detection
            |
            v
Bounded Min-Heap
            |
            v
Top-K Priority Alerts
            |
            v
Streamlit Dashboard
```

---

## Project Structure

```text
Expense Tracker and Anomaly Detection/
|
|-- data/
|   |-- Raw transactions.csv
|   |-- transactions.csv
|   |-- anomalies.csv
|   |-- top_alerts.csv
|   |-- classified_output.csv
|   `-- holdout_results.csv
|
|-- src/
|   |-- data_generator.py
|   |-- classifier.py
|   |-- anomaly_detector.py
|   |-- dashboard.py
|   `-- utils.py
|
|-- .gitignore
|-- README.md
`-- requirements.txt
```

---

## Installation

Clone the repository:

```bash
git clone <your-repository-url>

cd "Expense Tracker and Anomaly Detection"
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

---

## Usage

### 1. Generate Transaction Data

```bash
python src/data_generator.py
```

The generator creates synthetic Indian transaction data containing merchant names, transaction amounts, dates, banks, cities, and payment modes.

### 2. Run Merchant Classification Evaluation

```bash
python src/classifier.py
```

This performs:

- Training-data sanity checking
- Noisy held-out evaluation
- Classification result generation

### 3. Run Anomaly Detection

```bash
python src/anomaly_detector.py
```

This:

- Processes transactions chronologically
- Maintains fixed-size sliding-window statistics
- Detects anomalies using Z-scores
- Maintains Top-K severe alerts using a min-heap
- Saves anomaly results to CSV files

### 4. Launch Dashboard

```bash
python -m streamlit run src/dashboard.py
```

---

## Algorithmic Complexity

Let:

```text
N = number of transactions
W = sliding-window size
A = number of detected anomalies
K = number of priority alerts
```

| Operation | Time Complexity | Space Complexity |
|---|---:|---:|
| Merchant classification | O(N × C × M × L) | O(N) output |
| Welford insertion | O(1) | O(1) |
| Reverse-Welford removal | O(1) | O(1) |
| Deque insertion/removal | O(1) | O(W) |
| Z-score calculation | O(1) | O(1) |
| Top-K heap update | O(log K) | O(K) |
| Complete anomaly pipeline | O(N + A log K) | O(W + A + K) |

Where `C` is the number of categories, `M` is the average number of keywords per category, and `L` represents merchant-string matching cost.

---

## Example Results

Using the generated 5,000-transaction dataset:

```text
Transactions Processed:     5,000

Training Accuracy:
100.00% (sanity check)

Held-Out Classification:
147 noisy merchant variants

Held-Out Accuracy:
90.48%

Detected Anomalies:
219

Default Window Size:
30 transactions

Default Z-Score Threshold:
3.0

Priority Alerts:
Top 10 by Z-score
```

The classification training accuracy is reported only as a sanity check because the keyword dictionary was developed against the generated merchant dataset.

The **90.48% noisy held-out accuracy** is the more meaningful classification evaluation result.

---

## Key Engineering Decisions

### Why use a sliding window?

Spending behavior changes over time. Recent transactions provide a more adaptive baseline than statistics calculated over the entire transaction history.

### Why evaluate before inserting the current transaction?

Including the current transaction in its own baseline can increase the mean and standard deviation, reducing its anomaly score.

The detector therefore evaluates each transaction against the previous window before inserting it.

### Why use Welford's algorithm?

Recomputing mean and variance from scratch requires scanning the entire window for every transaction.

Incremental statistics avoid repeated scans and allow constant-time updates.

### Why use reverse-Welford updates?

Classic Welford updates statistics when values are added.

A fixed-size sliding window also requires removing the oldest observation, so reverse updates are used to maintain the same statistics without recomputing the entire window.

### Why use a min-heap?

Sorting every anomaly requires `O(A log A)` time.

A bounded min-heap maintains only the Top-K most severe alerts in `O(A log K)` time and `O(K)` heap space.

---

## Limitations

- Merchant classification is rule-based and depends on the coverage of the keyword dictionary.
- The noisy held-out dataset is synthetically generated rather than sourced from real bank statements.
- The anomaly detector currently uses a global spending baseline across all categories.
- Category-specific anomaly baselines could better distinguish normal high-value purchases from genuinely unusual transactions.
- Z-score detection assumes that mean and standard deviation provide a meaningful representation of recent spending behavior.
- The application is intended as an analytics and anomaly-detection project, not as a production fraud-detection system.

---

## Future Improvements

- Category-specific sliding-window anomaly detectors
- Robust statistics such as median and MAD for skewed transaction distributions
- Multiple transaction streams or user-specific spending profiles
- Persistent storage using PostgreSQL
- REST API for real-time transaction ingestion
- Automated tests for classifier and anomaly-detector correctness
- Dockerized deployment
- CI/CD pipeline
- Deployment of the Streamlit application

---

## Tech Stack

- Python
- Pandas
- Streamlit
- Regular Expressions
- Welford's Online Algorithm
- Reverse-Welford Sliding-Window Updates
- Deque
- Min-Heap / Priority Queue
- Z-Score Anomaly Detection

---

## Author

**Arun Kumar**

B.Tech, Biotechnology and Biochemical Engineering  
IIT Delhi
