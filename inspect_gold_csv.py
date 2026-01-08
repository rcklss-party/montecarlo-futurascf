import pandas as pd
import io
import requests

def inspect_datahub_gold():
    url = "https://datahub.io/core/gold-prices/r/monthly.csv"
    # Follow redirects
    response = requests.get(url, allow_redirects=True)
    
    if response.status_code == 200:
        print("✅ Download successful!")
        content = response.content.decode('utf-8')
        # Print first few lines to debug
        print("\n--- Raw CSV Head ---")
        print('\n'.join(content.split('\n')[:5]))
        
        # Try parsing
        try:
            df = pd.read_csv(io.StringIO(content))
            print("\n✅ Parsed DataFrame:")
            print(df.head())
            print(f"\nTime range: {df.iloc[0,0]} to {df.iloc[-1,0]}")
        except Exception as e:
            print(f"❌ Parsing Error: {e}")
    else:
        print(f"❌ Download failed. Status: {response.status_code}")

if __name__ == "__main__":
    inspect_datahub_gold()
