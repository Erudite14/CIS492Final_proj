"""Display functions for the PY-Bloomberg Terminal prototype.

Stock-index values are fetched from Yahoo Finance via yfinance; they are
recent daily closes, not guaranteed real-time quotes.
"""
import matplotlib.pyplot as plt
from market_data import get_stock_data, get_gov_bond_data, get_money_data


class StockIndex:
    """A market index with its two most recent available closing values."""

    def __init__(self, symbol: str, name: str, current: float, previous: float):
        self.symbol = symbol
        self.name = name
        self.current = current
        self.previous = previous

    def calculate_change(self) -> tuple[float, float]:
        """Calculate the point and percentage changes from the previous value."""
        point_change = self.current - self.previous
        percent_change = (point_change / self.previous) * 100 if self.previous != 0 else 0.0
        return point_change, percent_change


def buildStockDict() -> dict[str, StockIndex]:
    indexes = {
        "SP500": ("^GSPC", "S&P 500"),
        "DJIA": ("^DJI", "Dow Jones"),
        "NASDAQ": ("^IXIC", "Nasdaq Composite")
    }

    results = {}

    for key, (symbol, name) in indexes.items():
        try:
            prices = get_stock_data(symbol)

            if prices is not None:
                current, previous = prices

                results[key] = StockIndex(
                    symbol, name, current, previous
                )

        except Exception as error:
            print(f"Unable to retrieve {name}: {error}")

    return results


def displayBondInfo() -> None:
    bond_data = get_gov_bond_data()
    indexes = {
            "Bills": ("^GSPC", "S&P 500"),
            "Bonds": ("^DJI", "Dow Jones"),
            "Notes": ("^IXIC", "Nasdaq Composite")
        }#----
    return {}


def displayMoneyInfo() -> dict:
    money_data = get_money_data()
    print(f"Dollar (USD): {money_data.get('USD')}")
    print(f"Japanese yen (JPY): {money_data.get('JPY')}")
    print(f"Pound sterling (GBP): {money_data.get('GBP')}")
    print(f"Canadian dollar (CAD): {money_data.get('CAD')}")
    print(f"Swedish krona (SEK): {money_data.get('SEK')}")
    print(f"Swiss franc (CHF): {money_data.get('CHF')}")

    plt.plot(x=range(len(money_data.get('list'))), y=money_data.get('list'))
    plt.xlabel("Days (last 30 calendar days)")
    plt.ylabel("DXY Closing Price")

    plt.show()
    return {}


def buildCommodityDict() -> dict:
    return {}


def buildStateDict() -> dict:
    return {}


def displayInfo() -> None:
    """Display the stock-index prototype as a formatted terminal table."""
    print("\nSTOCK MARKET OVERVIEW [LATEST DAILY CLOSES]")
    print(f"{'INDEX':<22}{'VALUE':>12}{'CHANGE':>12}{'CHANGE %':>12}")
    print("-" * 58)
    for index in buildStockDict().values():
        point_change, percent_change = index.calculate_change()
        print(f"{index.name:<22}{index.current:>12,.2f}{point_change:>+12,.2f}{percent_change:>+11.2f}%")