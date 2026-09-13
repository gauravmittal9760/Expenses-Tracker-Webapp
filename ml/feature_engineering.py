import pandas as pd


def expenses_to_dataframe(expenses):
    data = []

    for expense in expenses:
        data.append({
            "date": expense.date,
            "amount": float(expense.amount),
            "category": expense.category
        })

    if not data:
        return pd.DataFrame(columns=["date", "amount", "category"])

    df = pd.DataFrame(data)

    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values("date")

    return df


def create_daily_dataset(expenses):
    df = expenses_to_dataframe(expenses)

    if df.empty:
        return df

    daily = (
        df.groupby("date")["amount"]
        .sum()
        .reset_index()
    )

    return daily