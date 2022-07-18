import pandas as pd
from re import sub
from decimal import Decimal
from datetime import datetime
import requests


def free_checking_table():
    free_checking = pd.read_csv("../free_checking.csv").fillna("")
    df = free_checking.drop(["ID"], axis=1)
    table = df.to_dict("split")
    columns = table["columns"]
    data = table["data"]
    return columns, data


def credit_card_table():
    free_checking = pd.read_csv("../credit_card.csv").fillna("")
    df = free_checking.drop(["ID"], axis=1)
    table = df.to_dict("split")
    columns = table["columns"]
    data = table["data"]
    return columns, data


def credit_card():
    credit_card = pd.read_csv("../credit_card.csv")
    raw_dates = credit_card["DATE"].tolist()[::-1]
    clean_dates = [datetime.strptime(date.strip(), "%m/%d/%Y") for date in raw_dates]
    expenses = [
        float(sub(r"[^\d.]", "", expense)) for expense in credit_card["AMOUNT"].tolist()
    ][::-1]
    return clean_dates, expenses


def free_checking():
    free_checking = pd.read_csv("../free_checking.csv")
    withdrawals_data = (
        free_checking.apply(extract_withdrawals, axis=1).dropna().to_list()
    )
    withdrawals_df = pd.DataFrame(
        withdrawals_data, columns=["Date", "Description", "Amount", "Current Balance"]
    )
    raw_dates = free_checking["DATE"].tolist()[::-1]
    clean_dates = [datetime.strptime(date.strip(), "%m/%d/%Y") for date in raw_dates]
    values = [
        float(sub(r"[^\d.]", "", account_balance))
        for account_balance in free_checking["CURRENT BALANCE"].tolist()
    ][::-1]
    return clean_dates, values


def extract_withdrawals(row):
    if "withdrawal" and "middlesex" in row["DESCRIPTION"].lower():
        data = (row["DATE"], row["DESCRIPTION"], row["AMOUNT"], row["CURRENT BALANCE"])
        return data
    elif "withdrawal" and "coliseum" in row["DESCRIPTION"].lower():
        data = (row["DATE"], row["DESCRIPTION"], row["AMOUNT"], row["CURRENT BALANCE"])
        return data
    elif "withdrawal-cash" in row["DESCRIPTION"].lower():
        data = (row["DATE"], row["DESCRIPTION"], row["AMOUNT"], row["CURRENT BALANCE"])
        return data


if __name__ == "__main__":

    free_checking_table()
