import yfinance as yf

def test_new_tickers():
    # S&P 500 Candidates
    # ^GSPC: Standard S&P 500 Index
    # SPY: SPDR S&P 500 ETF (1993)
    
    # MSCI World ex USA Candidates
    # ACWX: iShares MSCI ACWI ex U.S. ETF (2008)
    # VXUS: Vanguard Total International Stock ETF (2011)
    # EFA: iShares MSCI EAFE ETF (Developed ex-US-Canada, 2001) - Close proxy for developed
    # ^990300-USD-STRD: Random Yahoo code for MSCI indexes? Worth trying.
    # ^MIWO00000PUS: Possible index ticker
    
    candidates = ["^GSPC", "SPY", "ACWX", "VXUS", "EFA", "^990300-USD-STRD", "^MIWO00000PUS"]
    
    print("Testing S&P 500 and World ex USA candidates...")
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
    test_new_tickers()
