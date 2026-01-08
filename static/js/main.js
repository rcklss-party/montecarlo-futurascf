document.addEventListener('DOMContentLoaded', () => {
    // === DOM Elements ===
    const form = document.getElementById('simulationForm');
    const submitBtnAlloc = document.getElementById('submit-btn-alloc');
    const submitBtnParams = document.getElementById('submit-btn-params');
    const downloadBtn = document.getElementById('download-btn');

    // Helper to get current active submit button
    function getActiveSubmitBtn() {
        if (currentMode === 'params') return submitBtnParams;
        if (currentMode === 'allocation') return submitBtnAlloc;
        return null;
    }
    const viewToggleBtn = document.getElementById('view-toggle-btn');

    // Status
    const statusText = document.getElementById('statusText');
    const statusDot = document.querySelector('.status-dot');

    // Mode Logic
    const modeBoxes = document.querySelectorAll('.mode-box');
    let currentMode = null;
    let lastResults = null;
    let isFocusView = false;

    // === ASSET CONFIGURATION ===
    // Maps DOM ID suffix -> JSON Key in asset_data.json
    const ASSETS = [
        { id: 'sp500', key: 'sp500' },
        { id: 'exusa', key: 'world_ex_usa' },
        { id: 'em', key: 'emerging_markets' },
        { id: 'quality', key: 'quality' },
        { id: 'value', key: 'value' },
        { id: 'momentum', key: 'momentum' },
        { id: 'smallcap', key: 'small_cap' },
        { id: 'multifactor', key: 'multifactor' },
        { id: 'euro', key: 'euro_aggregate' },
        { id: 'glob', key: 'global_aggregate' },
        { id: 'gold', key: 'gold' }
    ];

    // PRESET DEFINITIONS
    const PRESETS = {
        conservative: {
            sp500: 20, exusa: 10, em: 0,
            quality: 0, value: 0, momentum: 0, smallcap: 0, multifactor: 0,
            euro: 40, glob: 20, gold: 10
        },
        balanced: {
            sp500: 40, exusa: 20, em: 5,
            quality: 0, value: 0, momentum: 0, smallcap: 0, multifactor: 0,
            euro: 15, glob: 10, gold: 10
        },
        aggressive: {
            sp500: 50, exusa: 20, em: 10,
            quality: 5, value: 5, momentum: 5, smallcap: 0, multifactor: 0,
            euro: 0, glob: 0, gold: 5
        }
    };

    // LAZY PORTFOLIOS DEFINITIONS
    const LAZY_PRESETS = {
        golden_butterfly: {
            sp500: 20, smallcap: 20,
            euro: 20, glob: 20, gold: 20,
            exusa: 0, em: 0, quality: 0, value: 0, momentum: 0, multifactor: 0
        },
        permanent: {
            sp500: 25,
            euro: 25, glob: 25, gold: 25,
            exusa: 0, em: 0, quality: 0, value: 0, momentum: 0, smallcap: 0, multifactor: 0
        },
        all_weather: {
            sp500: 30,
            glob: 40, euro: 15, gold: 15, // Simplified (Commodities -> Gold)
            exusa: 0, em: 0, quality: 0, value: 0, momentum: 0, smallcap: 0, multifactor: 0
        }
    };

    // Helper to safely set style
    function safeStyle(el, prop, val) {
        if (el && el.style) el.style[prop] = val;
    }

    // === SYNC LOGIC ===
    const syncMap = {
        'capital-manual': 'capital-alloc',
        'capital-alloc': 'capital-manual',
        'n_sims-manual': 'n_sims-alloc',
        'n_sims-alloc': 'n_sims-manual',
        'years-manual': 'years-alloc',
        'years-alloc': 'years-manual'
    };

    function attachSyncListeners() {
        for (let srcId in syncMap) {
            const srcEl = document.getElementById(srcId);
            if (srcEl) {
                srcEl.addEventListener('input', (e) => {
                    const targetId = syncMap[srcId];
                    const targetEl = document.getElementById(targetId);
                    if (targetEl) targetEl.value = e.target.value;
                    if (srcId.includes('years')) {
                        const slider = document.getElementById('yearsRange-alloc');
                        if (slider) slider.value = e.target.value;
                    }
                });
            }
        }
        const rangeAlloc = document.getElementById('yearsRange-alloc');
        if (rangeAlloc) {
            rangeAlloc.addEventListener('input', (e) => {
                const val = e.target.value;
                const targetEl1 = document.getElementById('years-alloc');
                const targetEl2 = document.getElementById('years-manual');
                if (targetEl1) targetEl1.value = val;
                if (targetEl2) targetEl2.value = val;
            });
        }
    }
    attachSyncListeners();

    // Listen to manual μ/σ inputs to update footer stats in real time
    function updateManualFooterStats() {
        if (currentMode !== 'params') return;
        const muEl = document.getElementById('mu');
        const sigmaEl = document.getElementById('sigma');
        const muVal = muEl ? parseFloat(muEl.value) : 5.23;
        const sigmaVal = sigmaEl ? parseFloat(sigmaEl.value) : 6.95;

        const calcMu = document.getElementById('calc-mu');
        const calcSigma = document.getElementById('calc-sigma');
        if (calcMu) calcMu.innerText = muVal.toFixed(2) + "%";
        if (calcSigma) calcSigma.innerText = sigmaVal.toFixed(2) + "%";
    }

    const muInput = document.getElementById('mu');
    const sigmaInput = document.getElementById('sigma');
    if (muInput) muInput.addEventListener('input', updateManualFooterStats);
    if (sigmaInput) sigmaInput.addEventListener('input', updateManualFooterStats);

    // === SELECTION LOGIC ===
    function setMode(mode) {
        currentMode = mode;
        modeBoxes.forEach(box => {
            const isSelected = box.dataset.mode === mode;
            if (isSelected) {
                box.classList.add('selected');
                const radio = box.querySelector('input[type="radio"]');
                if (radio) radio.checked = true;
            } else {
                box.classList.remove('selected');
                const radio = box.querySelector('input[type="radio"]');
                if (radio) radio.checked = false;
            }
        });

        // Toggle stats visibility based on mode
        const statsBox = document.querySelector('.global-stats-box');
        if (statsBox) {
            if (mode === 'params') {
                // In manual mode, show manual params in footer
                const muEl = document.getElementById('mu');
                const sigmaEl = document.getElementById('sigma');
                const muVal = muEl ? parseFloat(muEl.value) : 5.23;
                const sigmaVal = sigmaEl ? parseFloat(sigmaEl.value) : 6.95;

                // Update footer display
                const calcMu = document.getElementById('calc-mu');
                const calcSigma = document.getElementById('calc-sigma');
                const totalEl = document.getElementById('total-allocation');
                const fill = document.getElementById('allocation-fill');

                if (calcMu) calcMu.innerText = muVal.toFixed(2) + "%";
                if (calcSigma) calcSigma.innerText = sigmaVal.toFixed(2) + "%";
                if (totalEl) totalEl.innerText = "--";
                if (fill) fill.style.width = "0%";

                // Hide allocation bar, show only stats
                const allocStatus = statsBox.querySelector('.allocation-status');
                if (allocStatus) allocStatus.style.display = 'none';
            } else {
                // In allocation mode, show allocation stats
                const allocStatus = statsBox.querySelector('.allocation-status');
                if (allocStatus) allocStatus.style.display = 'flex';
                recalcAllocation();
            }
        }

        updateStatus(`Modalità: ${mode === 'params' ? 'Parametri Manuali' : 'Asset Allocation'}`, 'processing');
        validateState();
    }

    modeBoxes.forEach(box => {
        const header = box.querySelector('.mode-header');
        if (header) {
            header.addEventListener('click', () => setMode(box.dataset.mode));
        }
    });

    // === VIEW TOGGLE LOGIC ===
    if (viewToggleBtn) {
        viewToggleBtn.addEventListener('click', () => {
            isFocusView = !isFocusView;
            if (isFocusView) {
                viewToggleBtn.classList.add('active-view');
            } else {
                viewToggleBtn.classList.remove('active-view');
            }
            if (lastResults) {
                renderTable(lastResults);
            }
        });
    }

    // === ASSET ALLOCATION LOGIC ===
    let assetData = null;

    function loadAssetData() {
        fetch('/static/asset_data.json?t=' + new Date().getTime())
            .then(r => r.json())
            .then(data => {
                assetData = data;
                console.log("Assets loaded");
                recalcAllocation();
            })
            .catch(e => console.error("Asset load error", e));
    }
    loadAssetData();

    // -- ACCORDION LOGIC (Exclusive: only one open at a time) --
    document.querySelectorAll('.accordion-header').forEach(header => {
        header.addEventListener('click', () => {
            const section = header.parentElement;
            const isOpen = section.classList.contains('open');

            // Close all other sections first
            document.querySelectorAll('.accordion-section').forEach(s => {
                if (s !== section) s.classList.remove('open');
            });

            // Toggle current section
            if (!isOpen) {
                section.classList.add('open');
            } else {
                section.classList.remove('open');
            }
        });
    });

    // -- PRESET LOGIC --
    document.querySelectorAll('.preset-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const presetKey = btn.dataset.preset;
            const preset = PRESETS[presetKey];
            if (preset) {
                // Remove active class from all
                document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                // Apply values
                for (let asset of ASSETS) {
                    const val = preset[asset.id] !== undefined ? preset[asset.id] : 0;
                    const el = document.getElementById(`weight-${asset.id}`);
                    if (el) {
                        el.value = val;
                        const disp = document.getElementById(`weight-${asset.id}-val`);
                        if (disp) disp.innerText = val + "%";
                    }
                }
                recalcAllocation();
            }
        });
    });

    // -- LAZY PORTFOLIO LOGIC --
    const lazySelect = document.getElementById('lazy-portfolios');
    if (lazySelect) {
        lazySelect.addEventListener('change', (e) => {
            const presetKey = e.target.value;
            const preset = LAZY_PRESETS[presetKey];
            if (preset) {
                // Deselect main preset buttons
                document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));

                // Apply values
                for (let asset of ASSETS) {
                    const val = preset[asset.id] !== undefined ? preset[asset.id] : 0;
                    const el = document.getElementById(`weight-${asset.id}`);
                    if (el) {
                        el.value = val;
                        const disp = document.getElementById(`weight-${asset.id}-val`);
                        if (disp) disp.innerText = val + "%";
                    }
                }
                recalcAllocation();
            }
        });
    }

    // -- CALCULATION LOGIC --
    function getWeight(id) {
        const el = document.getElementById(`weight-${id}`);
        return el ? parseInt(el.value) : 0;
    }

    function recalcAllocation() {
        let total = 0;
        const sectionTotals = {};

        // 1. Update Display & Calc Totals
        ASSETS.forEach(asset => {
            const val = getWeight(asset.id);
            const disp = document.getElementById(`weight-${asset.id}-val`);
            if (disp) disp.innerText = val + "%";

            total += val;

            // Section Totals
            const el = document.getElementById(`weight-${asset.id}`);
            if (el) {
                const cat = el.dataset.category;
                if (cat) {
                    if (!sectionTotals[cat]) sectionTotals[cat] = 0;
                    sectionTotals[cat] += val;
                }
            }
        });

        // 2. Update Section Headers
        for (let cat in sectionTotals) {
            const span = document.getElementById(`total-${cat}`);
            if (span) span.innerText = sectionTotals[cat] + "%";
        }

        // 3. Update Main Total Bar
        const fill = document.getElementById('allocation-fill');
        const totalTxt = document.getElementById('total-allocation');
        const icon = document.getElementById('allocation-status-icon');

        if (totalTxt) totalTxt.innerText = total;
        if (fill) {
            fill.style.width = Math.min(total, 100) + "%";
            if (total === 100) {
                fill.style.backgroundColor = 'var(--green-optimistic)';
                if (icon) icon.innerHTML = '<i class="fa-solid fa-check-circle" style="color:var(--green-optimistic)"></i>';
            } else if (total > 100) {
                fill.style.backgroundColor = 'var(--red-pessimistic)';
                if (icon) icon.innerHTML = '<i class="fa-solid fa-circle-exclamation" style="color:var(--red-pessimistic)"></i>';
            } else {
                fill.style.backgroundColor = 'var(--accent-orange)';
                if (icon) icon.innerHTML = '';
            }
        }

        // 4. Calculate Portfolio Stats (Mu, Sigma)
        if (assetData && assetData.stats) {
            let portMu = 0;
            let portVar = 0;

            // Vectors
            const w = ASSETS.map(a => getWeight(a.id) / 100);
            const mu = ASSETS.map(a => assetData.stats[a.key]?.mu || 0);
            const sigma = ASSETS.map(a => assetData.stats[a.key]?.sigma || 0);
            const names = ASSETS.map(a => assetData.stats[a.key]?.name || a.key); // for correlation lookup key usually needs mapping

            // BUT asset_data.json keys for stats match keys used here (e.g. 'sp500').
            // Correlation matrix usually uses full names or keys? 
            // In previous export_asset_data: 
            // stats uses keys: "sp500", "world_ex_usa"
            // correlations uses keys: "S&P 500", "World ex USA" (names!)
            // We need to map properly.

            // Let's rely on mapping. assetData.stats[key].name gives the name used in correlation matrix

            const corrKeys = ASSETS.map(a => assetData.stats[a.key]?.name || "");

            // Calc Expected Return
            for (let i = 0; i < w.length; i++) {
                portMu += w[i] * mu[i];
            }

            // Calc Variance
            for (let i = 0; i < w.length; i++) {
                for (let j = 0; j < w.length; j++) {
                    let rho = 0;
                    if (corrKeys[i] && corrKeys[j]) {
                        // Check correlation availability (symmetric)
                        if (assetData.correlations && assetData.correlations[corrKeys[i]]) {
                            rho = assetData.correlations[corrKeys[i]][corrKeys[j]] || 0;
                        }
                    }
                    // If i==j rho is 1
                    if (i === j) rho = 1;

                    portVar += w[i] * w[j] * rho * sigma[i] * sigma[j];
                }
            }
            const portSigma = Math.sqrt(portVar);

            const muEl = document.getElementById('calc-mu');
            const sigmaEl = document.getElementById('calc-sigma');
            if (muEl) muEl.innerText = (portMu * 100).toFixed(2) + "%";
            if (sigmaEl) sigmaEl.innerText = (portSigma * 100).toFixed(2) + "%";

            if (form) {
                form.dataset.calcMu = (portMu * 100).toFixed(4);
                form.dataset.calcSigma = (portSigma * 100).toFixed(4);
            }
        }
        validateState(total);
    }

    function validateState(passedTotal) {
        const msgEl = document.getElementById('validation-message');
        if (msgEl) { msgEl.classList.remove('show'); msgEl.style.display = 'none'; }

        // Disable both buttons by default
        if (submitBtnAlloc) submitBtnAlloc.disabled = true;
        if (submitBtnParams) submitBtnParams.disabled = true;

        if (!currentMode) {
            if (submitBtnAlloc) submitBtnAlloc.title = "Seleziona una modalità";
            if (submitBtnParams) submitBtnParams.title = "Seleziona una modalità";
            return;
        }

        if (currentMode === 'params') {
            if (submitBtnParams) {
                submitBtnParams.disabled = false;
                submitBtnParams.title = "";
            }
            return;
        }

        if (currentMode === 'allocation') {
            let total = 0;
            if (passedTotal !== undefined) total = passedTotal;
            else {
                ASSETS.forEach(a => total += getWeight(a.id));
            }

            if (total !== 100) {
                if (msgEl) {
                    msgEl.innerText = `Il totale deve essere 100% (Attuale: ${total}%)`;
                    msgEl.style.display = 'block';
                    msgEl.classList.add('show');
                }
                if (submitBtnAlloc) submitBtnAlloc.title = "Correggi allocazione";
            } else {
                if (submitBtnAlloc) {
                    submitBtnAlloc.disabled = false;
                    submitBtnAlloc.title = "";
                }
            }
        }
    }

    // Attach Listeners to Sliders
    ASSETS.forEach(asset => {
        const el = document.getElementById(`weight-${asset.id}`);
        if (el) el.addEventListener('input', recalcAllocation);
    });

    // === SIMULATION RUN ===
    async function runSimulation() {
        const submitBtn = getActiveSubmitBtn();
        if (!submitBtn || submitBtn.disabled) return;
        setLoading(true);
        updateStatus('Simulazione in corso...', 'processing');

        try {
            const suffix = currentMode === 'params' ? '-manual' : '-alloc';
            const capitalEl = document.getElementById(`capital${suffix}`);
            const yearsEl = document.getElementById(`years${suffix}`);
            const simsEl = document.getElementById(`n_sims${suffix}`);

            const data = {
                capital: capitalEl ? capitalEl.value : 400000,
                years: yearsEl ? yearsEl.value : 30,
                n_sims: simsEl ? simsEl.value : 1000
            };

            if (currentMode === 'params') {
                const muEl = document.getElementById('mu');
                const sigmaEl = document.getElementById('sigma');
                data.mu = muEl ? muEl.value : 5.23;
                data.sigma = sigmaEl ? sigmaEl.value : 6.95;
            } else {
                data.mu = form.dataset.calcMu;
                data.sigma = form.dataset.calcSigma;
            }

            const response = await fetch('/simulate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (!response.ok) throw new Error('Simulazione fallita');
            const result = await response.json();

            lastResults = result.table; // Save for view toggle
            renderChart(JSON.parse(result.chart));
            if (result.distribution) {
                renderDistributionChart(result.distribution, result.table);
            }
            renderTable(lastResults);

            const emptyState = document.getElementById('empty-state');
            if (emptyState) emptyState.style.display = 'none';
            const emptyRow = document.getElementById('empty-table-row');
            if (emptyRow) emptyRow.style.display = 'none';
            if (downloadBtn) downloadBtn.disabled = false;

            updateStatus('Simulazione completata!', 'success');

        } catch (error) {
            console.error(error);
            updateStatus('Errore: ' + error.message, 'error');
        } finally {
            setLoading(false);
        }
    }

    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            runSimulation();
        });
    }

    window.downloadChart = function () {
        Plotly.downloadImage('plotlyChart', {
            format: 'png', filename: 'monte_carlo_proiezione', height: 800, width: 1200
        });
    }

    function setLoading(isLoading) {
        const submitBtn = getActiveSubmitBtn();
        if (!submitBtn) return;
        const loader = submitBtn.querySelector('.loader');
        const btnText = submitBtn.querySelector('.btn-text');

        submitBtn.disabled = isLoading;
        if (isLoading) {
            if (loader) loader.style.display = 'inline-block';
            if (btnText) btnText.textContent = 'Calcolo...';
        } else {
            if (loader) loader.style.display = 'none';
            if (btnText) btnText.textContent = 'Esegui Simulazione';
        }
    }

    function updateStatus(msg, type) {
        if (statusText) statusText.textContent = msg;
        if (statusDot) {
            statusDot.style.background = '#ccc';
            if (type === 'success') statusDot.style.background = '#22c55e';
            if (type === 'processing') statusDot.style.background = '#eab308';
            if (type === 'error') statusDot.style.background = '#ef4444';
        }
    }

    function renderChart(graphData) {
        Plotly.newPlot('plotlyChart', graphData.data, graphData.layout, {
            responsive: true, displayModeBar: false
        });
    }

    function renderDistributionChart(distData, tableData) {
        const p50 = tableData.find(r => r.percentile_int === 50);
        const p75 = tableData.find(r => r.percentile_int === 75);
        const p25 = tableData.find(r => r.percentile_int === 25);
        const p3 = tableData.find(r => r.percentile_int === 3);

        const curveTrace = {
            x: distData.x,
            y: distData.y,
            type: 'scatter',
            mode: 'lines',
            fill: 'tozeroy',
            line: { color: '#e2e8f0', width: 2, shape: 'spline' },
            fillcolor: 'rgba(226, 232, 240, 0.5)',
            hoverinfo: 'y+x',
            hovertemplate: '<b>CAGR: %{x:.1%}</b><br>Frequenza: %{y:.1%} dei casi<extra></extra>'
        };

        const shapes = [];
        const annotations = [];
        const markerX = [];
        const markerY = [];
        const markerColors = [];
        const markerTexts = [];

        function addMarker(row, color, label, position = 'top') {
            if (!row) return;
            const xVal = row.cagr;

            shapes.push({
                type: 'line',
                x0: xVal,
                x1: xVal,
                y0: 0,
                y1: 1,
                yref: 'paper',
                line: { color: color, width: 2, dash: 'dot' }
            });

            annotations.push({
                x: xVal,
                y: position === 'top' ? 1 : 0.05,
                yref: 'paper',
                text: label || row.percentile,
                showarrow: false,
                font: { color: color, size: 10, weight: 'bold' },
                yshift: position === 'top' ? 10 : 10
            });

            // Interactive Point
            markerX.push(xVal);
            // Approx Y
            let closestY = 0;
            let minDiff = Infinity;
            let idx = 0;
            for (let i = 0; i < distData.x.length; i++) {
                const diff = Math.abs(distData.x[i] - xVal);
                if (diff < minDiff) { minDiff = diff; idx = i; }
            }
            closestY = distData.y[idx];

            markerY.push(closestY);
            markerColors.push(color);

            const p = row.percentile_int;
            const text = `
<b>CAGR ${label}: ${(row.cagr * 100).toFixed(1)}%</b><br>
Percentile: ${p}°<br>
${p}% dei casi sotto questo valore<br>
${100 - p}% dei casi sopra questo valore
            `.trim();
            markerTexts.push(text);
        }

        addMarker(p50, '#1e3a5f', 'Mediano', 'top');
        addMarker(p75, '#16a34a', 'Ottimistico', 'top');
        addMarker(p25, '#e88734', 'Conservativo', 'top');
        addMarker(p3, '#ef4444', 'Estremo', 'top');

        const markersTrace = {
            x: markerX,
            y: markerY,
            type: 'scatter',
            mode: 'markers',
            marker: { color: markerColors, size: 8, symbol: 'circle' },
            hoverinfo: 'text',
            hovertext: markerTexts,
            showlegend: false
        };

        let xMin = distData.x[0];
        let xMax = distData.x[distData.x.length - 1];

        if (p3 && p75) {
            const spread = p75.cagr - p3.cagr;
            xMin = p3.cagr - (spread * 0.2);
            xMax = p75.cagr + (spread * 0.2);
        }

        const layout = {
            margin: { l: 40, r: 20, t: 30, b: 30 },
            title: { text: 'Distribuzione Rendimenti Annuali (CAGR)', font: { size: 14 } },
            showlegend: false,
            xaxis: {
                showgrid: false, zeroline: false, showticklabels: true, tickformat: '.1%',
            },
            yaxis: {
                showgrid: false, zeroline: false, showticklabels: false
            },
            shapes: shapes,
            annotations: annotations,
            height: 250,
            hovermode: 'closest'
        };

        if (xMin < xMax) {
            layout.xaxis.range = [xMin, xMax];
        }

        Plotly.newPlot('distributionChart', [curveTrace, markersTrace], layout, { responsive: true, displayModeBar: false });
    }

    function renderTable(data) {
        const tbody = document.querySelector('#resultsTable tbody');
        if (!tbody) return;
        tbody.innerHTML = '';

        let displayData = [...data];
        const table = document.querySelector('#resultsTable');

        if (isFocusView) {
            table.classList.add('prob-focus');
            const p50 = displayData.find(r => r.percentile_int === 50);
            const p25 = displayData.find(r => r.percentile_int === 25);
            const p75 = displayData.find(r => r.percentile_int === 75);
            const others = displayData.filter(r => ![25, 50, 75].includes(r.percentile_int));

            displayData = [];
            if (p50) displayData.push(p50);
            if (p75) displayData.push(p75);
            if (p25) displayData.push(p25);
            displayData = displayData.concat(others);

        } else {
            table.classList.remove('prob-focus');
        }

        displayData.forEach(row => {
            const tr = document.createElement('tr');
            const isPos = !row.variation.includes('-');

            if (isFocusView) {
                if (row.percentile_int === 50) tr.classList.add('prob-row-large');
                else if ([25, 75].includes(row.percentile_int)) tr.classList.add('prob-row-medium');
                else tr.classList.add('prob-row-small');
            }

            let labelHtml = row.label;
            if (row.context) {
                labelHtml += `
                    <div class="tooltip-container">
                        <i class="fa-solid fa-circle-info scenario-tooltip-icon"></i>
                        <div class="tooltip-text">
                            <div class="tooltip-header"><i class="fa-solid fa-triangle-exclamation"></i> ${row.context.commento.split(':')[0]}</div>
                            <div class="tooltip-body">${row.context.commento.split(':')[1] || row.context.commento}</div>
                            <div class="tooltip-metric">${row.context.confronto_storico}</div>
                            <div class="tooltip-footer">
                                <div><strong>Probabilità:</strong> ${row.context.probabilita_descrittiva}</div>
                                <div style="margin-top:4px; font-style:italic;">Note: ${row.context.nota_tecnica}</div>
                            </div>
                        </div>
                    </div>
                `;
            }

            tr.innerHTML = `
                <td>${labelHtml}</td>
                <td>${row.percentile}</td>
                <td><strong>${row.value_formatted}</strong></td>
                <td style="color: ${isPos ? '#16a34a' : '#dc2626'}">${row.variation}</td>
                <td>${row.cagr_formatted}</td>
            `;
            tbody.appendChild(tr);
        });

        // Attach click handlers for tooltips
        attachTooltipClickHandlers();
    }

    // === TOOLTIP CLICK TOGGLE LOGIC ===
    function attachTooltipClickHandlers() {
        document.querySelectorAll('.tooltip-container .scenario-tooltip-icon').forEach(icon => {
            icon.addEventListener('click', (e) => {
                e.stopPropagation();
                const container = icon.closest('.tooltip-container');
                const isActive = container.classList.contains('active');

                // Close all other tooltips first
                document.querySelectorAll('.tooltip-container.active').forEach(tc => {
                    tc.classList.remove('active');
                });

                // Toggle this one
                if (!isActive) {
                    container.classList.add('active');
                }
            });
        });
    }

    // Close tooltips when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.tooltip-container')) {
            document.querySelectorAll('.tooltip-container.active').forEach(tc => {
                tc.classList.remove('active');
            });
        }
    });

    validateState();
});
