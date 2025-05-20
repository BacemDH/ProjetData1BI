#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
st.set_page_config(layout="centered")
# --- Chargement des données ---
data = pd.read_csv("ab_data.csv")
# --- Titre du dashboard ---
st.title("Analyse A/B Test : Ancienne vs Nouvelle Page")
# --- KPI Section 1 : Vue Générale ---
st.header("1. Vue d'ensemble des données")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Nombre total de visiteurs", len(data))

with col2:
    visitors_per_group = data['group'].value_counts()
    st.metric("Contrôle", visitors_per_group.get('control', 0))

with col3:
    st.metric("Traitement", visitors_per_group.get('treatment', 0))

# Taux de conversion global
conversion_rate = data['converted'].mean()
st.write(f"\n✅ **Taux de conversion global** : {conversion_rate:.2%}")

# --- KPI par groupe ---
st.subheader("Taux de conversion par groupe")
conversion_by_group = data.groupby('group')['converted'].mean().reset_index()
st.dataframe(conversion_by_group)

# --- Bar chart conversions ---
st.subheader("Visualisation : Taux de conversion par groupe")
bar_chart = alt.Chart(conversion_by_group).mark_bar().encode(
    x=alt.X('group:N', title='Groupe'),
    y=alt.Y('converted:Q', title='Taux de conversion'),
    color='group'
)
st.altair_chart(bar_chart, use_container_width=True)

# --- Partie 2 : Simulation sous l'hypothèse nulle ---
st.header("2. Test d'hypothèse par simulation")

# Paramètres de base
p_null = data['converted'].mean()
n_new = data.query("group == 'treatment'").shape[0]
n_old = data.query("group == 'control'").shape[0]

# Simulation de 10 000 expériences
np.random.seed(42)
diffs = []
for _ in range(10000):
    new_sample = np.random.binomial(1, p_null, n_new)
    old_sample = np.random.binomial(1, p_null, n_old)
    diffs.append(new_sample.mean() - old_sample.mean())

diffs = np.array(diffs)

# Différence observée
obs_diff = data.query("group == 'treatment'")['converted'].mean() - \
           data.query("group == 'control'")['converted'].mean()

# p-value
p_value = (diffs > obs_diff).mean()

# KPI Résultats
col4, col5, col6 = st.columns(3)
with col4:
    st.metric("Conversion Traitement", f"{data.query('group == \"treatment\"')['converted'].mean():.2%}")
with col5:
    st.metric("Conversion Contrôle", f"{data.query('group == \"control\"')['converted'].mean():.2%}")
with col6:
    st.metric("p-value", f"{p_value:.4f}")

# --- Histogramme des différences simulées ---
st.subheader("Distribution simulée des différences")
diffs_df = pd.DataFrame({'diffs': diffs})
chart = alt.Chart(diffs_df).mark_bar().encode(
    alt.X("diffs", bin=alt.Bin(maxbins=100), title="Différences simulées"),
    y='count()'
).properties(title="Distribution sous H₀")

line = alt.Chart(pd.DataFrame({'obs_diff': [obs_diff]})).mark_rule(color='red').encode(
    x='obs_diff'
)

st.altair_chart(chart + line, use_container_width=True)

# --- Interprétation ---
st.markdown("""
### 🎯 Conclusion
- La différence observée entre les taux de conversion est : **{0:.4f}**.
- La p-value est de **{1:.4f}**.
- Cela signifie que {2}
""".format(
    obs_diff,
    p_value,
    "cette différence est significative, la nouvelle page est probablement meilleure." if p_value < 0.05 else "la différence peut s'expliquer par le hasard. Nous ne rejetons pas l'hypothèse nulle."
))

