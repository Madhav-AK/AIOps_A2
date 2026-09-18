import argparse
import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/spam_dataset.csv")
    parser.add_argument("--out", default="data/model.joblib")
    args = parser.parse_args()

    df = pd.read_csv(args.data)
    X = df["text"]
    y = df["label"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    f1 = f1_score(y_test, preds, pos_label="spam")
    print(f"accuracy={acc:.4f}  f1={f1:.4f}")

    joblib.dump({"model": model, "feature_columns": ["text"]}, args.out)
    print(f"Saved model bundle to {args.out}")


if __name__ == "__main__":
    main()