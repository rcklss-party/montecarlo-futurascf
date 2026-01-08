import yfinance as yf

def test_euro_agg_tickers():
    # Candidates:
    # EUAG.MI: iShares Core Euro Aggregate Bond UCITS ETF (Borsa Italiana)
    # IEAG.AS: iShares Core Euro Aggregate Bond UCITS ETF (Euronext Amsterdam)
    # EAGG.PA: SPDR Bloomberg Euro Aggregate Bond UCITS ETF (Euronext Paris)
    # LEATTREU: Bloomberg Euro Aggregate Treasury Total Return Index Value Unhedged EUR (Index itself often not on Yahoo)
    
    candidates = ["EUAG.MI", "IEAG.AS", "EAGG.PA", "SYBA.DE", "IEAG.L"]
    
    print("Testing Euro Aggregate candidates...")
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
    test_euro_agg_tickers()
