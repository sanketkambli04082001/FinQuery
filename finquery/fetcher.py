# fetcher.py (simplified version without retry logic)
import os
import time
import requests
import yfinance as yf

from dotenv import load_dotenv

load_dotenv()

class DataFetcher:
    def __init__(self):
        self.api_key = os.getenv("ALPHA_VANTAGE_KEY")
        self.base_url = "https://www.alphavantage.co/query"

        if not self.api_key:
            raise ValueError("API key 'ALPHA_VANTAGE_KEY' not found in .env file.")

    def _clean_number(self, v):
        try:
            if v is None:
                return "N/A"
            if isinstance(v, (int, float)):
                return v
            s = str(v)
            s = s.replace(",", "").strip()
            if s.endswith("%"):
                return float(s.strip("%")) / 100.0
            return float(s)
        except Exception:
            return "N/A"

    def _fetch_indian_data(self, ticker):
        """Fetch Indian company data using yfinance (.NS tickers)."""
        ticker_norm = ticker.strip().upper()
        if not ticker_norm.endswith(".NS"):
            ticker_query = ticker_norm + ".NS"
        else:
            ticker_query = ticker_norm

        print(f"--- [yfinance] Trying to fetch {ticker_query} ...")
        try:
            t = yf.Ticker(ticker_query)

            # Try to get info safely
            try:
                info = t.info or {}
            except:
                info = t.get_info() if hasattr(t, "get_info") else {}

            if not info or (not info.get("longName") and not info.get("shortName")):
                print(f"--- [yfinance] No usable info for {ticker_query}")
                return None

            formatted_data = {
                "Name": info.get("longName") or info.get("shortName") or ticker_query,
                "PERatio": info.get("trailingPE") or info.get("forwardPE") or "N/A",
                "MarketCapitalization": info.get("marketCap", "N/A"),
                "EPS": info.get("trailingEps") or info.get("epsTrailingTwelveMonths") or "N/A",
                "DividendYield": info.get("dividendYield", "N/A")
            }
            print(f"--- [yfinance] Success for {ticker_query}")
            return formatted_data

        except Exception as e:
            print(f"--- [yfinance] Error: {e}")
            return None

    def _fetch_alpha_vantage_data(self, ticker):
        """Fetch global/US data using Alpha Vantage OVERVIEW."""
        ticker_norm = ticker.strip().upper()

        params = {
            "function": "OVERVIEW",
            "symbol": ticker_norm,
            "apikey": self.api_key
        }

        print(f"--- [AlphaVantage] Trying to fetch {ticker_norm} ...")
        try:
            resp = requests.get(self.base_url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"--- [AlphaVantage] Failed to fetch data: {e}")
            return None

        if not data or "Note" in data or "Information" in data:
            print(f"--- [AlphaVantage] Empty or rate-limited response for {ticker_norm}")
            return None

        formatted = {
            "Name": data.get("Name", ticker_norm),
            "PERatio": data.get("PERatio", "N/A"),
            "MarketCapitalization": data.get("MarketCapitalization", "N/A"),
            "EPS": data.get("EPS", "N/A"),
            "DividendYield": data.get("DividendYield", "N/A")
        }

        print(f"--- [AlphaVantage] Success for {ticker_norm}")
        return formatted

    def get_company_overview(self, ticker):
        """
        Try yfinance (India/NSE) first.
        If yfinance fails, fallback to Alpha Vantage.
        """
        print(f"--- [Fetcher] Checking Indian source for '{ticker}'")
        data = self._fetch_indian_data(ticker)
        if data:
            return data

        print(f"--- [Fetcher] Indian failed → Trying Alpha Vantage for '{ticker}'")
        return self._fetch_alpha_vantage_data(ticker)

    def get_competitor_stats(self, competitors):
        
        results = []
        for sym in (competitors or []):
            try:
                print(f"--- [Fetcher] Getting stats for {sym} ...")
                info = self.get_company_overview(sym)
                # Keep a simple shape: ticker + info dict (may contain PERatio, MarketCapitalization, etc.)
                results.append({"symbol": sym, "info": info})
            except Exception as e:
                print(f"--- [Fetcher] ERROR fetching stats for {sym}: {e}")
                results.append({"symbol": sym, "info": None})
        return results
