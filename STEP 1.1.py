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

st.title('Lending Club Loan Analysis')

risk_counts= df['risk_score'].value_counts().reset_index()
fig = px.pie(risk_counts, names='risk_score', values='count', title='Risk Score Distribution')

st.plotly_chart(fig)

loan_range = st.slider('Select Loan Amount Range:',
                       int(df['loan_amnt'].min()),
                       int(df['loan_amnt'].max()),
                       (10000, 25000))

filtered = df[(df['loan_amnt'] >= loan_range[0]) & (df['loan_amnt'] <= loan_range[1])]
risk_counts = filtered['risk_score'].value_counts().reset_index()
risk_counts.columns = ['risk_score', 'count']
fig = px.pie(risk_counts, names='risk_score', values='count', title='Risk Score Distribution')
st.plotly_chart(fig)
st.write(" Filtered Data", filtered)
