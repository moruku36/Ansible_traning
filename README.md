# Ansible Practice and Stock Data Tools

[English](README.md) | [日本語](README.ja.md)

A mixed learning repository containing Ansible playbooks and roles, plus Python and Streamlit tools for fetching and visualizing Japanese stock data from Stooq and Yahoo Finance.

## Two areas of study

The repository name refers to Ansible practice: numbered playbooks, roles, templates, and `QUICKSTART.md` cover file operations, conditions, loops, handlers, and Docker environments. The existing application guide also covers Japanese stock data tools.

For the Python tools:

```bash
pip install -r requirements.txt
python main.py
# Alternatively, open the web interface:
streamlit run streamlit_app.py
```

The stock tools use pandas, pandas-datareader, yfinance, Streamlit, Plotly, and Matplotlib. They can retrieve OHLCV data, compare multiple symbols, draw candlestick and volume charts, and export CSV. Data availability and timeliness depend on the provider. The Japanese guide retains the original examples and symbol table.


## Contents

- [QUICKSTART.md](QUICKSTART.md)
- [roles/](roles)
- [templates/](templates)

## Detailed documentation

The [Japanese guide](README.ja.md) retains the complete original setup instructions, configuration, examples, project status, and limitations. Supporting documents keep their existing language.
