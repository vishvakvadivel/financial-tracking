from newsapi import NewsApiClient

api_key = "f4737c1f9d6f46d79f41a359acfa61c0"
newsapi = NewsApiClient(api_key=api_key)
from pandas.io.json import json_normalize
import pandas as pd


def top_headlines():
    top_headlines = newsapi.get_top_headlines(
        category="general", language="en", country="us"
    )
    top_headlines = json_normalize(top_headlines["articles"])
    newdf = top_headlines[["title", "url"]]
    news_dict = newdf.set_index("title")["url"].to_dict()
    return news_dict


if __name__ == "__main__":
    top_headlines()
