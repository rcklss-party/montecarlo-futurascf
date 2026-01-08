import yfinance as yf
import pandas as pd
import io

def fetch_msci_world_returns():
    # Ticker Yahoo Finance per "MSCI World Net Total Return USD Index"
    # Codice comune: ^990100-USD-STRD
    ticker = "^990100-USD-STRD"
    
    print(f"⏳ Scarico dati storici INDICE MSCI World ({ticker})...")
    
    # Scarichiamo il massimo storico disponibile
    try:
        data = yf.download(ticker, period="max", progress=False)
    except Exception as e:
        print(f"❌ Errore durante il download: {e}")
        return

    if data.empty:
        print("❌ Errore: Nessun dato scaricato. Il ticker potrebbe essere momentaneamente non disponibile.")
        return

    print(f"✅ Dati scaricati: {len(data)} giorni di trading dal {data.index[0].strftime('%Y-%m-%d')} al {data.index[-1].strftime('%Y-%m-%d')}")
    
    # Calcolo rendimenti giornalieri (Close to Close)
    # Per gli indici spesso 'Close' e 'Adj Close' coincidono, ma usiamo Adj Close per sicurezza
    price_col = 'Adj Close' if 'Adj Close' in data.columns else 'Close'
    
    # Gestione multi-index se presente (yfinance a volte ritorna multi-level columns)
    if isinstance(data.columns, pd.MultiIndex):
        daily_returns = data.xs(price_col, axis=1, level=0).pct_change()
        # Se rimane ancora un livello (es. ticker), prendilo
        if daily_returns.shape[1] == 1:
             daily_returns = daily_returns.iloc[:, 0]
    else:
        daily_returns = data[price_col].pct_change()
    
    # Rimuovi NaN iniziale
    daily_returns = daily_returns.dropna()
    
    # Statistiche di base
    mean_daily = daily_returns.mean()
    std_daily = daily_returns.std()
    
    # Annualizzazione (approssimata a 252 giorni di trading)
    mean_annual = mean_daily * 252
    std_annual = std_daily * (252**0.5)
    
    print("\n📊 Prime 5 righe (Rendimenti Giornalieri):")
    print(daily_returns.head())
    
    print("\n📈 Statistiche Storiche INDICE (Annualizzate):")
    print(f"   Rendimento Medio Annuo: {mean_annual:.2%}")
    print(f"   Volatilità Annua:       {std_annual:.2%}")
    
    return daily_returns

def fetch_euro_aggregate_returns():
    # Ticker proxy: iShares Core Euro Aggregate Bond UCITS ETF
    # Ticker Yahoo: IEAG.AS (Euronext Amsterdam)
    # È uno dei più grandi e liquidi, con storico dal 2009.
    ticker = "IEAG.AS"
    
    print(f"\n⏳ Scarico dati storici Bloomberg Euro Aggregate (Proxy: {ticker})...")
    
    try:
        data = yf.download(ticker, period="max", progress=False)
    except Exception as e:
        print(f"❌ Errore durante il download: {e}")
        return

    if data.empty:
        print("❌ Errore: Nessun dato scaricato.")
        return

    print(f"✅ Dati scaricati: {len(data)} giorni di trading dal {data.index[0].strftime('%Y-%m-%d')} al {data.index[-1].strftime('%Y-%m-%d')}")
    
    price_col = 'Adj Close' if 'Adj Close' in data.columns else 'Close'
    
    if isinstance(data.columns, pd.MultiIndex):
        daily_returns = data.xs(price_col, axis=1, level=0).pct_change()
        if daily_returns.shape[1] == 1:
             daily_returns = daily_returns.iloc[:, 0]
    else:
        daily_returns = data[price_col].pct_change()
    
    daily_returns = daily_returns.dropna()
    
    mean_daily = daily_returns.mean()
    std_daily = daily_returns.std()
    
    mean_annual = mean_daily * 252
    std_annual = std_daily * (252**0.5)
    
    print("\n📊 Prime 5 righe (Rendimenti Giornalieri):")
    print(daily_returns.head())
    
    print("\n📈 Statistiche Storiche EURO AGGREGATE (Annualizzate):")
    print(f"   Rendimento Medio Annuo: {mean_annual:.2%}")
    print(f"   Volatilità Annua:       {std_annual:.2%}")
    
    return daily_returns

    return daily_returns

