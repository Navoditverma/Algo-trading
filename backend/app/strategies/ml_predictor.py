# backend/app/strategies/ml_predictor.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os
def ml_predictor_strategy(df: pd.DataFrame, model_file: str = "model.pkl"):
    """
    Machine Learning-based Strategy using Random Forest
    - Train a model to predict whether the price will go up or down
    - Buy if model predicts price will go up, sell if down
    """

    # Feature engineering: We are using previous day's close and change as features
    df['previous_close'] = df['close'].shift(1)
    df['price_change'] = df['close'] - df['previous_close']

    # Remove NaN values
    df = df.dropna()

    # Define features and target
    X = df[['previous_close', 'price_change']]  # Use previous close and price change
    y = (df['price_change'] > 0).astype(int)  # 1 if price goes up, 0 if down

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Train the model (or load pre-trained model)
    if os.path.exists(model_file):
        model = joblib.load(model_file)
    else:
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X_train, y_train)
        joblib.dump(model, model_file)

    # Predict on the test set
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    # Generate signals based on predictions
    df['signal'] = model.predict(X[['previous_close', 'price_change']])
    df['position'] = df['signal'].diff()

    return df, accuracy
