import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
import joblib
from urllib.parse import urlparse
import re

def tokenize_url(url: str) -> list[str]:
    parsed = urlparse(url)
    tokens: list[str] = []
    # Domain/netloc
    if parsed.netloc:
        tokens.extend([t for t in parsed.netloc.lower().split('.') if t])
    # Path tokens
    path = parsed.path or ""
    for part in path.lower().split('/'):
        if not part:
            continue
        for sub in re.split(r"[-_]+", part):
            if sub:
                tokens.append(sub)
    # Query tokens
    if parsed.query:
        tokens.append("has_query")
        for q in parsed.query.lower().split('&'):
            k = q.split('=')[0]
            if k:
                tokens.append(f"q_{k}")
    return tokens


def get_url_features(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    query = parsed_url.query

    features = {
        "path_depth": path.count('/') or 0,
        "path_length": len(path) or 0,
        "query_params": len(query.split('&')) if query else 0,
        "has_html_extension": 1 if path.endswith(".html") else 0,
        "has_php_extension": 1 if path.endswith(".php") else 0,
    }

    numeric_tokens = [f"{k}_{v}" for k, v in features.items()]
    text_tokens = tokenize_url(url)
    return " ".join(numeric_tokens + text_tokens)

def train_model():
    """
    Trains a model to classify wine URLs.
    """
    # Load the labeled data
    try:
        df = pd.read_csv('labeled_data.csv')
    except FileNotFoundError:
        print("Error: labeled_data.csv not found. Please run label_data.py first.")
        return

    # Feature Engineering
    df['features'] = df['url'].apply(get_url_features)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        df['features'], 
        df['label'], 
        test_size=0.2, 
        random_state=42
    )

    # Create a pipeline with a TfidfVectorizer and a Logistic Regression classifier
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', LogisticRegression(class_weight='balanced')),
    ])

    # Train the model
    print("Training the model...")
    pipeline.fit(X_train, y_train)
    print("Model training complete.")

    # Evaluate the model
    y_pred = pipeline.predict(X_test)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Save the trained model
    joblib.dump(pipeline, 'wine_url_classifier.joblib')
    print("\nModel saved to wine_url_classifier.joblib")

if __name__ == '__main__':
    train_model()
