import yfinance as yf

def test_tickers():
    candidates = ["^990100-USD-STRD", "^MSWORLD", "MWL", "URTH"]
    for t in candidates:
        print(f"Testing {t}...")
        data = yf.download(t, period="5d", progress=False)
        if not data.empty:
            print(f"✅ {t} FOUND! Rows: {len(data)}")
            print(data.head())
        else:
            print(f"❌ {t} not found or empty.")

if __name__ == "__main__":
    test_tickers()
