import pandas as pd
import streamlit as st
import plotly.express as px

# Load data
df = pd.read_excel("C:\\Users\\Admin\\OneDrive\\Desktop\\dashboard folder\\Trainer Information and Batch Monitoring Data.xlsx")
df.columns = df.columns.str.strip()

# Clean numeric columns
numeric_cols = [
    'Total Trainees Completed in batch 1', 'Males Completed in batch 1', 'Females Completed in batch 1',
    'Employed - Males from batch 1', 'Employed - Females from batch 1',
    'Unemployed - Males from batch 1', 'Unemployed - Females from batch 1',
    'Number of new Trainees', '2nd Batch - Males', '2nd Batch - Females'
]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# Sidebar filters
st.sidebar.title("Filters")

location = st.sidebar.selectbox("Location", ['All'] + sorted(df['Location'].dropna().unique()))
if location != 'All':
    df = df[df['Location'] == location]

industry_list = df['Industry'].dropna().unique()
industry = st.sidebar.selectbox("Industry", ['All'] + sorted(industry_list))
if industry != 'All':
    df = df[df['Industry'] == industry]

# KPIs
st.title("📊 Trainer & Trainee Dashboard")

total_trainees = int(df['Total Trainees Completed in batch 1'].sum())
males = int(df['Males Completed in batch 1'].sum())
females = int(df['Females Completed in batch 1'].sum())
employed = int(df['Employed - Males from batch 1'].sum() + df['Employed - Females from batch 1'].sum())
unemployed = int(df['Unemployed - Males from batch 1'].sum() + df['Unemployed - Females from batch 1'].sum())

st.markdown(f"""
### KPIs
- **Total Trainees Completed (Batch 1):** {total_trainees}  
- 👨 **Males Completed:** {males}  
- 👩 **Females Completed:** {females}  
- ✅ **Employed:** {employed}  
- ❌ **Unemployed:** {unemployed}
""")

# Charts
bar_fig = px.bar(
    df,
    x='Industry',
    y='Total Trainees Completed in batch 1',
    title='Total Trainees Completed in Batch 1 by Industry',
    text='Total Trainees Completed in batch 1'
)
bar_fig.update_traces(textposition='outside')
st.plotly_chart(bar_fig)

gender_counts = {
    'Males': males,
    'Females': females
}
pie_fig = px.pie(
    names=gender_counts.keys(),
    values=gender_counts.values(),
    title='Gender Distribution of Trainees Completed Batch 1'
)
st.plotly_chart(pie_fig)

st.markdown("✅ **Dashboard generated using Streamlit**")
