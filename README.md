cat > README.md <<'EOF'
# Plotly Dashboards (Synthetic Data)

Small, reproducible examples that generate synthetic datasets with NumPy/Pandas and visualize them with Plotly.

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/data_gen.py
python scripts/viz.py
# open outputs/dashboard.html
