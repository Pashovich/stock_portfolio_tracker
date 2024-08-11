from typing import Any
from django import forms
from .models import Portfolio, Share
from django.forms import modelformset_factory
from .finance_api import FinanceApi
from datetime import date
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz
import pandas as pd


types_ = {
    "y": {"years": None},
    "m": {"months": None},
}


class DividendPortfolioForm(forms.Form):
    CHOICES = [
        ("2y", "2y"),
        ("1y", "1y"),
        ("6m", "6m"),
    ]
    ticker_name = forms.CharField(max_length=100, required=True)
    capital = forms.IntegerField(min_value=1, required=True)
    period = forms.ChoiceField(choices=CHOICES, required=True)

    def clean_ticker_name(self):
        ticker_name = self.cleaned_data.get("ticker_name")
        if not FinanceApi.ticker_exists(ticker_name):
            self.add_error("ticker_name", "Invalid ticket name")
        return ticker_name

    def calculate_dividends_return(self, lookback_period = 365*5) -> pd.DataFrame:
        ticker_name: str = self.cleaned_data.get("ticker_name")
        capital: int = self.cleaned_data.get("capital")
        period: str = self.cleaned_data.get("period")

        dividends = FinanceApi.get_upcoming_dividends(ticker_name)

        tz = pytz.UTC

        if "y" in period:
            forecast_period = 12 * int(period.replace('y',''))
        elif 'm' in period:
            forecast_period = int(period.replace('m',''))

        dividends.index = dividends.index.tz_localize(None)
        dividends = dividends.loc[dividends.index >= pd.Timestamp.now() - pd.Timedelta(days = lookback_period)]
        dividends_by_month = dividends.groupby(dividends.index.month).mean()
        today = pd.Timestamp.now()
        forecast = []
        for i in range(forecast_period):
            future_date = today + pd.DateOffset(months=i)
            month_year = future_date.strftime("%B %Y")
            approximate_dividend = dividends_by_month.get(future_date.month, 0)
            forecast.append((month_year, approximate_dividend))

        df = pd.DataFrame(forecast, columns=["date", "avg_div"])
        df = df[df['avg_div'] > 0]

        stock_price = FinanceApi.get_stock_price(ticker_name)

        shares = int(capital / stock_price)
        df['dividends_return'] = df['avg_div'] * shares
        return df


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ["name"]


class ShareForm(forms.ModelForm):
    date_of_purchase = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Share
        fields = ["name", "price", "qty", "date_of_purchase"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        price = cleaned_data.get("price")
        qty = cleaned_data.get("qty")
        date_of_purchase = cleaned_data.get("date_of_purchase")

        if price and qty and date_of_purchase:
            if price <= 0:
                self.add_error("price", "Price must be positive.")
            if qty <= 0:
                self.add_error("qty", "Quantity must be positive.")

        if date_of_purchase and date_of_purchase > date.today():
            self.add_error(
                "date_of_purchase", "Date of purchase cannot be in the future."
            )

        if not FinanceApi.ticker_exists(name):
            self.add_error("name", "Invalid ticket name")

        return cleaned_data
