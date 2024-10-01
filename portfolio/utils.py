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

import json
import zlib
from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def create_dividend_report(dividend_calculation):
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    flowables = []

    # Add title
    title = Paragraph("Dividend Calculation Report", styles['Title'])
    flowables.append(title)

    # Add details from DividendCalculation model
    details = [
        f"Ticket Name: {dividend_calculation.ticket_name}",
        f"Capital: {dividend_calculation.capital}",
        f"Lookback Period: {dividend_calculation.lookback_period}",
        f"Calculation Period: {dividend_calculation.calculation_period}",
        f"Created At: {dividend_calculation.created_at.strftime('%B %d, %Y, %I:%M %p')}",
    ]

    for detail in details:
        flowables.append(Paragraph(detail, styles['Normal']))

    # Extract results data
    results = dividend_calculation.get_results()
    table_data = [["Date", "Yield", "Return on Capital"]]

    for key, date in results['date'].items():
        yield_value = results['avg_div'][key]
        return_on_capital = results['dividends_return'][key]
        table_data.append([date, f"{yield_value:.2%}", f"${return_on_capital:.2f}"])

    # Create the table
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    flowables.append(table)

    # Build the PDF
    pdf.build(flowables)
    buffer.seek(0)  # Move to the beginning of the buffer
    return buffer