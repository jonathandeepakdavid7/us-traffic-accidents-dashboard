#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
import pandas as pd
import plotly.express as px

# Configure the dashboard
st.set_page_config(
    page_title="US Traffic Accidents Dashboard",
    layout="wide"
)

# Load the cleaned dataset
@st.cache_data
def load_data():
    return pd.read_csv(
        "US_Accidents_clean.csv",
        parse_dates=["Start_Time", "Year_Month"]
    )

df = load_data()

# Dashboard title and introduction
st.title("US Traffic Accidents Dashboard")

st.write(
    "Explore reported traffic accidents across the United States "
    "by location, severity, weather conditions, and time."
)

st.caption(
    "Data: 2% random sample of US Accidents (2016–March 2023). "
    "Reported accident counts do not represent accident risk."
)

# Display initial dataset information
# Sidebar: State Filter
st.sidebar.header("Dashboard Filters")

state_options = sorted(df["State"].unique())

selected_states = st.sidebar.multiselect(
    "Select States",
    options=state_options,
    help="Leave empty to display all states."
)

# Filter the dataset by selected states
if selected_states:
    filtered_df = df[df["State"].isin(selected_states)].copy()
else:
    filtered_df = df.copy()

# Sidebar: Severity Filter
selected_severities = st.sidebar.multiselect(
    "Select Severity Levels",
    options=[1, 2, 3, 4],
    default=[1, 2, 3, 4],
    help="1 = least severe; 4 = most severe"
)

# Apply the severity filter
filtered_df = filtered_df[
    filtered_df["Severity"].isin(selected_severities)
]

# Sidebar: Year Range Filter
min_year = int(df["Year"].min())
max_year = int(df["Year"].max())

