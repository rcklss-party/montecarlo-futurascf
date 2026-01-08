import yfinance as yf

def test_historical_gold_tickers():
    # Candidates for long-term gold:
    # GC=F: Gold Futures (Starts ~2000)
    # XAUUSD=X: Gold Spot US Dollar
    # ^XAU: PHA Gold & Silver Index (Stocks, not useful for direct proxy but worth checking start date)
    # NEM: Newmont Corporation (Gold Miner, proxy? Starts 1980s?)
    # GOLD: Barrick Gold (Starts 1980s?)
    
    candidates = ["GC=F", "XAUUSD=X", "^XAU", "NEM", "GOLD"]
    
    print("Testing Long-Term Gold candidates...")
    for t in candidates:
        print(f"\n--- Testing {t} ---")
        try:
            data = yf.download(t, period="max", progress=False)
            if not data.empty:
                print(f"✅ {t} FOUND!")
                print(f"   Rows: {len(data)}")
                print(f"   Start Date: {data.index[0].strftime('%Y-%m-%d')}")
                print(f"   End Date:   {data.index[-1].strftime('%Y-%m-%d')}")
            else:
                print(f"❌ {t} returned empty data.")
        except Exception as e:
            print(f"❌ {t} Error: {e}")

if __name__ == "__main__":
    test_historical_gold_tickers()
