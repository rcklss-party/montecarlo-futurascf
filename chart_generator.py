"""
chart_generator.py
Genera il grafico Monte Carlo con lo stile professionale di Futura SCF.
"""

import plotly.graph_objects as go
from data_formatter import format_currency


# ========== COLORI BRAND FUTURA SCF ==========
# Palette professionale dedotta dal sito futurascf.it
COLORS = {
    'primary_blue': '#1e3a5f',           # Blu navy (colore principale)
    'accent_orange': '#e88734',          # Arancione caldo (accenti)
    'light_blue': '#5b8bb5',             # Blu chiaro per mediana
    'green_optimistic': '#6ba368',       # Verde per scenario positivo
    'red_pessimistic': '#d65252',        # Rosso per scenario negativo
    'gray_area': 'rgba(91, 139, 181, 0.15)',  # Area trasparente p25-p75
    'background': '#ffffff',             # Sfondo bianco
    'grid': '#e8e8e8',                   # Linee griglia grigio chiaro
    'text': '#2c3e50'                    # Testo grigio scuro
}

# Font professionale
FONT = {
    'family': 'Futura, Trebuchet MS, Helvetica, Arial, sans-serif',
    'size': 13,
    'color': COLORS['text']
}


def create_monte_carlo_chart(plotly_data: dict, params: dict) -> go.Figure:
    """
    Crea il fan chart Monte Carlo con percentili evidenziati.
    
    Args:
        plotly_data: output di prepare_plotly_data() con le liste dei percentili
        params: parametri simulazione (capital, mu, sigma, years, n_sims)
        
    Returns:
        oggetto plotly Figure pronto per visualizzazione o esportazione
    """
    
    # Crea figura Plotly vuota
    fig = go.Figure()
    
    # ========== 1) AREA OMBREGGIATA P25-P75 (50% probabilità) ==========
    # Prima traccia: bordo superiore (p75) - invisibile
    fig.add_trace(go.Scatter(
        x=plotly_data['time'],
        y=plotly_data['p75'],
        mode='lines',
        line=dict(width=0),          # Linea invisibile
        showlegend=False,             # Non mostrare in legenda
        hoverinfo='skip'              # Non mostrare hover
    ))
    
    # Seconda traccia: bordo inferiore (p25) - riempie area fino a p75
    fig.add_trace(go.Scatter(
        x=plotly_data['time'],
        y=plotly_data['p25'],
        mode='lines',
        line=dict(width=0),
        fillcolor=COLORS['gray_area'],   # Colore area trasparente
        fill='tonexty',                   # Riempie fino alla traccia precedente (p75)
        name='Area 25°-75° percentile',
        hovertemplate='<b>Anno:</b> %{x:.1f}<br><b>Valore:</b> €%{y:,.0f}<extra></extra>'
    ))
    
    # ========== 2) LINEA MEDIANA (P50) - PRINCIPALE ==========
    fig.add_trace(go.Scatter(
        x=plotly_data['time'],
        y=plotly_data['p50'],
        mode='lines',
        name='Mediana (50° percentile)',
        line=dict(
            color=COLORS['light_blue'],
            width=3                       # Linea spessa per evidenza
        ),
        hovertemplate='<b>Anno:</b> %{x:.1f}<br><b>Valore:</b> €%{y:,.0f}<extra></extra>'
    ))
    
    # ========== 3) P3 PESSIMISTICO (linea tratteggiata rossa) ==========
    fig.add_trace(go.Scatter(
        x=plotly_data['time'],
        y=plotly_data['p3'],
        mode='lines',
        name='3° percentile (pessimistico)',
        line=dict(
            color=COLORS['red_pessimistic'],
            width=2,
            dash='dash'                   # Linea tratteggiata
        ),
        hovertemplate='<b>Anno:</b> %{x:.1f}<br><b>Valore:</b> €%{y:,.0f}<extra></extra>'
    ))
    
    # ========== 4) P75 OTTIMISTICO (linea punteggiata verde) ==========
    fig.add_trace(go.Scatter(
        x=plotly_data['time'],
        y=plotly_data['p75'],
        mode='lines',
        name='75° percentile (ottimistico)',
        line=dict(
            color=COLORS['green_optimistic'],
            width=1.5,
            dash='dot'                    # Linea punteggiata
        ),
        hovertemplate='<b>Anno:</b> %{x:.1f}<br><b>Valore:</b> €%{y:,.0f}<extra></extra>'
    ))
    
    # ========== 5) LINEA CAPITALE INIZIALE (riferimento) ==========
    fig.add_hline(
        y=params['capital'],
        line_dash='dash',
        line_color='rgba(0,0,0,0.3)',     # Grigio trasparente
        line_width=1,
        annotation_text=f"Capitale iniziale ({format_currency(params['capital'])})",
        annotation_position='right',
        annotation_font=dict(size=11, color='gray')
    )
    
    # ========== 6) LAYOUT E STILE PROFESSIONALE ==========
    fig.update_layout(
        # Titolo principale
        title={
            'text': f"Simulazione Monte Carlo - Portafoglio {format_currency(params['capital'])}",
            'x': 0.5,                     # Centra titolo
            'xanchor': 'center',
            'font': dict(
                size=18,
                family=FONT['family'],
                color=COLORS['primary_blue'],
                weight='bold'
            )
        },
        
        # Sottotitolo con parametri
        annotations=[{
            'text': (
                f"10.000 simulazioni | "
                f"Rendimento atteso: {params['mu']*100:.2f}% | "
                f"Volatilità: {params['sigma']*100:.2f}% | "
                f"Orizzonte: {params['years']} anni"
            ),
            'xref': 'paper',
            'yref': 'paper',
            'x': 0.5,
            'y': 1.08,                    # Posiziona sopra il grafico
            'showarrow': False,
            'font': dict(size=12, color='gray'),
            'xanchor': 'center'
        }],
        
        # Asse X (tempo)
        xaxis=dict(
            title='Anni',
            showgrid=True,
            gridcolor=COLORS['grid'],
            tickfont=FONT,
            title_font=FONT,
            zeroline=False
        ),
        
        # Asse Y (valore portafoglio)
        yaxis=dict(
            title='Valore Portafoglio (€)',
            showgrid=True,
            gridcolor=COLORS['grid'],
            tickformat=',.0f',            # Formato migliaia: 1,234,567
            tickfont=FONT,
            title_font=FONT,
            zeroline=False
        ),
        
        # Colori sfondo
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        
        # Legenda
        legend=dict(
            x=0.02,                       # Sinistra
            y=0.98,                       # Alto
            bgcolor='rgba(255,255,255,0.9)',  # Bianco semi-trasparente
            bordercolor=COLORS['grid'],
            borderwidth=1,
            font=FONT
        ),
        
        # Hover unificato su asse X
        hovermode='x unified',
        
        # Dimensioni responsive
        autosize=True,
        # height=600,  <-- RIMOSSO per adattarsi al container
        margin=dict(t=80, b=40, l=60, r=40) # Margini ridotti
    )
    
    return fig


