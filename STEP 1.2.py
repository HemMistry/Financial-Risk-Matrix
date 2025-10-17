import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_excel(r"C:\Users\hemmi\OneDrive\Desktop\FINANCIAL RISK MATRIX\lendingclub_sample.xlsx")


def risk_score(row):
    if row['loan_amnt'] > 15000 and row['fico_range_high'] < 600:
        return 'High Risk'
    elif row['fico_range_high'] >= 700:
        return 'Low Risk'
    else:
        return 'Medium Risk'

df['risk_score'] = df.apply(risk_score, axis=1)


st.sidebar.header("🔍 Filters")
loan_range = st.sidebar.slider("Loan Amount", 
                               int(df['loan_amnt'].min()), 
                               int(df['loan_amnt'].max()), 
                               (10000, 25000))
grade = st.sidebar.multiselect("Select Grades", options=df['grade'].unique(), default=df['grade'].unique())


filtered = df[
    (df['loan_amnt'] >= loan_range[0]) & 
    (df['loan_amnt'] <= loan_range[1]) &
    (df['grade'].isin(grade))
]

st.title(" Financial Risk Matrix Dashboard")


st.subheader("1️ Risk Level Distribution")
risk_counts = filtered['risk_score'].value_counts().reset_index()
risk_counts.columns = ['risk_score', 'count']
fig1 = px.pie(risk_counts, names='risk_score', values='count', title='Risk Level Distribution')
st.plotly_chart(fig1, use_container_width=True)


st.subheader("2️ Average Income by Risk Level")
income_by_risk = filtered.groupby('risk_score')['annual_inc'].mean().reset_index()
fig2 = px.bar(income_by_risk, x='risk_score', y='annual_inc', title='Risk by Income')
st.plotly_chart(fig2, use_container_width=True)


st.subheader("3️ Average DTI by Risk")
dti_by_risk = filtered.groupby('risk_score')['dti'].mean().reset_index()
fig3 = px.bar(dti_by_risk, x='risk_score', y='dti', title='Average DTI by Risk')
st.plotly_chart(fig3, use_container_width=True)


st.subheader("4️ Risk by FICO Band")
fico_band = pd.cut(filtered['fico_range_high'], bins=[500, 600, 650, 700, 750, 800, 850])
filtered['fico_band'] = fico_band.astype(str)  
fico_risk = filtered.groupby(['fico_band', 'risk_score']).size().reset_index(name='count')

fig4 = px.bar(
    fico_risk,
    x='fico_band',
    y='count',
    color='risk_score',
    title='Risk Score Distribution by FICO Band',
    barmode='stack'
)



st.subheader(" Filtered Data Table")
st.dataframe(filtered)
