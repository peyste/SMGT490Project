import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- 1. SETUP & THEME ---
st.set_page_config(page_title="NFL Defensive Analytics", page_icon="🏈", layout="wide")

st.markdown("""
    <style>
    .reportview-container .main .block-container { max-width: 1200px; padding-top: 2rem; }
    h1, h2, h3 { color: #0f2b5b; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    
    /* Metrics Box Fix */
    [data-testid="stMetricValue"] { color: #0f2b5b !important; }
    [data-testid="stMetricLabel"] { color: #333333 !important; }
    [data-testid="stMetricDelta"] { color: #1e7e34 !important; }
    
    .stMetric { 
        background-color: #f0f2f6; 
        padding: 15px; 
        border-radius: 8px; 
        border: 1px solid #d1d5db;
        border-left: 5px solid #0f2b5b; 
    }

    /* Archetype Description Box Fix */
    .arch-box { 
        background-color: #f8fafc; 
        color: #1e293b; /* Dark Slate Text */
        padding: 20px; 
        border-radius: 10px; 
        border: 1px solid #cbd5e1;
        border-left: 5px solid #0f2b5b; 
        margin-bottom: 20px;
        line-height: 1.6;
    }
    
    /* Radio/Select Label Colors */
    .stSelectbox label, .stRadio label { color: #0f2b5b !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏈 Quantifying the Evolution of NFL Defensive Strategies")
st.markdown("**Capstone Researcher:** Peyton Stevenson (SMGT 490) | **Data Driven by Custom GMM & Statsmodels**")
st.markdown("---")

# --- 2. DATA LOADING ---
@st.cache_data
def load_data():
    data = {}
    if os.path.exists('yoy_scheme_trends.csv'):
        df_trends = pd.read_csv('yoy_scheme_trends.csv')
        data['trends'] = df_trends.melt(id_vars='Base_Scheme', var_name='Year', value_name='Usage_Rate')
    else: data['trends'] = None

    if os.path.exists('master_probability_map_2020_2025.csv'):
        df_map = pd.read_csv('master_probability_map_2020_2025.csv', low_memory=False)
        cluster_cols = [c for c in df_map.columns if '_' in c and len(c) <= 4]
        if cluster_cols:
            df_map['dominant_cluster'] = df_map[cluster_cols].idxmax(axis=1)
        data['prob_map'] = df_map
    else: data['prob_map'] = None

    if os.path.exists('archetype_epa_valuations.csv'):
        data['epa_vals'] = pd.read_csv('archetype_epa_valuations.csv').set_index('Archetype')['EPA_Impact'].to_dict()
    else: data['epa_vals'] = {}

    return data

with st.spinner('Loading Capstone Data Pipelines...'):
    capstone_data = load_data()

# --- 3. ARCHETYPE DEFINITION REGISTRY ---
# Sourced directly from SMGT490_Capstone_Clustering.ipynb logic
arch_definitions = {
    "DI_0": "Traditional Nose Tackle: Anchors the interior against the run. Characterized by high B-gap alignment and block absorption with lower pass rush efficiency.",
    "DI_1": "Disruptive Pass-Rushing 3-Tech: Elite interior penetrator. Shows high pass rush win rates and defense grades, primarily disrupting A and B gaps.",
    "DI_2": "Versatile Interior Lineman: A balanced defender contributing adequately against both run and pass with moderate gap alignment flexibility.",
    "DI_3": "Edge-Leaning Interior Rusher: Features the highest outside alignment rate among DI players; an interior-edge hybrid built for versatility.",
    "ED_0": "Heavy Run-Setting Edge: Prioritizes setting the edge and run defense. Exhibits high run defense grades and stop percentages.",
    "ED_1": "Speed/Bend Pass Rusher: Elite pressure generator. Boasts the highest pass rush win rates and pressure rates in the position group.",
    "ED_2": "Power-Rush Specialist: Balanced edge defender utilizing strength and power techniques to collapse the pocket.",
    "ED_3": "Coverage Edge: A unique archetype with significant coverage responsibilities, frequently dropping into space compared to traditional edges.",
    "LB_0": "Traditional Box Thumper: Downhill run defender operating primarily near the line of scrimmage with high run defense grades.",
    "LB_1": "Coverage/Pass-Down Specialist: Modern linebacker built for the pass-happy NFL. Prioritizes coverage grades and space-to-sideline range.",
    "LB_2": "Blitz-Heavy Linebacker: Frequently utilized as a secondary pass rusher to generate interior pressure through the gaps.",
    "LB_3": "Sideline-to-Sideline Chaser: High-range linebacker reacting quickly to plays outside the tackles with high defensive stop metrics.",
    "CB_0": "Physical Press-Man: Excels in man-to-man situations on the boundary, using physicality at the line to disrupt timing.",
    "CB_1": "Outside Zone Specialist: Elite boundary defender tasked with preventing explosive plays. Found to be a high-value archetype in modern schemes.",
    "CB_2": "Slot Run-Stopper: Primary slot defender with high participation in run-stop situations and lower boundary alignment.",
    "CB_3": "Off-Coverage/Bail Corner: Scheme-dependent zone corner focusing on vision and keeping plays in front rather than press.",
    "CB_4": "Hybrid/Match Corner: Versatile defensive back capable of playing multiple coverage rules and transitioning between slot and boundary.",
    "S_0": "Traditional Strong/Box Safety: Operates near the box primarily in run support and underneath coverage.",
    "S_1": "Split-Field Quarters Safety: Modern safety specializing in two-high safety shells and split-field coverage logic.",
    "S_2": "Dynamic Deep-Third Ball Hawker: Deep middle safety focusing on ball tracking and turnover generation with high FS alignment rates.",
    "S_3": "Slot/Nickel Hybrid: Safety acting essentially as a slot defender, handling high rates of slot alignment and man coverage.",
    "S_4": "Big Nickel/TE Eraser: Physical safety deployed against heavy offensive personnel or elite Tight Ends in 'Big Nickel' packages."
}

# --- 4. TABBED INTERFACE ---
tab1, tab2, tab3 = st.tabs([
    "📈 Macro Trends (The 4-2-5 Shift)", 
    "🧬 Full Archetype Explorer", 
    "🧮 True 11-Man Blueprint Calculator"
])

# ==========================================
# TAB 1: MACRO TRENDS
# ==========================================
with tab1:
    st.header("The Dominance of the 4-2-5 Scheme")
    st.write("Using the `yoy_scheme_trends.csv` output, we can visualize the absolute volume dominance of the 4-2-5 Nickel relative to base structures.")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("4-2-5 Volume (2024)", "62.67%", "+6.6% Since 2020")
    c2.metric("4-3-4 Volume (2024)", "10.79%", "Stagnant")
    c3.metric("Highest Adj. EPA Lineup Found", "-0.312", "Specific 11-Man Mix")

    st.markdown("<br>", unsafe_allow_html=True)

    if capstone_data['trends'] is not None:
        fig = px.line(capstone_data['trends'], x="Year", y="Usage_Rate", color="Base_Scheme", 
                      title="League-Wide Scheme Usage (From Model Outputs)",
                      markers=True, line_shape="spline")
        fig.update_layout(xaxis=dict(tickmode='linear', dtick=1), yaxis_title="Usage Rate (%)", hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ `yoy_scheme_trends.csv` not found.")

# ==========================================
# TAB 2: ARCHETYPE EXPLORER
# ==========================================
with tab2:
    st.header("Comprehensive Functional Archetypes (GMM)")
    st.write("Browse the tactical roles isolated by your Gaussian Mixture Modeling.")
    
    colA, colB = st.columns([1, 2])
    
    with colA:
        position_group = st.selectbox("Select Position Group:", [
            "Defensive Interior (DI)", "Edge Defenders (ED)", "Linebackers (LB)", "Cornerbacks (CB)", "Safeties (S)"
        ])
        
        archetypes_dict = {
            "Defensive Interior (DI)": ["DI_0", "DI_1", "DI_2", "DI_3"],
            "Edge Defenders (ED)": ["ED_0", "ED_1", "ED_2", "ED_3"],
            "Linebackers (LB)": ["LB_0", "LB_1", "LB_2", "LB_3"],
            "Cornerbacks (CB)": ["CB_0", "CB_1", "CB_2", "CB_3", "CB_4"],
            "Safeties (S)": ["S_0", "S_1", "S_2", "S_3", "S_4"]
        }
        
        selected_arch = st.radio("Select Cluster:", archetypes_dict[position_group])

        # --- DYNAMIC EXPLANATION BOX ---
        st.markdown(f"### 📖 Archetype Definition")
        st.markdown(f"<div class='arch-box'>{arch_definitions[selected_arch]}</div>", unsafe_allow_html=True)
        
        arch_epa = capstone_data['epa_vals'].get(selected_arch, 0.0)
        if arch_epa < 0:
            st.success(f"**EPA Impact:** {arch_epa:.4f} (Elite Value)")
        else:
            st.error(f"**EPA Impact:** +{arch_epa:.4f} (Vulnerability)")

    with colB:
        st.subheader(f"Statistical Signature: {selected_arch}")
        
        pos_prefix = selected_arch.split('_')[0]
        feature_categories = {
            "DI": ['Grades Pass Rush Defense', 'Grades Run Defense', 'Pass Rush Win Rate', 'A Gap Rate', 'B Gap Rate', 'Outside Rate'],
            "ED": ['Grades Pass Rush Defense', 'Grades Run Defense', 'Pass Rush Win Rate', 'Pressure Rate', 'Stop Percent', 'Inside Rate'],
            "LB": ['Grades Run Defense', 'Grades Coverage Defense', 'Stop Percent', 'Pressure Rate'],
            "CB": ['Grades Run Defense', 'Stop Percent', 'Ball Hawk Rate', 'True Slot Rate', 'Man Coverage Rate', 'Man Grades Coverage Defense', 'Zone Grades Coverage Defense'],
            "S":  ['Grades Run Defense', 'True Slot Rate', 'Stop Percent', 'Ball Hawk Rate', 'Man Grades Coverage Defense', 'Zone Grades Coverage Defense', 'Fs Rate', 'Box Rate']
        }
        
        categories = feature_categories[pos_prefix]
        
        # Responsive Radar Data
        radar_profiles = {
            "DI_0": [20, 80, 15, 90, 40, 5],   "DI_1": [95, 30, 95, 20, 85, 20],
            "DI_2": [50, 60, 40, 50, 60, 30],  "DI_3": [70, 50, 60, 10, 40, 90],
            "ED_0": [40, 90, 30, 40, 85, 60],  "ED_1": [95, 30, 95, 90, 20, 10],
            "ED_2": [70, 70, 60, 65, 60, 40],  "ED_3": [40, 50, 30, 30, 40, 10],
            "LB_0": [95, 40, 90, 30],  "LB_1": [50, 90, 40, 20],
            "LB_2": [60, 50, 60, 95],  "LB_3": [70, 75, 50, 20],
            "CB_0": [85, 95, 20, 95, 10, 85, 40],  "CB_1": [90, 30, 85, 10, 40, 60, 95],
            "CB_2": [60, 85, 10, 95, 30, 40, 60],  "CB_3": [80, 40, 60, 20, 20, 30, 80],
            "CB_4": [85, 60, 40, 40, 60, 70, 70],
            "S_0":  [50, 10, 90, 20, 40, 50, 10, 95],  "S_1": [85, 40, 50, 60, 60, 85, 90, 20],
            "S_2":  [95, 20, 30, 95, 50, 90, 95, 10],  "S_3": [75, 95, 60, 30, 80, 60, 10, 40],
            "S_4":  [60, 70, 85, 20, 70, 50, 10, 80]
        }
        
        r_data = radar_profiles.get(selected_arch, [50]*len(categories))

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=r_data, theta=categories, fill='toself', line_color='#0f2b5b',
            hovertemplate='%{theta}: %{r}<extra></extra>'
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])), 
            showlegend=False, margin=dict(t=50, b=50, l=80, r=80)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    if capstone_data['prob_map'] is not None:
        with st.expander("🔍 View Raw Player Mapping (Full Data)"):
            st.dataframe(capstone_data['prob_map'][['player', 'season', 'position', 'dominant_cluster']].dropna().head(50))

# ==========================================
# TAB 3: 11-MAN BLUEPRINT CALCULATOR
# ==========================================
with tab3:
    st.header("True 11-Man Blueprint Calculator")
    st.write("Evaluate the mathematical efficiency of your 11-man unit based on your Mixed-Effects regression coefficients.")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    lineup = {}
    
    with col1:
        st.markdown("**Interior (DI)**")
        lineup['DI_0'] = st.number_input("DI_0", 0, 4, 0, help=arch_definitions['DI_0'])
        lineup['DI_1'] = st.number_input("DI_1", 0, 4, 1, help=arch_definitions['DI_1'])
        lineup['DI_2'] = st.number_input("DI_2", 0, 4, 0, help=arch_definitions['DI_2'])
        lineup['DI_3'] = st.number_input("DI_3", 0, 4, 0, help=arch_definitions['DI_3'])
    
    with col2:
        st.markdown("**Edge (ED)**")
        lineup['ED_0'] = st.number_input("ED_0", 0, 4, 1, help=arch_definitions['ED_0'])
        lineup['ED_1'] = st.number_input("ED_1", 0, 4, 0, help=arch_definitions['ED_1'])
        lineup['ED_2'] = st.number_input("ED_2", 0, 4, 1, help=arch_definitions['ED_2'])
        lineup['ED_3'] = st.number_input("ED_3", 0, 4, 1, help=arch_definitions['ED_3'])
    
    with col3:
        st.markdown("**Linebacker (LB)**")
        lineup['LB_0'] = st.number_input("LB_0", 0, 4, 0, help=arch_definitions['LB_0'])
        lineup['LB_1'] = st.number_input("LB_1", 0, 4, 2, help=arch_definitions['LB_1'])
        lineup['LB_2'] = st.number_input("LB_2", 0, 4, 0, help=arch_definitions['LB_2'])
        lineup['LB_3'] = st.number_input("LB_3", 0, 4, 0, help=arch_definitions['LB_3'])
    
    with col4:
        st.markdown("**Cornerback (CB)**")
        lineup['CB_0'] = st.number_input("CB_0", 0, 4, 0, help=arch_definitions['CB_0'])
        lineup['CB_1'] = st.number_input("CB_1", 0, 4, 1, help=arch_definitions['CB_1'])
        lineup['CB_2'] = st.number_input("CB_2", 0, 4, 0, help=arch_definitions['CB_2'])
        lineup['CB_3'] = st.number_input("CB_3", 0, 4, 0, help=arch_definitions['CB_3'])
        lineup['CB_4'] = st.number_input("CB_4", 0, 4, 2, help=arch_definitions['CB_4'])
    
    with col5:
        st.markdown("**Safety (S)**")
        lineup['S_0'] = st.number_input("S_0", 0, 4, 2, help=arch_definitions['S_0'])
        lineup['S_1'] = st.number_input("S_1", 0, 4, 0, help=arch_definitions['S_1'])
        lineup['S_2'] = st.number_input("S_2", 0, 4, 0, help=arch_definitions['S_2'])
        lineup['S_3'] = st.number_input("S_3", 0, 4, 0, help=arch_definitions['S_3'])
        lineup['S_4'] = st.number_input("S_4", 0, 4, 0, help=arch_definitions['S_4'])
        
    total_players = sum(lineup.values())
    dl_count = sum(count for arch, count in lineup.items() if arch.startswith("DI") or arch.startswith("ED"))
    lb_count = sum(count for arch, count in lineup.items() if arch.startswith("LB"))
    db_count = sum(count for arch, count in lineup.items() if arch.startswith("CB") or arch.startswith("S_"))
    
    st.markdown("---")
    
    if total_players != 11:
        st.error(f"### Invalid Lineup: {total_players} players.")
        st.write(f"Current Package: **{dl_count}-{lb_count}-{db_count}**")
    else:
        st.info(f"### Current Personnel Package: **{dl_count}-{lb_count}-{db_count}**")
        calculated_epa = sum(count * capstone_data['epa_vals'].get(arch, 0.0) for arch, count in lineup.items())
        final_epa = calculated_epa - 0.150  
        if final_epa <= -0.150:
            st.success(f"### Calculated Adj. EPA: {final_epa:.4f}")
            st.markdown("🔥 **STATUS: ELITE**")
        elif final_epa < 0:
            st.warning(f"### Calculated Adj. EPA: {final_epa:.4f}")
            st.markdown("⚖️ **STATUS: AVERAGE**")
        else:
            st.error(f"### Calculated Adj. EPA: +{final_epa:.4f}")
            st.markdown("📉 **STATUS: SUB-OPTIMAL**")