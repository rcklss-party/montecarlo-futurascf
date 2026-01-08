import yfinance as yf

def test_gold_tickers():
    # Candidates:
    # GLD: SPDR Gold Shares (USA, Start 2004)
    # IGLN.L: iShares Physical Gold ETC (London, Start 2011)
    # IAU: iShares Gold Trust (USA, Start 2005)
    # SGLN.L: Invesco Physical Gold ETC (London)
    # GC=F: Gold Futures (Comex) - often has very long history but is futures data
    
    candidates = ["GLD", "IAU", "IGLN.L", "SGLN.L", "GC=F"]
    
    print("Testing LBMA Gold Price PM candidates (Proxies)...")
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
    test_gold_tickers()