def fetch_global_aggregate_hedged_returns():
    # Ticker proxy: Xtrackers II Global Aggregate Bond Swap UCITS ETF 1D - EUR Hedged
    # Ticker Yahoo: XG7S.DE (Xetra)
    # Storico dal 2013-08-14.
    ticker = "XG7S.DE"
    
    print(f"\n⏳ Scarico dati storici Bloomberg Global Aggregate EUR Hedged (Proxy: {ticker})...")
    
    try:
        data = yf.download(ticker, period="max", progress=False)
    except Exception as e:
        print(f"❌ Errore durante il download: {e}")
        return

    if data.empty:
        print("❌ Errore: Nessun dato scaricato.")
        return

    print(f"✅ Dati scaricati: {len(data)} giorni di trading dal {data.index[0].strftime('%Y-%m-%d')} al {data.index[-1].strftime('%Y-%m-%d')}")
    
    price_col = 'Adj Close' if 'Adj Close' in data.columns else 'Close'
    
    if isinstance(data.columns, pd.MultiIndex):
        daily_returns = data.xs(price_col, axis=1, level=0).pct_change()
        if daily_returns.shape[1] == 1:
             daily_returns = daily_returns.iloc[:, 0]
    else:
        daily_returns = data[price_col].pct_change()
    
    daily_returns = daily_returns.dropna()
    
    mean_daily = daily_returns.mean()
    std_daily = daily_returns.std()
    
    mean_annual = mean_daily * 252
    std_annual = std_daily * (252**0.5)
    
    print("\n📊 Prime 5 righe (Rendimenti Giornalieri):")
    print(daily_returns.head())
    
    print("\n📈 Statistiche Storiche GLOBAL AGGREGATE HEDGED (Annualizzate):")
    print(f"   Rendimento Medio Annuo: {mean_annual:.2%}")
    print(f"   Volatilità Annua:       {std_annual:.2%}")
    
    return daily_returns

    return daily_returns

def fetch_gold_long_term():
    import requests
    import io
    
    # Fonte: DataHub (Monthly Gold Prices since 1950)
    url = "https://datahub.io/core/gold-prices/r/monthly.csv"
    
    print(f"\n⏳ Scarico dati storici Gold (Long Term) da DataHub...")
    
    try:
        response = requests.get(url, allow_redirects=True)
        if response.status_code != 200:
            print(f"❌ Download failed. Status: {response.status_code}")
            return
            
        content = response.content.decode('utf-8')
        data = pd.read_csv(io.StringIO(content))
        
        # Parsing data: formato atteso 'YYYY-MM'
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)
        
        # Uso tutto lo storico disponibile (dal 1950)
        # data = data[data.index >= '1970-01-01']
        
    except Exception as e:
        print(f"❌ Errore durante elaborazione DataHub: {e}")
        return

    print(f"✅ Dati scaricati: {len(data)} mesi dal {data.index[0].strftime('%Y-%m')} al {data.index[-1].strftime('%Y-%m')}")
    
    # Calcolo rendimenti MENSILI
    # DataHub ha colonna 'Price'
    monthly_returns = data['Price'].pct_change().dropna()
    
    # Statistiche MENSILI
    mean_monthly = monthly_returns.mean()
    std_monthly = monthly_returns.std()
    
    # Annualizzazione (x12 per rendimento, xSQRT(12) per volatilità)
    mean_annual = mean_monthly * 12
    std_annual = std_monthly * (12**0.5)
    
    print("\n📊 Prime 5 righe (Rendimenti Mensili):")
    print(monthly_returns.head())
    
    print("\n📈 Statistiche Storiche GOLD (1970-Oggi, Annualizzate da dati Mensili):")
    print(f"   Rendimento Medio Annuo: {mean_annual:.2%}")
    print(f"   Volatilità Annua:       {std_annual:.2%}")
    
    return monthly_returns

    return monthly_returns

    return monthly_returns

