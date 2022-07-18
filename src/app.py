from fastapi import FastAPI, Request
from pydantic import BaseModel, AnyUrl
from typing import Sequence
from datetime import datetime
from categorize_data import (
    free_checking,
    credit_card,
    free_checking_table,
    credit_card_table,
)
from fastapi.middleware.cors import CORSMiddleware
from news import top_headlines

app = FastAPI()

origins = ["http://localhost:3000", "localhost:3000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class FreeChecking(BaseModel):
    dates: Sequence[datetime]
    account_value: Sequence[float]


class CreditCard(BaseModel):
    dates: Sequence[datetime]
    expenses: Sequence[float]


class Table(BaseModel):
    columns: Sequence[str]
    data: Sequence[list]


class NewsHeadlines(BaseModel):
    data: Sequence[dict]


@app.get("/api/financial-tracking/describe-free-checking", response_model=FreeChecking)
async def describe_free_checking():
    dates, values = free_checking()
    return FreeChecking(**{"dates": dates, "account_value": values})


@app.get("/api/financial-tracking/get-credit-expenses", response_model=CreditCard)
async def credit_expenses():
    dates, expenses = credit_card()
    return CreditCard(**{"dates": dates, "expenses": expenses})


@app.get("/api/financial-tracking/get-free-checking-table", response_model=Table)
async def credit_expenses():
    columns, data = free_checking_table()
    return Table(**{"columns": columns, "data": data})


@app.get("/api/financial-tracking/get-credit-card-table", response_model=Table)
async def credit_expenses():
    columns, data = credit_card_table()
    return Table(**{"columns": columns, "data": data})


@app.get("/api/financial-tracking/get-news", response_model=NewsHeadlines)
async def get_news():
    return NewsHeadlines(
        **{
            "data": [
                {"headline": headline, "url": url}
                for headline, url in top_headlines().items()
            ],
        }
    )
