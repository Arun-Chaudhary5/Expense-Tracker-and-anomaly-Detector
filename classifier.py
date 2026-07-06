
import random
import re
import pandas as pd

CATEGORY_KEYWORDS = {
    "Food": ["zomato", "swiggy", "dominos", "mcdonalds", "kfc", "pizza hut",
             "burger king", "subway", "starbucks", "cafe coffee day", "blinkit"],
    "Clothing": ["myntra", "ajio", "flipkart", "amazon", "hm", "zara", "levis",
                 "nike", "adidas", "puma"],
    "Home": ["urban ladder", "pepperfry", "ikea india", "hometown", "godrej",
             "nilkamal", "durian", "evok", "fabfurnish", "wooden street"],
    "Electronics": ["croma", "reliance", "vijay sales", "sony", "samsung",
                     "apple", "lg", "oneplus", "mi store", "motorola"],
    "Travel": ["makemytrip", "yatra", "goibibo", "cleartrip", "expedia",
               "booking", "airbnb", "oyo", "treebo", "fabhotels", "uber",
               "ola", "redbus", "indigo", "spicejet", "goair", "airasia"],
    "Entertainment": ["bookmyshow", "pvr", "inox", "cinepolis", "carnival",
                       "fun cinemas", "wave cinemas", "city gold", "srs",
                       "big cinemas", "netflix", "prime video", "hotstar",
                       "zee5", "sony liv", "voot", "alt balaji"],
    "Health": ["apollo", "medplus", "1mg", "netmeds", "pharmeasy", "practo",
               "lybrate", "docprime", "healthkart"],
    "Books": ["kindle", "book depository", "oxford", "crossword", "sapna",
              "rupa", "penguin", "harpercollins"],
    "Jewelry": ["tanishq", "kalyan", "malabar gold", "pc jeweller", "caratlane",
                "senco", "joyalukkas", "grt", "jubilee", "shubh"],
    "Sports": ["decathlon", "nike store", "adidas store", "puma store",
               "reebok", "under armour", "asics", "new balance",
               "skechers", "columbia"],
    "Beauty": ["nykaa", "purplle", "sephora", "the body shop", "forest essentials",
               "kama ayurveda", "mamaearth", "plum", "sugar", "colorbar"],
    "Education": ["byjus", "unacademy", "vedantu", "toppr", "khan academy",
                  "coursera", "udemy", "edx", "skillshare", "linkedin"],
    "Real Estate": ["99acres", "magicbricks", "housing", "nobroker", "commonfloor",
                     "makaan", "proptiger", "square yards", "nestaway", "zolo"],
}


def clean_merchant(merchant: str) -> str:
    merchant = merchant.lower()
    merchant = re.sub(r"[^a-z0-9\s]", "", merchant)
    return merchant


def classify_merchant(merchant: str) -> str:
    
    merchant = clean_merchant(merchant)
    best_category, best_score = "Unknown", 0

    for category, keywords in CATEGORY_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in merchant:
                word_count = len(keyword.split())
                score += word_count ** 2
        if score > best_score:
            best_score, best_category = score, category

    return best_category

def classify_transactions(df):

    result = df.copy()

    result["Predicted_Category"] = (
        result["Merchant"].apply(classify_merchant)
    )

    return result

def evaluate_on_real_data(raw_path: str, labeled_path: str) -> pd.DataFrame:
    
    raw_df = pd.read_csv(raw_path)
    raw_df["Predicted_Category"] = raw_df["Merchant"].apply(classify_merchant)

    ground_truth = pd.read_csv(labeled_path)
    merged = ground_truth.merge(
        raw_df[["Transaction_ID", "Predicted_Category"]],
        on="Transaction_ID", how="inner", validate="one_to_one",
    )
    assert len(merged) == len(ground_truth), (
        "Row count changed after merge -- Transaction_IDs don't fully "
        "match between raw and labeled files."
    )
    merged["Correct"] = merged["Category"] == merged["Predicted_Category"]
    return merged


SUFFIXES = [" Ltd", " Pvt Ltd", " India Pvt Ltd", " Limited", ".com", " Store"]
PREFIXES = ["POS ", "IN*", "PAYTM*", "UPI-", "NEFT-"]


def _make_noisy_variant(merchant: str) -> str:
    """Applies one realistic bank-statement noise pattern to a merchant name."""
    choice = random.random()
    if choice < 0.35:
        return merchant + random.choice(SUFFIXES)
    elif choice < 0.60:
        return random.choice(PREFIXES) + merchant
    elif choice < 0.75:
        return merchant.upper()
    elif choice < 0.85:
        return merchant[: max(4, len(merchant) - random.randint(1, 4))]  # truncation
    else:
        return merchant  # unchanged control


def evaluate_on_noisy_holdout(labeled_path: str, seed: int = 42) -> pd.DataFrame:
   
    random.seed(seed)
    clean = pd.read_csv(labeled_path)
    merchant_categories = dict(zip(clean.Merchant, clean.Category))

    rows = []
    for merchant, category in merchant_categories.items():
        variant = _make_noisy_variant(merchant)
        rows.append({
            "Original_Merchant": merchant,
            "Merchant": variant,
            "True_Category": category,
        })

    holdout = pd.DataFrame(rows)
    holdout["Predicted_Category"] = holdout["Merchant"].apply(classify_merchant)
    holdout["Correct"] = holdout["Predicted_Category"] == holdout["True_Category"]
    return holdout


if __name__ == "__main__":
    real_data = evaluate_on_real_data("data/Raw transactions.csv", "data/transactions.csv")
    real_accuracy = real_data["Correct"].mean() * 100
    print(f"Accuracy on training data (sanity check): {real_accuracy:.2f}%")

    holdout = evaluate_on_noisy_holdout("data/transactions.csv")
    holdout_accuracy = holdout["Correct"].mean() * 100
    print(f"Held-out accuracy on {len(holdout)} noisy merchant variants: {holdout_accuracy:.2f}%\n")

    wrong = holdout[~holdout["Correct"]]
    print(f"{len(wrong)} incorrect on held-out set:\n")
    print(wrong[["Original_Merchant", "Merchant", "True_Category", "Predicted_Category"]].to_string(index=False))

    real_data.to_csv("data/classified_output.csv", index=False)
    holdout.to_csv("data/holdout_results.csv", index=False)
    print("\nResults saved to data/classified_output.csv and data/holdout_results.csv")
    test_df = pd.read_csv("data/Raw transactions.csv")

    classified_df = classify_transactions(test_df)

    print("\nCLASSIFIED TRANSACTIONS:\n")
    print(
        classified_df[
            ["Merchant", "Predicted_Category"]
        ].head(10)
    )