def fetch_sp500_long_term():
    # Ticker: ^GSPC (S&P 500 Index)
    # Storico: dal 1927 su Yahoo Finance
    ticker = "^GSPC"
    print(f"\n⏳ Scarico dati storici S&P 500 (Long Term: {ticker})...")
    try:
        data = yf.download(ticker, period="max", progress=False)
        if data.empty: return None
        
        price_col = 'Adj Close' if 'Adj Close' in data.columns else 'Close'
        if isinstance(data.columns, pd.MultiIndex):
            returns = data.xs(price_col, axis=1, level=0).pct_change()
            if returns.shape[1] == 1: returns = returns.iloc[:, 0]
        else:
            returns = data[price_col].pct_change()
            
        returns = returns.dropna()
        
        # Stats
        mean_ann = returns.mean() * 252
        std_ann = returns.std() * (252**0.5)
        print(f"✅ S&P 500: {len(returns)} giorni ({returns.index[0].date()} - {returns.index[-1].date()})")
        print(f"   Rendimento: {mean_ann:.2%}, Volatilità: {std_ann:.2%}")
        
        return returns
    except Exception as e:
        print(f"❌ Errore S&P 500: {e}")
        return None

def fetch_world_ex_usa():
    # Ticker: EFA (iShares MSCI EAFE ETF) - Proxy Developed Markets ex-US
    # Storico: dal 2001
    # ACWX (ACWI ex US) parte solo dal 2008
    ticker = "EFA" 
    print(f"\n⏳ Scarico dati storici World ex USA (Proxy: {ticker})...")
    try:
        data = yf.download(ticker, period="max", progress=False)
        if data.empty: return None
        
        price_col = 'Adj Close' if 'Adj Close' in data.columns else 'Close'
        if isinstance(data.columns, pd.MultiIndex):
            returns = data.xs(price_col, axis=1, level=0).pct_change()
            if returns.shape[1] == 1: returns = returns.iloc[:, 0]
        else:
            returns = data[price_col].pct_change()
            
        returns = returns.dropna()
        
        # Stats
        mean_ann = returns.mean() * 252
        std_ann = returns.std() * (252**0.5)
        print(f"✅ World ex USA: {len(returns)} giorni ({returns.index[0].date()} - {returns.index[-1].date()})")
        print(f"   Rendimento: {mean_ann:.2%}, Volatilità: {std_ann:.2%}")
        
        return returns
    except Exception as e:
        print(f"❌ Errore World ex USA: {e}")
        return None

def fetch_emerging_markets():
    # Ticker: EEM (iShares MSCI Emerging Markets ETF)
    # Oldest EM ETF - Historical data since April 7, 2003
    ticker = "EEM"
    print(f"\n⏳ Scarico dati storici Mercati Emergenti (Proxy: {ticker})...")
    try:
        data = yf.download(ticker, period="max", progress=False)
        if data.empty: return None
        
        price_col = 'Adj Close' if 'Adj Close' in data.columns else 'Close'
        if isinstance(data.columns, pd.MultiIndex):
            returns = data.xs(price_col, axis=1, level=0).pct_change()
            if returns.shape[1] == 1: returns = returns.iloc[:, 0]
        else:
            returns = data[price_col].pct_change()
            
        returns = returns.dropna()
        
        # Stats
        mean_ann = returns.mean() * 252
        std_ann = returns.std() * (252**0.5)
        print(f"✅ Emerging Markets: {len(returns)} giorni ({returns.index[0].date()} - {returns.index[-1].date()})")
        print(f"   Rendimento: {mean_ann:.2%}, Volatilità: {std_ann:.2%}")
        
        return returns
    except Exception as e:
        print(f"❌ Errore Emerging Markets: {e}")
        return None

def fetch_quality_factor():
    # Ticker: QUAL (iShares MSCI USA Quality Factor ETF)
    # Historical data since July 16, 2013
    ticker = "QUAL"
    print(f"\n⏳ Scarico dati storici Quality Factor (Proxy: {ticker})...")
    try:
        data = yf.download(ticker, period="max", progress=False)
        if data.empty: return None
        
        price_col = 'Adj Close' if 'Adj Close' in data.columns else 'Close'
        if isinstance(data.columns, pd.MultiIndex):
            returns = data.xs(price_col, axis=1, level=0).pct_change()
            if returns.shape[1] == 1: returns = returns.iloc[:, 0]
        else:
            returns = data[price_col].pct_change()
            
        returns = returns.dropna()
        
        mean_ann = returns.mean() * 252
        std_ann = returns.std() * (252**0.5)
        print(f"✅ Quality Factor: {len(returns)} giorni ({returns.index[0].date()} - {returns.index[-1].date()})")
        print(f"   Rendimento: {mean_ann:.2%}, Volatilità: {std_ann:.2%}")
        
        return returns
    except Exception as e:
        print(f"❌ Errore Quality Factor: {e}")
        return None

