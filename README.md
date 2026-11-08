# US Traffic Accidents Dashboard

## Project Overview

This interactive Streamlit dashboard explores reported US traffic accidents from February 2016 through March 2023.

The dashboard includes filters for state, severity level, and year, along with four interactive Plotly visualizations.

## Dataset

Source: US Accidents (2016–2023), by Sobhan Moosavi, Kaggle.

https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents/

The original dataset contains 7,728,394 records. A reproducible 2% sample containing 154,568 records was prepared using Pandas.

The cleaned dataset is saved as `US_Accidents_clean.csv`.

## Dashboard Features

- State filtering
- Severity filtering (levels 1–4)
- Year range filtering
- Accident severity distribution
- Interactive accident location map
- Weather condition comparisons
- Monthly accident trends
- Dynamic key insights

## Running the Dashboard Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
streamlit run app.py
```

## Limitations

The dashboard reports accident counts rather than accident risk. Differences in traffic exposure and reporting coverage may affect comparisons.

The data ends in March 2023, so 2023 is incomplete. The map displays a sample of up to 3,000 filtered locations for performance.

## Live Dashboard

Public Streamlit URL: https://us-traffic-accidents-dashboard-git82xfycm245yrtcypz9g.streamlit.app/
