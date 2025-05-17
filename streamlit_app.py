import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Set page configuration with dark theme
st.set_page_config(
    page_title="A/B Test Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Force dark theme
st.markdown('''
    <style>
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
    </style>
''', unsafe_allow_html=True)

# Load data
data = pd.read_csv("ab_data.csv")

# Dashboard title
st.title("🔄 Analyse A/B Test : Ancienne vs Nouvelle Page")

# Overview section
st.header("📊 Vue d'ensemble")

col1, col2, col3 = st.columns(3)

total_visitors = len(data)
visitors_per_group = data['group'].value_counts()
control_visitors = visitors_per_group.get('control', 0)
treatment_visitors = visitors_per_group.get('treatment', 0)

with col1:
    st.metric("Total Visiteurs", f"{total_visitors:,}")
with col2:
    st.metric("Groupe Contrôle", f"{control_visitors:,}")
with col3:
    st.metric("Groupe Test", f"{treatment_visitors:,}")

# Conversion rates
st.header("📈 Taux de conversion")

conversion_by_group = data.groupby('group')['converted'].mean().reset_index()
st.dataframe(conversion_by_group.style.format({'converted': '{:.2%}'}))

# Visualization
chart = alt.Chart(conversion_by_group).mark_bar().encode(
    x=alt.X('group:N', title='Groupe'),
    y=alt.Y('converted:Q', title='Taux de conversion', axis=alt.Axis(format='%')),
    color='group:N'
).properties(
    title='Comparaison des taux de conversion'
)

st.altair_chart(chart, use_container_width=True)

# Statistical test
st.header("🎯 Test statistique")

# Calculate p-value using simulation
np.random.seed(42)
n_simulations = 10000
p_null = data['converted'].mean()
n_treatment = len(data[data['group'] == 'treatment'])
n_control = len(data[data['group'] == 'control'])

# Observed difference
obs_diff = (data[data['group'] == 'treatment']['converted'].mean() - 
            data[data['group'] == 'control']['converted'].mean())

# Simulation
diffs = []
for _ in range(n_simulations):
    control_sim = np.random.binomial(1, p_null, n_control).mean()
    treatment_sim = np.random.binomial(1, p_null, n_treatment).mean()
    diffs.append(treatment_sim - control_sim)

p_value = (np.array(diffs) >= obs_diff).mean()

# Display results
col4, col5 = st.columns(2)
with col4:
    st.metric("Différence observée", f"{obs_diff:.4f}")
with col5:
    st.metric("P-value", f"{p_value:.4f}")

# Conclusion
st.header("📝 Conclusion")
if p_value < 0.05:
    st.success("La différence est statistiquement significative (p < 0.05)")
else:
    st.info("La différence n'est pas statistiquement significative (p >= 0.05)")