def fetch_value_factor():
    # Ticker: IWD (iShares Russell 1000 Value ETF)
    # Historical data since May 22, 2000
    ticker = "IWD"
    print(f"\n⏳ Scarico dati storici Value Factor (Proxy: {ticker})...")
    try:
        data = yf.download(ticker, period="max", progress=False)
        if data.empty: return None
        
        price_col = 'Adj Close' if 'Adj Close' in data.columns else 'Close'
        if isinstance(data.columns, pd.MultiIndex):
            returns = data.xs(price_col, axis=1, level=0).pct_change()
            if returns.shape[1] == 1: returns = returns.iloc[:, 0]
        else:
            returns = data[price_col].pct_change()
            
        returns = returns.dropna()
        
        mean_ann = returns.mean() * 252
        std_ann = returns.std() * (252**0.5)
        print(f"✅ Value Factor: {len(returns)} giorni ({returns.index[0].date()} - {returns.index[-1].date()})")
        print(f"   Rendimento: {mean_ann:.2%}, Volatilità: {std_ann:.2%}")
        
        return returns
    except Exception as e:
        print(f"❌ Errore Value Factor: {e}")
        return None


def fetch_momentum_factor():
    # Ticker: MTUM (iShares MSCI USA Momentum Factor ETF)
    # Historical data since April 16, 2013
    ticker = "MTUM"
    print(f"\n⏳ Scarico dati storici Momentum Factor (Proxy: {ticker})...")
    try:
        data = yf.download(ticker, period="max", progress=False)
        if data.empty: return None
        
        price_col = 'Adj Close' if 'Adj Close' in data.columns else 'Close'
        if isinstance(data.columns, pd.MultiIndex):
            returns = data.xs(price_col, axis=1, level=0).pct_change()
            if returns.shape[1] == 1: returns = returns.iloc[:, 0]
        else:
            returns = data[price_col].pct_change()
            
        returns = returns.dropna()
        
        mean_ann = returns.mean() * 252
        std_ann = returns.std() * (252**0.5)
        print(f"✅ Momentum Factor: {len(returns)} giorni ({returns.index[0].date()} - {returns.index[-1].date()})")
        print(f"   Rendimento: {mean_ann:.2%}, Volatilità: {std_ann:.2%}")
        
        return returns
    except Exception as e:
        print(f"❌ Errore Momentum Factor: {e}")
        return None

def fetch_small_cap():
    # Ticker: IWM (iShares Russell 2000 ETF)
    # Oldest Small Cap ETF - Historical data since May 22, 2000
    ticker = "IWM"
    print(f"\n⏳ Scarico dati storici Small Cap (Proxy: {ticker})...")
    try:
        data = yf.download(ticker, period="max", progress=False)
        if data.empty: return None
        
        price_col = 'Adj Close' if 'Adj Close' in data.columns else 'Close'
        if isinstance(data.columns, pd.MultiIndex):
            returns = data.xs(price_col, axis=1, level=0).pct_change()
            if returns.shape[1] == 1: returns = returns.iloc[:, 0]
        else:
            returns = data[price_col].pct_change()
            
        returns = returns.dropna()
        
        mean_ann = returns.mean() * 252
        std_ann = returns.std() * (252**0.5)
        print(f"✅ Small Cap: {len(returns)} giorni ({returns.index[0].date()} - {returns.index[-1].date()})")
        print(f"   Rendimento: {mean_ann:.2%}, Volatilità: {std_ann:.2%}")
        
        return returns
    except Exception as e:
        print(f"❌ Errore Small Cap: {e}")
        return None

def fetch_multifactor():
    # Ticker: JPUS (JPMorgan Diversified Return US Equity ETF)
    # Oldest Multifactor ETF - Historical data since September 2015
    ticker = "JPUS"
    print(f"\n⏳ Scarico dati storici Multifactor (Proxy: {ticker})...")
    try:
        data = yf.download(ticker, period="max", progress=False)
        if data.empty: return None
        
        price_col = 'Adj Close' if 'Adj Close' in data.columns else 'Close'
        if isinstance(data.columns, pd.MultiIndex):
            returns = data.xs(price_col, axis=1, level=0).pct_change()
            if returns.shape[1] == 1: returns = returns.iloc[:, 0]
        else:
            returns = data[price_col].pct_change()
            
        returns = returns.dropna()
        
        mean_ann = returns.mean() * 252
        std_ann = returns.std() * (252**0.5)
        print(f"✅ Multifactor: {len(returns)} giorni ({returns.index[0].date()} - {returns.index[-1].date()})")
        print(f"   Rendimento: {mean_ann:.2%}, Volatilità: {std_ann:.2%}")
        
        return returns
    except Exception as e:
        print(f"❌ Errore Multifactor: {e}")
        return None