# ========== TEST DEL MODULO ==========
if __name__ == "__main__":
    print("🧪 Test generazione grafico Monte Carlo...")
    
    # Importa moduli necessari
    from monte_carlo_engine import run_monte_carlo_simulation
    from data_formatter import prepare_plotly_data
    
    # Parametri di test
    params = {
        'capital': 400_000,
        'mu': 0.0523,
        'sigma': 0.0695,
        'years': 30,
        'n_sims': 10_000,
        'seed': 42
    }
    
    print("📊 Eseguo simulazione...")
    results = run_monte_carlo_simulation(params)
    
    print("🎨 Preparo dati per grafico...")
    plotly_data = prepare_plotly_data(results)
    
    print("📈 Genero grafico...")
    fig = create_monte_carlo_chart(plotly_data, params)
    
    # Salva HTML standalone
    output_file = 'monte_carlo_chart.html'
    fig.write_html(output_file)
    
    print(f"✅ Grafico salvato in: {output_file}")
    print("🌐 Apri il file nel browser per visualizzare")
    
    # Mostra info percentili
    print("\n📊 Valori finali (anno 30):")
    pf = results['percentiles_final']
    print(f"  3° percentile:  {format_currency(pf['p3'])}")
    print(f"  25° percentile: {format_currency(pf['p25'])}")
    print(f"  50° percentile: {format_currency(pf['p50'])} (mediana)")
    print(f"  75° percentile: {format_currency(pf['p75'])}")
