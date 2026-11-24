import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import requests


def get_stock_data(symbol: str):
    stock = yf.Ticker(symbol)

    # Retrieve the most recent 5 trading days
    history = stock.history(period="5d")

    if len(history) < 2:
        return None

    # Extract the two most recent closing prices
    current = float(history["Close"].iloc[-1])
    previous = float(history["Close"].iloc[-2])

    return current, previous

def get_gov_bond_data():
    BASE_URL = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service'
    SECURITIES = ['Treasury Bills', 'Treasury Notes', 'Treasury Bonds']
    AUCTION_TYPES = ['Bill', 'Note', 'Bond']

    # 1. Fetch the most recent average interest rates
    rates_url = f'{BASE_URL}/v2/accounting/od/avg_interest_rates'
    rates_params = {
        'fields': 'record_date,security_desc,avg_interest_rate_amt',
        'filter': f"security_desc:in:({','.join(SECURITIES)})",
        'sort': '-record_date',
        'page[size]': 10,
    }

    rates_res = requests.get(rates_url, params=rates_params).json()
    rates_df = pd.DataFrame(rates_res['data'])

    # Keep only the latest reporting month
    latest_date = rates_df['record_date'].max()
    current_rates_df = rates_df[rates_df['record_date'] == latest_date].copy()
    current_rates_df['avg_interest_rate_amt'] = pd.to_numeric(
        current_rates_df['avg_interest_rate_amt']
    )

    # Normalize security names to match the auctions endpoint ('Bill', 'Note', 'Bond')
    name_map = {
        'Treasury Bills': 'Bill',
        'Treasury Notes': 'Note',
        'Treasury Bonds': 'Bond',
    }
    current_rates_df['Security Type'] = current_rates_df['security_desc'].map(
        name_map
    )

    # 2. Fetch securities issued over the past 3 months (90 days)
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=90)).strftime('%Y-%m-%d')

    auctions_url = f'{BASE_URL}/v1/accounting/od/auctions_query'
    auctions_params = {
        'fields': 'issue_date,security_type,total_accepted',
        'filter': (
            f"security_type:in:({','.join(AUCTION_TYPES)}),"
            f'issue_date:gte:{start_date},'
            f'issue_date:lte:{end_date}'
        ),
        'page[size]': 1000,
    }

    auctions_res = requests.get(auctions_url, params=auctions_params).json()
    auctions_df = pd.DataFrame(auctions_res['data'])

    # Convert issued amounts to numeric and sum by security type
    auctions_df['total_accepted'] = pd.to_numeric(
        auctions_df['total_accepted'], errors='coerce'
    )
    issued_3m_df = (
        auctions_df.groupby('security_type', as_index=False)['total_accepted']
        .sum()
        .rename(
            columns={
                'security_type': 'Security Type',
                'total_accepted': '3M Issued Amount ($)',
            }
        )
    )

    # 3. Combine both datasets into a single summary DataFrame
    summary_df = pd.merge(
        current_rates_df[['Security Type', 'record_date', 'avg_interest_rate_amt']],
        issued_3m_df,
        on='Security Type',
        how='outer',
    ).rename(
        columns={
            'record_date': 'Rate As Of',
            'avg_interest_rate_amt': 'Current Avg Rate (%)',
        }
    )

    print(summary_df.to_string(index=False))
    return summary_df
