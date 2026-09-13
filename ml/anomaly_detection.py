import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import OrdinalEncoder


def _prepare_features(expenses):
    """
    Convert expense records into ML features.

    Features:
    - amount
    - day of week
    - day of month
    - month
    - category
    """

    rows = []

    for expense in expenses:

        amount = float(
            expense.amount or 0
        )

        date_value = pd.to_datetime(
            expense.date,
            errors="coerce"
        )

        category = (
            expense.category
            or "Other"
        )

        rows.append({
            "amount": amount,
            "day_of_week": (
                date_value.dayofweek
                if not pd.isna(date_value)
                else 0
            ),
            "day_of_month": (
                date_value.day
                if not pd.isna(date_value)
                else 1
            ),
            "month": (
                date_value.month
                if not pd.isna(date_value)
                else 1
            ),
            "category": category
        })

    return pd.DataFrame(rows)


def detect_anomalies(expenses):
    """
    Detect unusual transactions using Isolation Forest.

    The model considers transaction amount, category and
    date-related behaviour instead of amount alone.
    """

    # ------------------------------------------
    # Minimum data requirement
    # ------------------------------------------

    if len(expenses) < 10:

        return {
            "success": False,
            "anomalies": [],
            "count": 0,
            "message": (
                "Not enough expenses for anomaly "
                "detection. At least 10 transactions "
                "are recommended."
            )
        }

    # ------------------------------------------
    # Prepare ML dataset
    # ------------------------------------------

    df = _prepare_features(
        expenses
    )

    if df.empty:

        return {
            "success": False,
            "anomalies": [],
            "count": 0,
            "message": (
                "No valid expense data available "
                "for anomaly detection."
            )
        }

    # ------------------------------------------
    # Encode categories
    # ------------------------------------------

    encoder = OrdinalEncoder(
        handle_unknown="use_encoded_value",
        unknown_value=-1
    )

    category_encoded = encoder.fit_transform(
        df[["category"]]
    )

    df["category_encoded"] = (
        category_encoded[:, 0]
    )

    # ------------------------------------------
    # ML features
    # ------------------------------------------

    feature_columns = [
        "amount",
        "day_of_week",
        "day_of_month",
        "month",
        "category_encoded"
    ]

    X = df[
        feature_columns
    ]

    # ------------------------------------------
    # Isolation Forest
    # ------------------------------------------

    model = IsolationForest(
        n_estimators=200,
        contamination="auto",
        random_state=42,
        n_jobs=-1
    )

    predictions = model.fit_predict(
        X
    )

    anomaly_scores = model.decision_function(
        X
    )

    # ------------------------------------------
    # Build anomaly results
    # ------------------------------------------

    anomalies = []

    for (
        expense,
        prediction,
        score
    ) in zip(
        expenses,
        predictions,
        anomaly_scores
    ):

        if prediction == -1:

            anomalies.append({

                "id": expense.id,

                "category": (
                    expense.category
                    or "Other"
                ),

                "amount": round(
                    float(expense.amount or 0),
                    2
                ),

                "date": str(
                    expense.date
                ),

                "description": (
                    expense.description
                    or ""
                ),

                "anomaly_score": round(
                    float(score),
                    4
                )
            })

    # ------------------------------------------
    # Sort most unusual first
    # ------------------------------------------

    anomalies.sort(
        key=lambda item: item[
            "anomaly_score"
        ]
    )

    # ------------------------------------------
    # Return result
    # ------------------------------------------

    return {

        "success": True,

        "anomalies": anomalies,

        "count": len(anomalies),

        "model": (
            "Isolation Forest"
        ),

        "features": feature_columns
    }