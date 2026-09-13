from collections import defaultdict
from statistics import mean, median
from datetime import datetime


def _safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _get_expense_data(expenses):
    data = []

    for expense in expenses:
        amount = _safe_float(
            getattr(expense, "amount", 0)
        )

        category = (
            getattr(expense, "category", None)
            or "Other"
        )

        date_value = getattr(
            expense,
            "date",
            None
        )

        try:
            if hasattr(date_value, "date"):
                date_value = date_value.date()

            if isinstance(date_value, str):
                date_value = datetime.fromisoformat(
                    date_value
                ).date()

        except (ValueError, TypeError):
            date_value = None

        data.append({
            "amount": amount,
            "category": category,
            "date": date_value
        })

    return data


def _calculate_category_patterns(data):
    totals = defaultdict(float)

    for item in data:
        totals[item["category"]] += item["amount"]

    return dict(totals)


def _calculate_recent_pattern(data):
    dated = [
        item for item in data
        if item["date"] is not None
    ]

    if len(dated) < 2:
        return None

    dated.sort(
        key=lambda item: item["date"]
    )

    unique_dates = sorted(
        set(item["date"] for item in dated)
    )

    if len(unique_dates) < 2:
        return None

    midpoint = len(unique_dates) // 2

    first_period = set(
        unique_dates[:midpoint]
    )

    second_period = set(
        unique_dates[midpoint:]
    )

    first_amounts = [
        item["amount"]
        for item in dated
        if item["date"] in first_period
    ]

    second_amounts = [
        item["amount"]
        for item in dated
        if item["date"] in second_period
    ]

    if not first_amounts or not second_amounts:
        return None

    first_total = sum(first_amounts)
    second_total = sum(second_amounts)

    if first_total == 0:
        return None

    change_percent = (
        (second_total - first_total)
        / first_total
    ) * 100

    return {
        "first_total": first_total,
        "second_total": second_total,
        "change_percent": change_percent
    }


def _build_recommendations(
    data,
    category_totals,
    forecast,
    anomalies,
    budget,
    income
):
    recommendations = []

    total = sum(
        item["amount"]
        for item in data
    )

    # ------------------------------------------
    # Category-based recommendation
    # ------------------------------------------

    if category_totals and total > 0:

        highest_category = max(
            category_totals,
            key=category_totals.get
        )

        highest_amount = (
            category_totals[highest_category]
        )

        share = (
            highest_amount / total
        ) * 100

        if share >= 30:

            recommendations.append(
                f"Your {highest_category} category "
                f"accounts for about {share:.1f}% "
                f"of recorded spending. Review recent "
                f"expenses in this category and identify "
                f"which purchases can be reduced or planned "
                f"in advance."
            )

        else:

            recommendations.append(
                f"{highest_category} is currently your "
                f"largest spending category. Keep tracking "
                f"this category closely because changes "
                f"here will have the biggest effect on your "
                f"overall spending."
            )

    # ------------------------------------------
    # Spending trend recommendation
    # ------------------------------------------

    trend = _calculate_recent_pattern(data)

    if trend:

        change = trend["change_percent"]

        if change > 10:

            recommendations.append(
                f"Your spending in the more recent part "
                f"of the recorded period is approximately "
                f"{change:.1f}% higher than the earlier "
                f"period. Consider reviewing recent "
                f"purchases before increasing discretionary "
                f"spending."
            )

        elif change < -10:

            recommendations.append(
                f"Your recent spending is approximately "
                f"{abs(change):.1f}% lower than the earlier "
                f"recorded period. Continue the habits that "
                f"are contributing to this improvement."
            )

        else:

            recommendations.append(
                "Your spending pattern is relatively "
                "stable across the recorded period. "
                "Continue monitoring category-wise "
                "spending to maintain this consistency."
            )

    # ------------------------------------------
    # ML forecast recommendation
    # ------------------------------------------

    if forecast.get("success"):

        predicted = _safe_float(
            forecast.get(
                "predicted_total",
                0
            )
        )

        if budget is not None:

            budget_value = _safe_float(
                budget
            )

            if budget_value > 0:

                difference = (
                    predicted - budget_value
                )

                if difference > 0:

                    recommendations.append(
                        f"The ML model forecasts around "
                        f"₹{predicted:.2f} of spending for "
                        f"the next 30 days, which is about "
                        f"₹{difference:.2f} above your "
                        f"recorded monthly budget. Consider "
                        f"planning upcoming discretionary "
                        f"expenses carefully."
                    )

                else:

                    recommendations.append(
                        f"The ML forecast is approximately "
                        f"₹{predicted:.2f} for the next "
                        f"30 days, currently below your "
                        f"₹{budget_value:.2f} budget."
                    )

        else:

            recommendations.append(
                f"The ML model forecasts approximately "
                f"₹{predicted:.2f} of spending over the "
                f"next 30 days. Use this forecast as a "
                f"planning reference and continue recording "
                f"expenses."
            )

    # ------------------------------------------
    # Anomaly recommendation
    # ------------------------------------------

    if anomalies:

        recommendations.append(
            f"The ML anomaly detector identified "
            f"{len(anomalies)} unusual transaction"
            f"{'s' if len(anomalies) != 1 else ''}. "
            f"Review these transactions to determine "
            f"whether they were exceptional purchases "
            f"or indicate a new spending pattern."
        )

    # ------------------------------------------
    # Keep recommendations concise
    # ------------------------------------------

    unique = []

    for recommendation in recommendations:

        if recommendation not in unique:
            unique.append(recommendation)

    return unique[:3]


