from django.urls import path
from .views import (
    PortfolioListView,
    PortfolioCreateView,
    PortfolioDetailView,
    PortfolioDeleteUpdateView,
    PortfolioDeleteView,
    DividendPortfolioView
)

urlpatterns = [
    path("", PortfolioListView.as_view(), name="portfolio_list"),
    path('create/', PortfolioCreateView.as_view(), name='portfolio_create'),
    path('edit/<int:pk>/', PortfolioDeleteUpdateView.as_view(), name='portfolio_edit'),
    path('<int:pk>/delete/', PortfolioDeleteView.as_view(), name='portfolio_delete'),
    path('<int:pk>/', PortfolioDetailView.as_view(), name='portfolio_detail'),
    # path('dividend_calculator/', DividendPortfolioView.as_view(), name='portfolio_create'),
]