def export_asset_data():
    import json
    import numpy as np
    
    print("\n🔄 -- ELABORAZIONE FINALE E ESPORTAZIONE --")
    
    # 1. Fetch Returns (Daily or Monthly)
    assets = {}
    
    print("1. Scarico Asset Core...")
    assets['sp500'] = fetch_sp500_long_term()
    assets['world_ex_usa'] = fetch_world_ex_usa()
    assets['emerging_markets'] = fetch_emerging_markets()
    
    print("2. Scarico Smart Beta / Factors...")
    assets['quality'] = fetch_quality_factor()
    assets['value'] = fetch_value_factor()
    assets['momentum'] = fetch_momentum_factor()
    assets['small_cap'] = fetch_small_cap()
    assets['multifactor'] = fetch_multifactor()
    
    print("3. Scarico Bonds & Alternatives...")
    assets['euro_aggregate'] = fetch_euro_aggregate_returns()
    assets['global_aggregate'] = fetch_global_aggregate_hedged_returns()
    assets['gold'] = fetch_gold_long_term() 
    
    # Define display names and scalar for annualization
    meta = {
        'sp500': {'name': 'S&P 500 (USA)', 'freq': 'D'},
        'world_ex_usa': {'name': 'World ex USA', 'freq': 'D'},
        'emerging_markets': {'name': 'Emerging Markets', 'freq': 'D'},
        'quality': {'name': 'Quality Factor', 'freq': 'D'},
        'value': {'name': 'Value Factor (IWD)', 'freq': 'D'},
        'momentum': {'name': 'Momentum Factor', 'freq': 'D'},
        'small_cap': {'name': 'Small Cap (IWM)', 'freq': 'D'},
        'multifactor': {'name': 'Multifactor', 'freq': 'D'},
        'euro_aggregate': {'name': 'Euro Aggregate', 'freq': 'D'},
        'global_aggregate': {'name': 'Global Agg Hedged', 'freq': 'D'},
        'gold': {'name': 'Gold (Spot)', 'freq': 'M'}
    }
    
    # 2. Calculate Stats (on full available history for each)
    stats = {}
    monthly_series = {}
    
    for key, data in assets.items():
        if data is None or len(data) == 0:
            print(f"⚠️ Dati mancanti per {key}")
            continue
            
        # Stats
        if meta[key]['freq'] == 'D':
            mu = data.mean() * 252
            sigma = data.std() * (252**0.5)
            # Resample to Monthly for Correlation
            monthly = data.resample('M').apply(lambda x: (1 + x).prod() - 1)
        else: # Monthly (Gold)
            mu = data.mean() * 12
            sigma = data.std() * (12**0.5)
            monthly = data
            
        stats[key] = {
            "name": meta[key]['name'],
            "mu": mu,
            "sigma": sigma
        }
        
        # Align index to end of month for consistency
        monthly.index = monthly.index.to_period('M').to_timestamp('M')
        monthly.name = meta[key]['name']
        monthly_series[key] = monthly

    # 3. Create Master DataFrame for Correlation
    # We use inner join or outer? 
    # Pairwise correlation in pandas ignores NaNs, so Outer Join is best to maximize data for each pair.
    df_all = pd.DataFrame(monthly_series)
    
    # 4. Correlation Matrix
    correlation_matrix = df_all.corr()
    
    print("\n🔗 Matrice di Correlazione (Anteprima):")
    print(correlation_matrix.iloc[:5, :5])
    
    output_data = {
        "stats": stats,
        # fillna(0) just in case, though corr() usually returns 1s on diag and values elsewhere
        "correlations": correlation_matrix.fillna(0).to_dict()
    }
    
    with open('static/asset_data.json', 'w') as f:
        json.dump(output_data, f, indent=4)
        
    print("\n💾 Dati aggiornati ed esportati in 'static/asset_data.json'")

if __name__ == "__main__":
    export_asset_data()
