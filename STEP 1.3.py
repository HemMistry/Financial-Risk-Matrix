import streamlit as st
import pandas as pd
import plotly.express as px

# Load your dataset
df = pd.read_excel(r"C:\Users\hemmi\OneDrive\Desktop\FINANCIAL RISK MATRIX\lendingclub_sample.xlsx")

# Clean up any missing values that affect scoring
df = df.dropna(subset=['dti', 'annual_inc', 'fico_range_high'])

# ✨ New: Balanced Risk Scoring using quantiles
dti_q = df['dti'].quantile([0.33, 0.66])
income_q = df['annual_inc'].quantile([0.33, 0.66])
fico_q = df['fico_range_high'].quantile([0.33, 0.66])

from sklearn.preprocessing import MinMaxScaler
import numpy as np

# Normalize important features
scaler = MinMaxScaler()
df[['dti_norm', 'income_norm', 'fico_norm']] = scaler.fit_transform(
    df[['dti', 'annual_inc', 'fico_range_high']]
)

# Calculate composite score (lower is worse)
# Invert DTI (since low DTI is good)
df['composite_score'] = (1 - df['dti_norm']) * 0.4 + df['income_norm'] * 0.3 + df['fico_norm'] * 0.3

# Now use quantiles to assign risk levels
df['risk_level'] = pd.qcut(df['composite_score'], q=[0, 0.3, 0.7, 1.0], labels=['High Risk', 'Medium Risk', 'Low Risk'])


# ───────────────────────────────────────────────
# 🧠 SIDEBAR FILTERS
st.sidebar.header("🔍 Filters")
loan_range = st.sidebar.slider("Loan Amount", 5000, 40000, (10000, 25000))
grades = df['grade'].unique()
selected_grades = st.sidebar.multiselect("Grade", options=grades, default=grades)

# Apply filters
filtered = df[
    (df['loan_amnt'] >= loan_range[0]) &
    (df['loan_amnt'] <= loan_range[1]) &
    (df['grade'].isin(selected_grades))
]

# ───────────────────────────────────────────────
# 📊 METRICS
st.title("📊 Financial Risk Matrix Dashboard")

col1, col2 = st.columns(2)
col1.metric("Total Records", len(filtered))
col2.metric("High Risk %", f"{(filtered['risk_level'].value_counts().get('High Risk', 0)/len(filtered)*100):.1f}%" if len(filtered) else "0%")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Risk Distribution",
    "💰 Income vs Risk",
    "📈 DTI vs Risk",
    "🧾 FICO Band vs Risk",
    "📄 Data Table"
])

with tab1:
    st.subheader("📊 Risk Level Distribution")
    risk_counts = filtered['risk_level'].value_counts().reset_index()
    risk_counts.columns = ['risk_level', 'count']
    fig1 = px.pie(risk_counts, names='risk_level', values='count', title='Risk Distribution')
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    st.subheader("💰 Average Income by Risk Level")
    income_by_risk = filtered.groupby('risk_level')['annual_inc'].mean().reset_index()
    fig2 = px.bar(income_by_risk, x='risk_level', y='annual_inc', title='Income by Risk Level', color='risk_level')
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("📈 Average DTI by Risk Level")
    dti_by_risk = filtered.groupby('risk_level')['dti'].mean().reset_index()
    fig3 = px.bar(dti_by_risk, x='risk_level', y='dti', title='DTI by Risk Level', color='risk_level')
    st.plotly_chart(fig3, use_container_width=True)

with tab4:
    st.subheader("🧾 Risk Level by FICO Band")
    fico_band = pd.cut(filtered['fico_range_high'], bins=[500, 600, 650, 700, 750, 800, 850])
    filtered['fico_band'] = fico_band.astype(str)
    fico_risk = filtered.groupby(['fico_band', 'risk_level']).size().reset_index(name='count')

    # Sort for cleaner chart
    fico_risk['risk_level'] = pd.Categorical(fico_risk['risk_level'], categories=['High Risk', 'Medium Risk', 'Low Risk'])
    fico_risk = fico_risk.sort_values(['fico_band', 'risk_level'])

    fig4 = px.bar(fico_risk, x='fico_band', y='count', color='risk_level', title='FICO Band vs Risk', barmode='stack')
    st.plotly_chart(fig4, use_container_width=True)

with tab5:
    st.subheader("📄 Filtered Data Table")
    st.dataframe(filtered)

    # Download
    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", data=csv, file_name='filtered_loans.csv', mime='text/csv')
