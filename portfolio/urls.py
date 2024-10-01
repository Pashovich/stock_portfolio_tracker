from django.urls import path
from .views import (
    PortfolioListView,
    PortfolioCreateView,
    PortfolioDetailView,
    PortfolioDeleteUpdateView,
    PortfolioDeleteView,
    DividendCalculatorView,
    DividendCalculatorListView,
    DividendCalculatorReportView,
    ReportDeleteView,
    DividendReportDownload,
    ForbiddenForNonPaid
)

urlpatterns = [
    path("", PortfolioListView.as_view(), name="portfolio_list"),
    path('create/', PortfolioCreateView.as_view(), name='portfolio_create'),
    path('edit/<int:pk>/', PortfolioDeleteUpdateView.as_view(), name='portfolio_edit'),
    path('<int:pk>/delete/', PortfolioDeleteView.as_view(), name='portfolio_delete'),
    path('<int:pk>/', PortfolioDetailView.as_view(), name='portfolio_detail'),
    path('dividend_calculator/create', DividendCalculatorView.as_view(), name='portfolio_calculator'),
    path('dividend_calculator/view_list/', DividendCalculatorListView.as_view(), name='portfolio_calculator_list_view'),
    path('dividend_calculator/download/<int:pk>', DividendReportDownload.as_view(), name='dividend_report_download'),
    path('dividend_calculator/view/<int:pk>', DividendCalculatorReportView.as_view(), name='portfolio_calculator_detailt_view'),
    path('dividend_calculator/delete/<int:pk>', ReportDeleteView.as_view(), name='report_delete'),
    path('non-paid-403/', ForbiddenForNonPaid.as_view(), name='non_paid_403')
]
