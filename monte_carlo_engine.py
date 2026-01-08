import numpy as np
from typing import Dict, Any


def run_monte_carlo_simulation(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Esegue simulazione Monte Carlo su portafoglio con GBM.
    
    Args:
        params: dizionario con:
            - capital: capitale iniziale (€)
            - mu: rendimento annuo atteso (decimale, es. 0.0523)
            - sigma: volatilità annua (decimale, es. 0.0695)
            - years: orizzonte temporale (anni)
            - n_sims: numero simulazioni
            - seed: seed random (opzionale, default None)
    
    Returns:
        dizionario con:
            - paths: array (n_sims x n_steps) con valori portafoglio
            - time: array con timestamp (anni)
            - percentiles_time: dict con p3, p25, p50, p75 nel tempo
            - percentiles_final: dict con valori finali per percentile
            - stats: dict con statistiche (mean, std, cagr)
    """
    # Estrai parametri
    S0 = params['capital']
    mu = params['mu']
    sigma = params['sigma']
    T = params['years']
    n_sims = params['n_sims']
    seed = params.get('seed', None)
    
    # Setup
    if seed is not None:
        np.random.seed(seed)
    
    dt = 1/12  # step mensile
    n_steps = int(T / dt)
    
    # Genera shock normali
    Z = np.random.randn(n_sims, n_steps)
    
    # GBM formula
    drift = (mu - 0.5 * sigma**2) * dt
    diffusion = sigma * np.sqrt(dt)
    log_returns = drift + diffusion * Z
    
    # Cumulative per prezzi
    cum_log_returns = np.cumsum(log_returns, axis=1)
    paths = S0 * np.exp(cum_log_returns)
    
    # Aggiungi S0 come primo valore
    paths = np.column_stack([np.full(n_sims, S0), paths])
    time = np.linspace(0, T, n_steps + 1)
    
    # Calcola percentili nel tempo
    p3_time = np.percentile(paths, 3, axis=0)
    p25_time = np.percentile(paths, 25, axis=0)
    p50_time = np.percentile(paths, 50, axis=0)
    p75_time = np.percentile(paths, 75, axis=0)
    
    # Percentili finali
    final_values = paths[:, -1]
    p3_final = np.percentile(final_values, 3)
    p5_final = np.percentile(final_values, 5)
    p7_final = np.percentile(final_values, 7)
    p10_final = np.percentile(final_values, 10)
    p25_final = np.percentile(final_values, 25)
    p50_final = np.percentile(final_values, 50)
    p75_final = np.percentile(final_values, 75)
    
    # Statistiche
    mean_final = np.mean(final_values)
    std_final = np.std(final_values, ddof=1)
    
    # CAGR per ogni simulazione
    cagr = (final_values / S0) ** (1/T) - 1
    cagr_p3 = np.percentile(cagr, 3)
    cagr_p25 = np.percentile(cagr, 25)
    cagr_p50 = np.percentile(cagr, 50)
    cagr_p75 = np.percentile(cagr, 75)
    
    # Calcola distribuzione su CAGR con granularità fissa 0.2% (0.002)
    # Usiamo 'weights' per ottenere la % diretta invece della densità astratta
    cagr_min = np.floor(cagr.min() / 0.002) * 0.002
    cagr_max = np.ceil(cagr.max() / 0.002) * 0.002
    bins = np.arange(cagr_min, cagr_max + 0.002, 0.002)
    
    hist_counts, hist_bins = np.histogram(cagr, bins=bins, weights=np.ones(len(cagr)) / len(cagr))
    hist_x = (hist_bins[:-1] + hist_bins[1:]) / 2
    
    return {
        'paths': paths,
        'time': time,
        'percentiles_time': {
            'p3': p3_time,
            'p25': p25_time,
            'p50': p50_time,
            'p75': p75_time
        },
        'percentiles_final': {
            'p3': p3_final,
            'p5': p5_final,
            'p7': p7_final,
            'p10': p10_final,
            'p25': p25_final,
            'p50': p50_final,
            'p75': p75_final
        },
        'stats': {
            'mean': mean_final,
            'std': std_final,
            'cagr_p3': cagr_p3,
            'cagr_p5': np.percentile(cagr, 5),
            'cagr_p7': np.percentile(cagr, 7),
            'cagr_p10': np.percentile(cagr, 10),
            'cagr_p25': cagr_p25,
            'cagr_p50': cagr_p50,
            'cagr_p75': cagr_p75
        },
        'n_sims': n_sims,
        'distribution': {
            'x': hist_x.tolist(),
            'y': hist_counts.tolist()
        }
    }


# Test
if __name__ == "__main__":
    test_params = {
        'capital': 400_000,
        'mu': 0.0523,
        'sigma': 0.0695,
        'years': 30,
        'n_sims': 10_000,
        'seed': 42
    }
    
    results = run_monte_carlo_simulation(test_params)
    print(f"Mediana finale: €{results['percentiles_final']['p50']:,.0f}")
    print(f"CAGR mediano: {results['stats']['cagr_p50']*100:.2f}%")
