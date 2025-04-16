import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_excel('test-availability.xlsx')
#create datapoint_available column
df['datapoint_available']=df['Value'].notna().astype(int)

# --- Filter by a specific indicator ---
indicator_name = 'Population Size'
df_filtered = df[df['Indicator'] == indicator_name]

# --- Sex slicer ---
sex_options = df_filtered['Sex'].dropna().unique().tolist()
selected_sex = st.selectbox('Select Sex', sex_options)

# --- Filter by selected sex ---
df_filtered = df_filtered[df_filtered['Sex'] == selected_sex]

# Define full range of years
years_range = list(range(2010, 2025))

# Pivot and reindex to include all desired years
heatmap_data = df_filtered.pivot_table(
    index='Country',
    columns='Year',
    values='datapoint_available',
    aggfunc='max',
    fill_value=0
)

# Reindex the columns to include missing years (will fill with NaN or 0)
heatmap_data = heatmap_data.reindex(columns=years_range, fill_value=0)

# --- Plot the heatmap ---
plt.figure(figsize=(12, len(heatmap_data) * 0.4))
sns.heatmap(
    heatmap_data,
    cmap=sns.color_palette(['lightgrey', 'mediumseagreen']),
    cbar=False,
    linewidths=0.5,
    linecolor='white'
)
plt.title(f'Availability Heatmap: {indicator_name} ({selected_sex})')
plt.xlabel('Year')
plt.ylabel('Country')

# --- Show plot in Streamlit ---
st.pyplot(plt.gcf())