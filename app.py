"""
app.py
Assembla tutti i componenti e genera il report HTML completo standalone.
"""

from monte_carlo_engine import run_monte_carlo_simulation
from data_formatter import prepare_plotly_data, create_summary_table, format_currency
from chart_generator import create_monte_carlo_chart, COLORS


def generate_html_report(params: dict) -> str:
    """
    Genera report HTML completo con grafico e tabella.
    
    Args:
        params: dizionario parametri simulazione
        
    Returns:
        stringa HTML completa pronta da salvare
    """
    
    print("🔄 Eseguo simulazione Monte Carlo...")
    results = run_monte_carlo_simulation(params)
    
    print("📊 Preparo dati per visualizzazione...")
    plotly_data = prepare_plotly_data(results)
    
    print("🎨 Genero grafico interattivo...")
    fig = create_monte_carlo_chart(plotly_data, params)
    
    print("📋 Creo tabella scenari...")
    table_data = create_summary_table(results, params['capital'])
    
    # Converti grafico in HTML (usa CDN per plotly.js)
    chart_html = fig.to_html(
        include_plotlyjs='cdn',
        div_id='monte-carlo-chart',
        config={'displayModeBar': True, 'displaylogo': False}
    )
    
    # ========== COSTRUISCI RIGHE TABELLA ==========
    table_rows = ""
    for row in table_data:
        table_rows += f"""
                    <tr>
                        <td class="scenario-label">{row['label']}</td>
                        <td>{row['percentile']}</td>
                        <td class="value">{row['value_formatted']}</td>
                        <td class="positive">{row['variation']}</td>
                        <td>{row['cagr_formatted']}</td>
                    </tr>"""
    
    # ========== HTML COMPLETO ==========
    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simulazione Monte Carlo - Futura SCF</title>
    <style>
        /* ===== RESET E BASE ===== */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: Futura, Trebuchet MS, Helvetica, Arial, sans-serif;
            background-color: #f8f9fa;
            color: {COLORS['text']};
            line-height: 1.6;
            padding: 20px;
        }}
        
        /* ===== CONTAINER PRINCIPALE ===== */
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        }}
        
        /* ===== HEADER ===== */
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 2px solid {COLORS['primary_blue']};
        }}
        
        h1 {{
            color: {COLORS['primary_blue']};
            font-size: 32px;
            font-weight: 600;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            color: #666;
            font-size: 16px;
            font-weight: 300;
        }}
        
        /* ===== SEZIONE GRAFICO ===== */
        .chart-section {{
            margin: 40px 0;
        }}
        
        /* ===== SEZIONE TABELLA ===== */
        .table-section {{
            margin-top: 50px;
        }}
        
        h2 {{
            color: {COLORS['primary_blue']};
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid {COLORS['grid']};
        }}
        
        /* ===== TABELLA SCENARI ===== */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            font-size: 14px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}
        
        thead {{
            background-color: {COLORS['primary_blue']};
            color: white;
        }}
        
        th {{
            padding: 15px 12px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 0.5px;
        }}
        
        td {{
            padding: 15px 12px;
            border-bottom: 1px solid {COLORS['grid']};
        }}
        
        tbody tr:hover {{
            background-color: #f8f9fa;
            transition: background-color 0.2s ease;
        }}
        
        tbody tr:last-child td {{
            border-bottom: none;
        }}
        
        /* ===== STILI CELLE SPECIALI ===== */
        .scenario-label {{
            font-weight: 600;
            color: {COLORS['primary_blue']};
        }}
        
        .value {{
            font-weight: 600;
            color: {COLORS['text']};
        }}
        
        .positive {{
            color: {COLORS['green_optimistic']};
            font-weight: 500;
        }}
        
        /* ===== FOOTER ===== */
        .footer {{
            margin-top: 60px;
            padding-top: 30px;
            border-top: 2px solid {COLORS['grid']};
            text-align: center;
        }}
        
        .disclaimer {{
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px 20px;
            margin-bottom: 20px;
            font-size: 13px;
            text-align: left;
            border-radius: 4px;
        }}
        
        .disclaimer strong {{
            color: #856404;
            display: block;
            margin-bottom: 5px;
        }}
        
        .footer-text {{
            color: #666;
            font-size: 13px;
        }}
        
        .footer-text strong {{
            color: {COLORS['primary_blue']};
        }}
        
        /* ===== RESPONSIVE ===== */
        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
            }}
            
            h1 {{
                font-size: 24px;
            }}
            
            h2 {{
                font-size: 20px;
            }}
            
            table {{
                font-size: 12px;
            }}
            
            th, td {{
                padding: 10px 8px;
            }}
        }}
        
        /* ===== PRINT STYLES ===== */
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                box-shadow: none;
                padding: 20px;
            }}
            
            .footer {{
                page-break-before: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- HEADER -->
        <div class="header">
            <h1>📊 Simulazione Monte Carlo</h1>
            <p class="subtitle">Analisi Probabilistica Portafoglio {format_currency(params['capital'])}</p>
        </div>
        
        <!-- GRAFICO -->
        <div class="chart-section">
            {chart_html}
        </div>
        
        <!-- TABELLA SCENARI -->
        <div class="table-section">
            <h2>Scenari Probabilistici</h2>
            <p style="color: #666; margin-bottom: 15px; font-size: 14px;">
                Distribuzione dei possibili risultati finali dopo {params['years']} anni (10.000 simulazioni)
            </p>
            
            <table>
                <thead>
                    <tr>
                        <th>Scenario</th>
                        <th>Percentile</th>
                        <th>Valore Finale</th>
                        <th>Variazione</th>
                        <th>CAGR</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>
        
        <!-- FOOTER E DISCLAIMER -->
        <div class="footer">
            <div class="disclaimer">
                <strong>⚠️ Disclaimer Importante</strong>
                Questa simulazione è basata su ipotesi probabilistiche (rendimento atteso {params['mu']*100:.2f}%, 
                volatilità {params['sigma']*100:.2f}%) e modella la distribuzione storica dei rendimenti. 
                I risultati NON costituiscono garanzia di performance futura. I mercati finanziari sono soggetti 
                a rischi imprevedibili e eventi estremi che possono non essere catturati da modelli matematici.
            </div>
            
            <p class="footer-text">
                <strong>Futura SCF</strong> - Società di Consulenza Finanziaria<br>
                Consulenza Finanziaria Indipendente<br>
                Report generato il {__import__('datetime').datetime.now().strftime('%d/%m/%Y alle %H:%M')}
            </p>
        </div>
    </div>
</body>
</html>"""
    
    return html


# ========== ESECUZIONE PRINCIPALE ==========
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 GENERAZIONE REPORT MONTE CARLO - FUTURA SCF")
    print("=" * 60)
    print()
    
    # ===== PARAMETRI SIMULAZIONE =====
    params = {
        'capital': 400_000,      # Capitale iniziale in euro
        'mu': 0.0523,            # 5.23% rendimento annuo atteso
        'sigma': 0.0695,         # 6.95% volatilità annua
        'years': 30,             # Orizzonte 30 anni
        'n_sims': 10_000,        # 10.000 simulazioni
        'seed': 42               # Seed per riproducibilità
    }
    
    print("📝 Parametri simulazione:")
    print(f"   • Capitale iniziale: {format_currency(params['capital'])}")
    print(f"   • Rendimento atteso: {params['mu']*100:.2f}% annuo")
    print(f"   • Volatilità: {params['sigma']*100:.2f}% annua")
    print(f"   • Orizzonte temporale: {params['years']} anni")
    print(f"   • Numero simulazioni: {params['n_sims']:,}")
    print()
    
    # ===== GENERA REPORT =====
    html_content = generate_html_report(params)
    
    # ===== SALVA FILE =====
    output_filename = 'report_monte_carlo_futura_scf.html'
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print()
    print("=" * 60)
    print(f"✅ REPORT GENERATO CON SUCCESSO!")
    print("=" * 60)
    print(f"📄 File: {output_filename}")
    print(f"🌐 Apri il file nel browser per visualizzare")
    print()
    print("💡 Il report include:")
    print("   ✓ Grafico interattivo fan chart")
    print("   ✓ Tabella scenari (3°, 25°, 50°, 75° percentile)")
    print("   ✓ Stile professionale Futura SCF")
    print("   ✓ Responsive e stampabile")
    print()
