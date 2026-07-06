import pandas as pd
import streamlit as st

from classifier import classify_transactions
from anomaly_detector import detect_anomalies


st.set_page_config(
    page_title="Expense Tracker & Anomaly Detector",
    page_icon="📊",
    layout="wide"
)


st.title("Expense Tracker & Anomaly Detector")

st.caption(
    "Merchant classification, category analytics, "
    "sliding-window anomaly detection and severity-ranked alerts."
)

# -----------------------------
# SIDEBAR CONTROLS
# -----------------------------

st.sidebar.header("Detector Settings")

window_size = st.sidebar.slider(
    "Sliding Window Size",
    min_value=10,
    max_value=100,
    value=30,
    step=5
)

z_threshold = st.sidebar.slider(
    "Z-Score Threshold",
    min_value=1.0,
    max_value=10.0,
    value=3.0,
    step=0.1
)

top_k = st.sidebar.slider(
    "Number of Priority Alerts",
    min_value=5,
    max_value=50,
    value=10,
    step=5
)

# -----------------------------
# LOAD DATA
# -----------------------------

df = pd.read_csv("data/Raw transactions.csv")

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values("Date").reset_index(drop=True)


# -----------------------------
# CLASSIFY TRANSACTIONS
# -----------------------------

classified_df = classify_transactions(df)


# -----------------------------
# DETECT ANOMALIES
# -----------------------------

anomaly_df, top_alerts_df = detect_anomalies(
    classified_df,
    window_size=window_size,
    z_threshold=z_threshold,
    top_k=top_k
)


# -----------------------------
# KPI METRICS
# -----------------------------

total_transactions = len(classified_df)

total_spending = classified_df["Amount"].sum()

total_anomalies = len(anomaly_df)

anomaly_rate = (
    total_anomalies / total_transactions * 100
    if total_transactions > 0
    else 0
)


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Transactions",
    f"{total_transactions:,}"
)

col2.metric(
    "Total Spending",
    f"₹{total_spending:,.2f}"
)

col3.metric(
    "Anomalies Detected",
    f"{total_anomalies:,}"
)

col4.metric(
    "Anomaly Rate",
    f"{anomaly_rate:.2f}%"
)


# -----------------------------
# CATEGORY ANALYTICS
# -----------------------------

st.header("Category-wise Spending")

category_spending = (
    classified_df
    .groupby("Predicted_Category")["Amount"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(category_spending)


# -----------------------------
# MONTHLY SPENDING TREND
# -----------------------------

st.header("Monthly Spending Trend")

monthly_spending = (
    classified_df
    .set_index("Date")
    .resample("ME")["Amount"]
    .sum()
)

st.line_chart(monthly_spending)


# -----------------------------
# TOP-K ALERTS
# -----------------------------

st.header(f"Top {top_k} Severe Alerts")

st.dataframe(
    top_alerts_df,
    use_container_width=True
)


# -----------------------------
# ALL ANOMALIES
# -----------------------------

st.header("Detected Anomalies")

st.dataframe(
    anomaly_df,
    use_container_width=True
)


# -----------------------------
# TRANSACTION EXPLORER
# -----------------------------

st.header("Transaction Explorer")

selected_category = st.selectbox(
    "Filter by Category",
    ["All"] +
    sorted(
        classified_df["Predicted_Category"]
        .unique()
        .tolist()
    )
)


if selected_category == "All":

    filtered_df = classified_df

else:

    filtered_df = classified_df[
        classified_df["Predicted_Category"]
        == selected_category
    ]


st.dataframe(
    filtered_df,
    use_container_width=True
)