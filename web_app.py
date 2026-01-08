from flask import Flask, render_template, request, jsonify
import json
import plotly
from monte_carlo_engine import run_monte_carlo_simulation
from chart_generator import create_monte_carlo_chart
from data_formatter import prepare_plotly_data, create_summary_table

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        # Get parameters from request
        data = request.json
        params = {
            'capital': float(data.get('capital', 400000)),
            'mu': float(data.get('mu', 5.23)) / 100,  # Convert percentage to decimal
            'sigma': float(data.get('sigma', 6.95)) / 100, # Convert percentage to decimal
            'years': int(data.get('years', 30)),
            'n_sims': int(data.get('n_sims', 1000)),
            'seed': 42 # Optional: make this random or user-selectable? For now fixed for reproducibility as per original
        }

        # Run simulation
        results = run_monte_carlo_simulation(params)
        
        # Prepare chart
        plotly_data = prepare_plotly_data(results)
        fig = create_monte_carlo_chart(plotly_data, params)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Prepare table
        table_data = create_summary_table(results, params['capital'])
        
        return jsonify({
            'status': 'success',
            'chart': graphJSON,
            'table': table_data,
            'distribution': results.get('distribution')
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    print("Starting Main App on 5003 (Production Mode)...")
    app.run(host='0.0.0.0', debug=False, port=5003)
