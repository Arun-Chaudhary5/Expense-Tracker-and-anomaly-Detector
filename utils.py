import pandas as pd

def load_and_align(raw_path: str, labeled_path: str) -> pd.DataFrame:
    """
    Loads raw (unlabeled) and labeled transaction data and aligns them
    by Transaction_ID — NEVER by row position. Files that are exported
    independently make no guarantee about row order.
    """
    raw = pd.read_csv(raw_path)
    labeled = pd.read_csv(labeled_path)

    assert raw['Transaction_ID'].is_unique, "Duplicate Transaction_IDs in raw file"
    assert labeled['Transaction_ID'].is_unique, "Duplicate Transaction_IDs in labeled file"

    merged = raw.merge(
        labeled[['Transaction_ID', 'Category']],
        on='Transaction_ID',
        how='inner',
        validate='one_to_one'   # fails loudly if the join isn't 1:1 — cheap insurance
    )
    assert len(merged) == len(raw), "Row count changed after merge — IDs don't fully match"
    return merged


def evaluate(df: pd.DataFrame, predict_fn) -> float:
    df = df.copy()
    df['Predicted_Category'] = df['Merchant'].apply(predict_fn)
    accuracy = (df['Predicted_Category'] == df['Category']).mean()
    return accuracy, df