import requests
from django.core.cache import cache
from .models import Share
from .finance_api import FinanceApi

def get_upcomming_dividends(share: Share) -> float:
    key = f"{share.name}:upcomming_dividends"
    dividends = cache.get(key)
    if dividends is None:
        dividends = FinanceApi.get_upcoming_dividends(share.name)
        cache.set(key, dividends, timeout=60 * 30)
    return dividends

def get_current_price(share: Share) -> float:
    key = f"{share.name}:current_price"
    current_price = cache.get(key)
    if not current_price:
        current_price = FinanceApi.get_stock_price(share.name)
        cache.set(key, current_price, timeout=120)
    return current_price