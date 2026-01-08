import yfinance as yf

def test_global_hedged_tickers():
    # Candidates:
    # AGGH.AS: iShares Core Global Aggregate Bond UCITS ETF EUR Hedged (Acc) - Euronext Amsterdam
    # EUNA.DE: iShares Core Global Aggregate Bond UCITS ETF EUR Hedged (Acc) - Xetra
    # SPFF.L: SPDR Bloomberg Global Aggregate Bond UCITS ETF EUR Hedged - London
    # XG7S.DE: Xtrackers II Global Aggregate Bond Swap UCITS ETF 1D - EUR Hedged
    
    candidates = ["AGGH.AS", "EUNA.DE", "SPFF.L", "XG7S.DE", "GLBAG.MI"]
    
    print("Testing Global Aggregate EUR Hedged candidates...")
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
    test_global_hedged_tickers()