selected_years = st.sidebar.slider(
    "Select Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Apply the year range filter
filtered_df = filtered_df[
    filtered_df["Year"].between(
        selected_years[0],
        selected_years[1]
    )
]

# Display the number of accidents after all three filters
st.metric(
    "Accidents Matching Filters",
    f"{len(filtered_df):,}"
)

# Handle filters that return no matching accidents
if filtered_df.empty:
    st.warning("No accidents match the selected filters.")
    st.stop()

# Dynamic Key Insights
st.subheader("Key Insights")

# Identify the most common severity level
top_severity = filtered_df["Severity"].value_counts()
most_common_severity = top_severity.idxmax()
severity_count = top_severity.max()

severity_percentage = (
    severity_count / len(filtered_df) * 100
)

st.write(
    f"**Severity:** Level {most_common_severity} is the "
    f"most frequently reported severity, with "
    f"{severity_count:,} accidents "
    f"({severity_percentage:.1f}% of selected records)."
)

# Identify the most common recorded weather condition
known_weather = filtered_df[
    filtered_df["Weather_Condition"].notna()
    & (filtered_df["Weather_Condition"] != "Unknown")
]

if not known_weather.empty:
    top_weather = known_weather["Weather_Condition"].value_counts()
    weather_name = top_weather.idxmax()
    weather_count = top_weather.max()

    st.write(
        f"**Weather:** {weather_name} is the most frequently "
        f"recorded weather condition, appearing in "
        f"{weather_count:,} accidents with available "
        f"weather information."
    )
else:
    st.write("**Weather:** No recorded weather conditions are available.")

st.caption(
    "These findings describe reported accidents in the "
    "selected sample. They do not establish accident risk "
    "or prove that weather caused accidents."
)

# Visualization 1: Accident Severity Distribution
st.subheader("Accident Severity Distribution")

severity_counts = (
    filtered_df["Severity"]
    .value_counts()
    .reindex([1, 2, 3, 4], fill_value=0)
    .rename_axis("Severity")
    .reset_index(name="Accident Count")
)

severity_counts["Severity"] = (
    severity_counts["Severity"].astype(str)
)

fig_severity = px.bar(
    severity_counts,
    x="Severity",
    y="Accident Count",
    title="Reported Accidents by Severity Level",
    text_auto=True,
    labels={
        "Severity": "Severity Level",
        "Accident Count": "Number of Accidents"
    }
)

fig_severity.update_layout(
    yaxis_rangemode="tozero"
)

# Display severity levels as categories
fig_severity.update_xaxes(
    type="category",
    categoryorder="array",
    categoryarray=["1", "2", "3", "4"]
)

st.plotly_chart(fig_severity, use_container_width=True)

st.caption(
    "Severity ranges from 1 (least severe) to 4 (most severe). "
    "Counts reflect the selected filters."
)

# Visualization 2: Accident Location Map
st.subheader("Accident Location Map")

# Limit map points to maintain performance
map_df = filtered_df.sample(
    n=min(len(filtered_df), 3000),
    random_state=42
).copy()

# Treat severity levels as categories
map_df["Severity Level"] = map_df["Severity"].astype(str)

# Create interactive accident map
fig_map = px.scatter_map(
    map_df,
    lat="Start_Lat",
    lon="Start_Lng",
    center={"lat": 39.5, "lon": -98.35},
   color="Severity Level",
     category_orders={
        "Severity Level": ["1", "2", "3", "4"]
    },
    color_discrete_map={
        "1": "#2ca02c",
        "2": "#1f77b4",
        "3": "#ff7f0e",
        "4": "#d62728"
    },
    hover_name="State",
    hover_data=["Start_Time"],
    zoom=3,
    map_style="open-street-map",
    title="Geographic Distribution of Reported Accidents"
)


fig_map.update_layout(
    height=550,
    margin=dict(l=0, r=0, t=50, b=0)
)

st.plotly_chart(fig_map, use_container_width=True)

st.caption(
    f"Displaying {len(map_df):,} of "
    f"{len(filtered_df):,} filtered accident records. "
    "A reproducible random sample of up to 3,000 locations "
    "is used for map performance. "
    "Map density does not represent accident risk."
)

# Visualization 3: Weather Conditions
st.subheader("Accidents by Weather Condition")

# Find the 10 most common weather conditions
weather_counts = (
    filtered_df["Weather_Condition"]
    .fillna("Unknown")
    .value_counts()
    .head(10)
    .sort_values()
    .rename_axis("Weather Condition")
    .reset_index(name="Accident Count")
)

# Create a horizontal bar chart
fig_weather = px.bar(
    weather_counts,
    x="Accident Count",
    y="Weather Condition",
    orientation="h",
    title="Top 10 Recorded Weather Conditions",
    labels={
        "Accident Count": "Number of Accidents",
        "Weather Condition": "Weather Condition"
    }
)

fig_weather.update_layout(
    height=500,
    xaxis_rangemode="tozero"
)

st.plotly_chart(fig_weather, use_container_width=True)

st.caption(
    "Counts represent reported accidents under each weather "
    "condition within the selected filters. These comparisons "
    "do not establish whether weather caused accidents or "
    "which conditions are most dangerous."
)

# Visualization 4: Accident Trend Over Time
st.subheader("Accident Trends Over Time")

# Count accidents by month
monthly_counts = (
    filtered_df.groupby("Year_Month")
    .size()
    .reset_index(name="Accident Count")
    .sort_values("Year_Month")
)

# Create interactive line chart
fig_trend = px.line(
    monthly_counts,
    x="Year_Month",
    y="Accident Count",
    title="Monthly Reported Traffic Accidents",
    markers=True,
    labels={
        "Year_Month": "Month and Year",
        "Accident Count": "Number of Accidents"
    }
)

fig_trend.update_layout(
    yaxis_rangemode="tozero",
    hovermode="x unified",
    height=500
)

st.plotly_chart(fig_trend, use_container_width=True)

st.caption(
    "Monthly counts reflect the selected filters. "
    "The dataset begins in February 2016 and ends in March 2023. "
    "The first and last years are incomplete, and changes "
    "in reporting coverage may influence observed trends."
)
