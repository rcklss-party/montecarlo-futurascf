"""
data_formatter.py
Funzioni per formattare i risultati numerici in formato leggibile per l'utente.
"""

# Dizionario commenti per percentili bassi (30 anni)
TAIL_RISK_CONTEXT = {
    3: {
        "alert_level": "extreme",
        "commento": "⚠️ SCENARIO ESTREMO: Mai verificato in 120+ anni di mercati azionari. Il peggior caso storico reale su 30 anni è stato +4.7% annuo (1902-1932, include Grande Depressione).",
        "probabilita_descrittiva": "Estremamente improbabile (3 su 100 simulazioni)",
        "nota_tecnica": "Il modello GBM può sovrastimare i rischi a lungo termine ignorando la mean reversion documentata nei dati storici."
    },
    5: {
        "alert_level": "extreme",
        "commento": "⚠️ SCENARIO MOLTO SEVERO: Peggiore del worst case storico. Nessun periodo di 30 anni dell'S&P 500 ha mai registrato rendimenti così bassi.",
        "probabilita_descrittiva": "Molto improbabile (5 su 100 simulazioni)",
        "nota_tecnica": "Include scenari di crisi multiple concatenate mai verificatesi nella storia finanziaria moderna."
    },
    7: {
        "alert_level": "high",
        "commento": "⚠️ SCENARIO SEVERO: Al limite del worst case storico. Solo 1 periodo su 120 anni ha performato peggio (1902-1932: +4.7% annuo).",
        "probabilita_descrittiva": "Improbabile (7 su 100 simulazioni)",
        "nota_tecnica": "Rappresenta una combinazione di crisi e sequenza sfavorevole di rendimenti."
    },
    10: {
        "alert_level": "moderate",
        "commento": "📊 SCENARIO PESSIMISTICO: Allineato con il 10° percentile storico (~4.4% reale annuo). Rappresenta il peggiore 10% dei periodi di 30 anni dal 1900.",
        "probabilita_descrittiva": "Possibile ma raro (1 su 10 simulazioni)",
        "nota_tecnica": "Coerente con dati storici di lungo termine durante periodi di crisi prolungate."
    }
}

def get_tail_risk_comment(percentile, rendimento_annuo, n_sims=1000):
    """
    Restituisce il commento contestualizzato per i percentili bassi
    Args:
        percentile (int): 3, 5, 7, o 10
        rendimento_annuo (float): Il rendimento annualizzato percentuale (es. 4.5 per 4.5%)
        n_sims (int): Numero di simulazioni totali per calcolo frequenza
    
    Returns:
        dict: Dizionario con alert_level, commento, probabilità e nota tecnica
    """
    if percentile not in TAIL_RISK_CONTEXT:
        return None
    
    context = TAIL_RISK_CONTEXT[percentile].copy()
    
    # Calcola probabilità esatta su n_sims
    count = int(n_sims * percentile / 100)
    context["probabilita_descrittiva"] = f"{percentile}% ({count} su {n_sims} simulazioni)"

    
    # Aggiungi confronto numerico storico
    # Rendi il check robusto: rendimento_annuo è float (es 5.2)
    ra = float(rendimento_annuo)
    
    if ra < 0:
        context["confronto_storico"] = f"Rendimento negativo: MAI VERIFICATO in alcun periodo di 30 anni (worst case storico: +4.7%)"
    elif ra < 4.4:
        context["confronto_storico"] = f"Rendimento {ra:.2f}%: Peggiore del 10° percentile storico (4.4% reale)"
    elif ra < 6.2:
        context["confronto_storico"] = f"Rendimento {ra:.2f}%: Nel bottom quartile storico (4.4-6.2%)"
    else:
        context["confronto_storico"] = f"Rendimento {ra:.2f}%: Sopra il worst case storico"
    
    return context


def format_currency(value: float) -> str:
    """
    Converte un numero in formato euro con separatori di migliaia.
    Esempio: 1234567.89 -> "€ 1.234.568"
    """
    formatted = f"€ {value:,.0f}"
    formatted = formatted.replace(",", ".")
    return formatted


def format_percentage(value: float) -> str:
    """
    Converte un decimale in percentuale formattata.
    Esempio: 0.0523 -> "5.23%"
    """
    return f"{value * 100:.2f}%"


def create_summary_table(results: dict, initial_capital: float) -> list:
    """
    Crea i dati per la tabella riassuntiva dei percentili.
    """
    percentiles_final = results['percentiles_final']
    stats = results['stats']
    
    scenarios = [
        {
            'label': 'Ottimistico',
            'percentile_int': 75,
            'percentile': '75°',
            'value': percentiles_final['p75'],
            'cagr': stats['cagr_p75']
        },
        {
            'label': 'Mediano',
            'percentile_int': 50,
            'percentile': '50°',
            'value': percentiles_final['p50'],
            'cagr': stats['cagr_p50']
        },
        {
            'label': 'Conservativo',
            'percentile_int': 25,
            'percentile': '25°',
            'value': percentiles_final['p25'],
            'cagr': stats['cagr_p25']
        },
        {
            'label': 'Scenario 10% (Pessimistico)',
            'percentile_int': 10,
            'percentile': '10°',
            'value': percentiles_final['p10'],
            'cagr': stats['cagr_p10']
        },
        {
            'label': 'Scenario 7% (Severo)',
            'percentile_int': 7,
            'percentile': '7°',
            'value': percentiles_final['p7'],
            'cagr': stats['cagr_p7']
        },
        {
            'label': 'Scenario 5% (Molto Severo)',
            'percentile_int': 5,
            'percentile': '5°',
            'value': percentiles_final['p5'],
            'cagr': stats['cagr_p5']
        },
        {
            'label': 'Scenario 3% (Estremo)',
            'percentile_int': 3,
            'percentile': '3°',
            'value': percentiles_final['p3'],
            'cagr': stats['cagr_p3']
        }
    ]
    
    # Estrai numero simulazioni
    n_sims = results.get('n_sims', 1000)

    for scenario in scenarios:
        scenario['value_formatted'] = format_currency(scenario['value'])
        
        variation_decimal = (scenario['value'] / initial_capital) - 1
        scenario['variation'] = format_percentage(variation_decimal)
        
        scenario['cagr_formatted'] = format_percentage(scenario['cagr'])
        
        # Add Tail Risk Context if applicable
        cagr_percent = scenario['cagr'] * 100
        context = get_tail_risk_comment(scenario['percentile_int'], cagr_percent, n_sims)
        if context:
            scenario['context'] = context
    
    return scenarios


def prepare_plotly_data(results: dict) -> dict:
    """
    Converte i risultati numpy in liste Python per Plotly.
    """
    percentiles_time = results['percentiles_time']
    time = results['time']
    
    return {
        'time': time.tolist(),
        'p3': percentiles_time['p3'].tolist(),
        'p25': percentiles_time['p25'].tolist(),
        'p50': percentiles_time['p50'].tolist(),
        'p75': percentiles_time['p75'].tolist()
    }
