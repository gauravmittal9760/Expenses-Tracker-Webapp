import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor

from .feature_engineering import create_daily_dataset


def _prepare_features(daily):
    """
    Create time-series features from daily expense data.

    Features:
    - day number
    - day of week
    - day of month
    - month
    - rolling 3-day average
    - rolling 7-day average
    - previous day's spending
    """

    df = daily.copy()

    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values("date").reset_index(
        drop=True
    )

    df["day_number"] = np.arange(
        len(df)
    )

    df["day_of_week"] = (
        df["date"].dt.dayofweek
    )

    df["day_of_month"] = (
        df["date"].dt.day
    )

    df["month"] = (
        df["date"].dt.month
    )

    df["previous_day"] = (
        df["amount"]
        .shift(1)
        .fillna(df["amount"].median())
    )

    df["rolling_3_day"] = (
        df["amount"]
        .rolling(
            window=3,
            min_periods=1
        )
        .mean()
    )

    df["rolling_7_day"] = (
        df["amount"]
        .rolling(
            window=7,
            min_periods=1
        )
        .mean()
    )

    return df


def predict_future_spending(
    expenses,
    future_days=30
):
    """
    Predict future spending using a Random Forest
    regression model with time-based spending features.

    Returns the same response structure expected
    by app.py.
    """

    daily = create_daily_dataset(
        expenses
    )

    # ------------------------------------------
    # Minimum data requirement
    # ------------------------------------------

    if len(daily) < 14:

        return {
            "success": False,
            "predicted_total": 0.0,
            "daily_predictions": [],
            "message": (
                "Not enough historical data for "
                "ML forecasting. At least 14 "
                "days of expense history are "
                "recommended."
            )
        }

    # ------------------------------------------
    # Feature engineering
    # ------------------------------------------

    df = _prepare_features(
        daily
    )

    feature_columns = [
        "day_number",
        "day_of_week",
        "day_of_month",
        "month",
        "previous_day",
        "rolling_3_day",
        "rolling_7_day"
    ]

    X = df[feature_columns]
    y = df["amount"]

    # ------------------------------------------
    # Random Forest model
    # ------------------------------------------

    model = RandomForestRegressor(
        n_estimators=250,
        max_depth=10,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )

    model.fit(
        X,
        y
    )

    # ------------------------------------------
    # Create future dates
    # ------------------------------------------

    last_date = pd.to_datetime(
        df["date"].iloc[-1]
    )

    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=future_days,
        freq="D"
    )

    # ------------------------------------------
    # Generate future predictions
    # ------------------------------------------

    predictions = []

    historical_amounts = (
        df["amount"]
        .tolist()
    )

    for index, future_date in enumerate(
        future_dates
    ):

        day_number = (
            len(df) + index
        )

        day_of_week = (
            future_date.dayofweek
        )

        day_of_month = (
            future_date.day
        )

        month = (
            future_date.month
        )

        # --------------------------------------
        # Previous day spending
        # --------------------------------------

        previous_day = (
            historical_amounts[-1]
            if historical_amounts
            else float(y.median())
        )

        # --------------------------------------
        # Rolling averages
        # --------------------------------------

        recent_3 = (
            historical_amounts[-3:]
            if historical_amounts
            else [float(y.median())]
        )

        recent_7 = (
            historical_amounts[-7:]
            if historical_amounts
            else [float(y.median())]
        )

        rolling_3_day = float(
            np.mean(recent_3)
        )

        rolling_7_day = float(
            np.mean(recent_7)
        )

        future_row = pd.DataFrame(
            [[
                day_number,
                day_of_week,
                day_of_month,
                month,
                previous_day,
                rolling_3_day,
                rolling_7_day
            ]],
            columns=feature_columns
        )

        prediction = model.predict(
            future_row
        )[0]

        prediction = max(
            float(prediction),
            0.0
        )

        predictions.append(
            prediction
        )

        # Add prediction so that the next
        # future day can use it as previous
        # spending.
        historical_amounts.append(
            prediction
        )

    # ------------------------------------------
    # Total predicted spending
    # ------------------------------------------

    predicted_total = float(
        sum(predictions)
    )

    # ------------------------------------------
    # Return result
    # ------------------------------------------

    return {
        "success": True,

        "predicted_total": round(
            predicted_total,
            2
        ),

        "daily_predictions": [
            round(
                float(value),
                2
            )
            for value in predictions
        ],

        "forecast_days": future_days,

        "model": (
            "Random Forest Regression"
        ),

        "features": feature_columns
    }