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
        .stMetric {
            background-color: #262730 !important;
            border: 1px solid #21222c;
        }
        .stMetric:hover {
            background-color: #2c2c3a !important;
        }
        div[data-testid="stMetricValue"] {
            color: #fafafa !important;
        }
        div[data-testid="stMetricDelta"] {
            color: #4a90e2 !important;
        }
        .element-container {
            color: #fafafa;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #4a90e2 !important;
        }
        .stDataFrame {
            background-color: #262730;
        }
        .stMarkdown {
            color: #fafafa;
        }
    </style>
''', unsafe_allow_html=True)

# Additional styling for dark theme
st.markdown("""
<style>
    .main {
        padding: 2rem;
        background-color: #0e1117;
    }
    .stMetric {
        background: linear-gradient(135deg, #262730 0%, #1e1e24 100%);
        padding: 1.2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        border: 1px solid #21222c;
        color: #fafafa;
    }
    .stMetric:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        background: linear-gradient(135deg, #2c2c3a 0%, #262730 100%);
    }
    h1 {
        color: #4a90e2 !important;
        padding-bottom: 1rem;
        border-bottom: 3px solid #4a90e2;
        text-align: center;
        font-weight: 800;
    }
    h2 {
        color: #fafafa !important;
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        font-weight: 600;
        border-left: 4px solid #4a90e2;
        padding-left: 1rem;
    }
    .stDataFrame {
        background-color: #262730;
        border: 1px solid #21222c;
        border-radius: 10px;
        padding: 1rem;
        color: #fafafa;
    }
    .stPlotlyChart {
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        padding: 1rem;
        background: #262730;
    }
    div[data-testid="stDecoration"] {
        background-image: linear-gradient(90deg, #4a90e2, #1f77b4);
    }
    /* Style for charts */
    .vega-embed {
        background-color: #262730;
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #21222c;
    }
    /* Style for text */
    p, span, div {
        color: #fafafa !important;
    }
</style>
""", unsafe_allow_html=True)
# --- Chargement des données ---
data = pd.read_csv("ab_data.csv")
# --- Titre du dashboard avec style moderne ---
st.markdown("<h1 style='text-align: center;'>🔄 Analyse A/B Test : Ancienne vs Nouvelle Page</h1>", unsafe_allow_html=True)

# --- KPI Section 1 avec design amélioré ---
st.markdown("<h2>📊 Vue d'ensemble des données</h2>", unsafe_allow_html=True)

# Ajout d'un conteneur avec ombre
with st.container():
    col1, col2, col3 = st.columns(3)
    
    total_visitors = len(data)
    visitors_per_group = data['group'].value_counts()
    control_visitors = visitors_per_group.get('control', 0)
    treatment_visitors = visitors_per_group.get('treatment', 0)
    
    with col1:
        st.metric(
            "📥 Nombre total de visiteurs",
            f"{total_visitors:,}",
            delta=None,
            help="Nombre total de visiteurs dans l'expérience A/B"
        )
    
    with col2:
        st.metric(
            "🔵 Groupe Contrôle",
            f"{control_visitors:,}",
            delta=f"{(control_visitors/total_visitors)*100:.1f}%",
            help="Nombre de visiteurs dans le groupe contrôle"
        )
    
    with col3:
        st.metric(
            "🟣 Groupe Traitement",
            f"{treatment_visitors:,}",
            delta=f"{(treatment_visitors/total_visitors)*100:.1f}%",
            help="Nombre de visiteurs dans le groupe traitement"
        )

# --- Section Taux de conversion avec design moderne ---
st.markdown("<hr style='margin: 2rem 0;'>", unsafe_allow_html=True)
st.markdown("<h2>📈 Analyse des Taux de Conversion</h2>", unsafe_allow_html=True)

# Conteneur pour les taux de conversion
with st.container():
    # Calcul des taux de conversion
    conversion_rate = data['converted'].mean()
    conversion_by_group = data.groupby('group')['converted'].mean().reset_index()
    
    # Affichage des taux de conversion avec style
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Tableau stylisé
        st.dataframe(
            conversion_by_group.style.format({
                'converted': '{:.2%}'
            }).set_properties(**{
                'background-color': '#262730',
                'color': '#fafafa'
            }),
            hide_index=True
        )
        
        st.markdown(f"""<p style='text-align: center; margin-top: 1rem;'>
            📄 Taux de conversion global: <strong>{conversion_rate:.2%}</strong>
        </p>""", unsafe_allow_html=True)
    
    with col2:
        # Graphique amélioré
        base = alt.Chart(conversion_by_group).encode(
            x=alt.X('group:N', 
                    title='Groupe',
                    axis=alt.Axis(labelAngle=0, labelFontSize=12)),
            y=alt.Y('converted:Q',
                    title='Taux de conversion',
                    axis=alt.Axis(format='%'),
                    scale=alt.Scale(domain=[0, max(conversion_by_group['converted']) * 1.2])),
            color=alt.Color('group:N',
                          scale=alt.Scale(range=['#4a90e2', '#00ff87']),
                          legend=None)
        )

        bar_chart = base.mark_bar(cornerRadius=8).encode(
            tooltip=[
                alt.Tooltip('group:N', title='Groupe'),
                alt.Tooltip('converted:Q', title='Taux de conversion', format='.2%')
            ]
        ).properties(
            title=alt.TitleParams(
                ['Comparaison des Taux de Conversion', 'Analyse par groupe'],
                fontSize=16
            ),
            width=400,
            height=300
        ).configure_view(
            strokeWidth=0
        )

st.altair_chart(bar_chart, use_container_width=True)

# --- Section Test d'Hypothèse avec Design Moderne ---
st.markdown("<hr style='margin: 2rem 0;'>", unsafe_allow_html=True)
st.markdown("<h2>🔮 Test d'Hypothèse par Simulation</h2>", unsafe_allow_html=True)

# Paramètres et simulation
with st.container():
    # Calculs de base
    p_null = data['converted'].mean()
    n_new = data.query("group == 'treatment'").shape[0]
    n_old = data.query("group == 'control'").shape[0]
    
    # Simulation
    np.random.seed(42)
    diffs = []
    n_simulations = 10000
    
    # Calcul de la différence observée
    obs_diff = (data.query('group == "treatment"')['converted'].mean() - 
                data.query('group == "control"')['converted'].mean())
    
    # Simulation sous l'hypothèse nulle
    for _ in range(n_simulations):
        control_sim = np.random.binomial(1, p_null, n_old).mean()
        treatment_sim = np.random.binomial(1, p_null, n_new).mean()
        diffs.append(treatment_sim - control_sim)
    
    # Calcul de la p-value
    p_value = (np.array(diffs) >= obs_diff).mean()
    
    # Affichage des résultats avec style
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.metric(
            "🟣 Conversion Traitement",
            f"{data.query('group == "treatment"')['converted'].mean():.2%}",
            help="Taux de conversion du groupe traitement"
        )
    
    with col5:
        st.metric(
            "🔵 Conversion Contrôle",
            f"{data.query('group == "control"')['converted'].mean():.2%}",
            help="Taux de conversion du groupe contrôle"
        )
    with col6:
        st.metric(
            "📊 P-value",
            f"{p_value:.4f}",
            delta="Significatif" if p_value < 0.05 else "Non significatif",
            delta_color="normal",
            help="Une p-value < 0.05 indique une différence significative"
        )

# Visualisation améliorée
st.markdown("<h3 style='color: #2c3e50; margin-top: 2rem;'>📈 Distribution des Différences</h3>", unsafe_allow_html=True)

# Création du graphique amélioré
diffs_df = pd.DataFrame({'diffs': diffs})

# Histogramme avec ligne verticale
hist_data = alt.Chart(diffs_df, background='#262730').transform_density(
    'diffs',
    as_=['diffs', 'density'],
).mark_area(opacity=0.8, color='#4a90e2').encode(
    x=alt.X('diffs:Q', title='Différence de taux de conversion',
            axis=alt.Axis(labelColor='#fafafa', titleColor='#fafafa')),
    y=alt.Y('density:Q', title='Densité',
            axis=alt.Axis(labelColor='#fafafa', titleColor='#fafafa')),
) + alt.Chart(pd.DataFrame({'x': [obs_diff]})).mark_rule(color='#00ff87', size=2).encode(
    x='x:Q',
    tooltip=['x']
).properties(
    title={
        'text': 'Distribution des différences simulées',
        'color': '#fafafa'
    },
    width=700,
    height=300
).configure_axis(
    grid=True,
    gridColor='#333333',
    domainColor='#fafafa',
    tickColor='#fafafa'
).configure_view(
    strokeWidth=0
)

st.altair_chart(hist_data, use_container_width=True)

# Box Plot pour la distribution des conversions
box_plot = alt.Chart(data, background='#262730').mark_boxplot(color='#4a90e2').encode(
    x=alt.X('group:N', title='Groupe',
            axis=alt.Axis(labelColor='#fafafa', titleColor='#fafafa')),
    y=alt.Y('converted:Q', title='Taux de conversion',
            axis=alt.Axis(format='%', labelColor='#fafafa', titleColor='#fafafa')),
    color=alt.Color('group:N',
                    scale=alt.Scale(range=['#00ff87', '#4a90e2']),
                    legend=None)
).properties(
    title={
        'text': 'Distribution des conversions par groupe (Box Plot)',
        'color': '#fafafa'
    },
    width=700,
    height=300
).configure_axis(
    grid=True,
    gridColor='#333333',
    domainColor='#fafafa',
    tickColor='#fafafa'
).configure_view(
    strokeWidth=0
)

st.altair_chart(box_plot, use_container_width=True)

# Ajout d'une séparation visuelle avant la conclusion
st.markdown("<hr style='height: 3px; background: linear-gradient(to right, #4a90e2, #1f77b4); border: none; margin: 2rem 0;'>", unsafe_allow_html=True)

# Conclusion stylée avec un design amélioré
st.markdown("""
<div style='background: linear-gradient(135deg, #262730 0%, #1e222e 100%); 
            padding: 2rem; 
            border-radius: 15px; 
            border-left: 5px solid #4a90e2; 
            margin: 2rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
    <h3 style='color: #4a90e2; 
               margin-bottom: 1.5rem; 
               padding-bottom: 0.5rem; 
               border-bottom: 2px solid #333;'>
        🎯 Conclusion de l'Analyse
    </h3>
    <div style='background: #1e222e; 
                padding: 1.5rem; 
                border-radius: 10px; 
                border: 1px solid #333;'>
        <ul style='list-style-type: none; 
                   padding-left: 0; 
                   margin: 0;'>
            <li style='margin-bottom: 1rem; 
                       padding: 0.5rem; 
                       border-radius: 8px; 
                       background-color: #262730;'>
                📈 <strong style='color: #00ff87;'>Différence observée:</strong> 
                <span style='float: right; color: #fafafa;'>{0:.4f}</span>
            </li>
            <li style='margin-bottom: 1rem; 
                       padding: 0.5rem; 
                       border-radius: 8px; 
                       background-color: #262730;'>
                📊 <strong style='color: #00ff87;'>P-value:</strong> 
                <span style='float: right; color: #fafafa;'>{1:.4f}</span>
            </li>
            <li style='padding: 1rem; 
                       border-radius: 8px; 
                       background-color: #262730; 
                       border-left: 3px solid #00ff87;'>
                📝 <strong style='color: #00ff87;'>Interprétation:</strong><br>
                <p style='margin-top: 0.5rem; margin-bottom: 0; color: #fafafa;'>{2}</p>
            </li>
        </ul>
    </div>
</div>

<!-- Ajout d'une note finale -->
<div style='text-align: center; 
            margin-top: 2rem; 
            padding: 1rem; 
            color: #666; 
            font-style: italic;'>
    💡 <em>Cette analyse a été réalisée avec rigueur statistique pour garantir la validité des résultats.</em>
</div>
""".format(
    obs_diff,
    p_value,
    "Cette différence est statistiquement significative. La nouvelle page montre une amélioration notable des performances." 
    if p_value < 0.05 else 
    "La différence observée n'est pas statistiquement significative. Les performances des deux versions sont similaires."
), unsafe_allow_html=True)

# Visualisation
st.subheader('Visualisation des taux de conversion')
chart = alt.Chart(conversion_by_group).mark_bar().encode(
    x=alt.X('group:N', title='Groupe'),
    y=alt.Y('converted:Q', title='Taux de conversion', axis=alt.Axis(format='%')),
    color='group:N'
).properties(
    title='Comparaison des taux de conversion'
)

st.altair_chart(chart, use_container_width=True)

# Test statistique
st.header('🎯 Test statistique')

# Calcul de la p-value
np.random.seed(42)
n_simulations = 10000
p_null = data['converted'].mean()
n_treatment = len(data[data['group'] == 'treatment'])
n_control = len(data[data['group'] == 'control'])

# Différence observée
obs_diff = (data[data['group'] == 'treatment']['converted'].mean() - 
            data[data['group'] == 'control']['converted'].mean())

# Simulation
diffs = []
for _ in range(n_simulations):
    control_sim = np.random.binomial(1, p_null, n_control).mean()
    treatment_sim = np.random.binomial(1, p_null, n_treatment).mean()
    diffs.append(treatment_sim - control_sim)

p_value = (np.array(diffs) >= obs_diff).mean()

# Affichage des résultats
col4, col5 = st.columns(2)
with col4:
    st.metric('Différence observée', f'{obs_diff:.4f}')
with col5:
    st.metric('P-value', f'{p_value:.4f}')

# Conclusion
st.header('📝 Conclusion')
if p_value < 0.05:
    st.success('La différence est statistiquement significative (p < 0.05)')
else:
    st.info('La différence n\'est pas statistiquement significative (p >= 0.05)')