def generate_financial_recommendation(
    user,
    expenses,
    forecast,
    anomalies
):
    """
    Free local AI/ML recommendation engine.

    No OpenAI API.
    No API key.
    No external AI model.
    No paid service.

    Recommendations are generated from the user's
    actual financial data and ML results.
    """

    data = _get_expense_data(
        expenses
    )

    if not data:

        return (
            "There is not enough expense data yet "
            "to generate personalized financial insights."
        )

    total_spending = sum(
        item["amount"]
        for item in data
    )

    amounts = [
        item["amount"]
        for item in data
    ]

    category_totals = (
        _calculate_category_patterns(data)
    )

    budget = getattr(
        user,
        "budget",
        None
    )

    income = getattr(
        user,
        "income",
        None
    )

    recommendations = _build_recommendations(
        data=data,
        category_totals=category_totals,
        forecast=forecast,
        anomalies=anomalies,
        budget=budget,
        income=income
    )

    # ------------------------------------------
    # Key spending pattern
    # ------------------------------------------

    highest_category = max(
        category_totals,
        key=category_totals.get
    )

    highest_amount = (
        category_totals[highest_category]
    )

    category_percentage = (
        highest_amount / total_spending
    ) * 100 if total_spending else 0

    trend = _calculate_recent_pattern(
        data
    )

    if trend:

        change = trend["change_percent"]

        if change > 10:
            trend_text = (
                f"Recent spending is approximately "
                f"{change:.1f}% higher than the earlier "
                f"recorded period."
            )

        elif change < -10:
            trend_text = (
                f"Recent spending is approximately "
                f"{abs(change):.1f}% lower than the earlier "
                f"recorded period."
            )

        else:
            trend_text = (
                "Recent spending is relatively stable "
                "compared with the earlier recorded period."
            )

    else:

        trend_text = (
            "There is not enough date history to "
            "determine a reliable spending trend."
        )

    # ------------------------------------------
    # ML forecast
    # ------------------------------------------

    if forecast.get("success"):

        predicted = _safe_float(
            forecast.get(
                "predicted_total",
                0
            )
        )

        forecast_text = (
            f"ML predicts approximately "
            f"₹{predicted:.2f} spending over "
            f"the next 30 days."
        )

    else:

        forecast_text = (
            "ML forecasting needs more historical "
            "expense data."
        )

    # ------------------------------------------
    # Unusual spending
    # ------------------------------------------

    if anomalies:

        anomaly_text = (
            f"Machine learning detected "
            f"{len(anomalies)} unusual transaction"
            f"{'s' if len(anomalies) != 1 else ''}."
        )

    else:

        anomaly_text = (
            "No unusual transactions were detected "
            "by the ML anomaly detector."
        )

    # ------------------------------------------
    # Final personalized insight
    # ------------------------------------------

    result = []

    result.append(
        "### Key Spending Pattern"
    )

    result.append(
        f"{highest_category} is currently your "
        f"largest spending category at "
        f"₹{highest_amount:.2f}, representing "
        f"approximately {category_percentage:.1f}% "
        f"of recorded spending."
    )

    result.append(
        trend_text
    )

    result.append(
        ""
    )

    result.append(
        "### ML Forecast"
    )

    result.append(
        forecast_text
    )

    result.append(
        ""
    )

    result.append(
        "### Unusual Spending"
    )

    result.append(
        anomaly_text
    )

    result.append(
        ""
    )

    result.append(
        "### Recommendations"
    )

    if recommendations:

        for index, recommendation in enumerate(
            recommendations,
            start=1
        ):

            result.append(
                f"{index}. {recommendation}"
            )

    else:

        result.append(
            "Continue recording expenses to generate "
            "more personalized recommendations."
        )

    return "\n".join(result)