# WellnessWise — Your Daily Wellness Companion

## Files
- `dashboard.py`: main app and all six pages.
- `data_utils.py`: loads and prepares the CSV, date filtering, averages.
- `theme_config.py`: Blush Pink, Ocean Blue, Midnight Purple themes.
- `data/`: put Emily's CSV and data dictionary here.
- `charts/`: optional assets; Plotly charts are generated directly in the app.

## Setup
1. Put `PJ2_Emily_Park_wellness_2025.csv` inside `data/`.
2. Open this folder in VS Code.
3. In the terminal run: `python -m pip install -r requirements.txt`
4. Then run: `python -m streamlit run dashboard.py`

The dashboard expects the CSV filename above and recognizes common column-name variations. It displays a helpful warning if the CSV is missing. The data dictionary is for reference and does not need to be imported into Python. The dashboard is educational, not medical advice.
