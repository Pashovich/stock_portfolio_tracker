import yfinance as yf
import requests

from django.conf import settings
from pandas import DataFrame
from typing import Optional
from datetime import date

BASE_URL = "https://api.polygon.io/v3/"
class FinanceApi:

    @staticmethod
    def ticker_exists(ticker_name: str) -> bool:
        stock = yf.Ticker(ticker_name)
        return True if stock.info.get("symbol", False) else False

    @staticmethod
    def get_stock_price(ticker_name: str) -> Optional[float]:
        """Get stock price with assumption that ticket exists."""
        stock = yf.Ticker(ticker_name)
        hist: DataFrame = stock.history(period="1d")
        if not hist.empty:
            return round(hist.iloc[-1]["Close"],3)

        recent_data: DataFrame = yf.download(ticker_name, period="5d")
        if not recent_data.empty:
            return round(recent_data.iloc[-1]["Close"],3)

        return None
    
    @staticmethod
    def get_upcoming_dividends(ticker_name: str)-> list[dict]:
        today = date.today().__str__()
        POLYGON_API_KEY = settings.POLYGON_API_KEY 
        response = requests.get(
            BASE_URL + f'reference/dividends?ticker={ticker_name}' + '&limit=10'+f'&pay_date.gt={today}'+ f'&apiKey={POLYGON_API_KEY}'
        )
        if response.ok:
            return response.json()['results']
        else:
            return []
                
    @staticmethod
    def get_all_dividends(ticker_name: str)-> DataFrame:
        stock = yf.Ticker(ticker_name)
        return stock.dividends

