import flet as ft
import pandas as pd
import yfinance as yf

def fetch_data():
    tickers = ["AAPL", "TSLA", "AMZN", "MSFT", "GOOGL", "NVDA", "AMD", "META", "INTC", "NFLX"]
    data = []

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info
        data.append({
            "Name": info.get("shortName", ticker),
            "Price": info.get("regularMarketPrice", "N/A"),
            "Change": info.get("regularMarketChangePercent", "N/A"),
        })

    return pd.DataFrame(data)

def main(page: ft.Page):
    page.title = "Stock Tracker - Yahoo Finance"
    page.scroll = "auto"

    title = ft.Text("📈 Most Active Stocks (via yfinance) -Albert Hlelesi", size=24, weight="bold")
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Price")),
            ft.DataColumn(ft.Text("Change (%)")),
        ],
        rows=[]
    )

    # Load data and update UI
    def load_data(e=None):
        df = fetch_data()
        table.rows.clear()

        for _, row in df.iterrows():
            change = row["Change"]
            change_str = f"{change:.2f}%" if isinstance(change, float) else str(change)
            table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(row["Name"]))),
                        ft.DataCell(ft.Text(str(row["Price"]))),
                        ft.DataCell(ft.Text(change_str)),
                    ]
                )
            )
        page.update()

    refresh_btn = ft.ElevatedButton("🔄 Refresh", on_click=load_data)

    page.add(title, refresh_btn, table)
    load_data()  # Load data on start

ft.app(target=main, view=ft.WEB_BROWSER)

