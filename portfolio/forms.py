from django import forms
from .models import Portfolio, Share
from django.forms import modelformset_factory
from .finance_api import FinanceApi
from datetime import date

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
        name = cleaned_data.get('name')
        price = cleaned_data.get('price')
        qty = cleaned_data.get('qty')
        date_of_purchase = cleaned_data.get('date_of_purchase')

        if price and qty and date_of_purchase:
            if price <= 0:
                self.add_error('price', 'Price must be positive.')
            if qty <= 0:
                self.add_error('qty', 'Quantity must be positive.')

        if date_of_purchase and date_of_purchase > date.today():
            self.add_error('date_of_purchase', "Date of purchase cannot be in the future.")

        if not FinanceApi.ticker_exists(name):
            self.add_error('name', "Invalid ticket name")

        return cleaned_data
