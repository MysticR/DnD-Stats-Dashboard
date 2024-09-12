#######################
# Import libraries
import streamlit as st
import altair as alt
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

#######################
# Page configuration
st.set_page_config(
    page_title="DnD Stats",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded",
)

alt.themes.enable("dark")

#######################
# CSS styling
st.markdown(
    """
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
    display: flex;
    justify-content: center;
    align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""",
    unsafe_allow_html=True,
)


#######################
# Load data
stats = pd.read_csv("data/stats.txt")

#######################
# Sidebar
# with st.sidebar:
#     st.title("🎲 DnD Dashboard")

#     char_list = ["Gehrman", "Meluk", "Far"]
#     char_s = st.selectbox("Select a character", char_list)
#     if char_s == "Gehrman":
#         selected_char = "G"
#     elif char_s == "Far":
#         selected_char = "F"
#     else:
#         selected_char = "M"

#     color_theme_list = [
#         "blues",
#         "cividis",
#         "greens",
#         "inferno",
#         "magma",
#         "plasma",
#         "reds",
#         "rainbow",
#         "turbo",
#         "viridis",
#     ]
#     selected_color_theme = st.selectbox("Select a color theme", color_theme_list)

# if input_color == "blue":
#    chart_color = ["#29b5e8", "#155F7A"]
# if input_color == "green":
#    chart_color = ["#27AE60", "#12783D"]
# if input_color == "orange":
#    chart_color = ["#F39C12", "#875A12"]
# if input_color == "red":
#    chart_color = ["#E74C3C", "#781F16"]

st.title("🎲 DnD Stats Dashboard")


#######################
# Plots
def d20(selected_char):
    stats = pd.read_csv("data/stats.txt")
    mdf_selected_char = stats[stats.char == selected_char]
    md20 = mdf_selected_char[mdf_selected_char[" d"] == 20]
    md20hit = md20[md20[" dmg"] == 0]
    return md20hit


# Data for different characters
md20 = d20("M")
gd20 = d20("G")
fd20 = d20("F")

# Create box plot figure
ovhit = go.Figure()
ovhit.update_layout(
    title={"text": "Hit Rolls"},
    xaxis=dict(title="Characters"),
    yaxis=dict(title="Rolls"),
)
ovhit.update_yaxes(range=[0, 20])

# Add box plots
ovhit = ovhit.add_trace(go.Box(y=md20[" r"], name="Meluk"))
ovhit = ovhit.add_trace(go.Box(y=gd20[" r"], name="Gehrman"))
ovhit = ovhit.add_trace(go.Box(y=fd20[" r"], name="Far"))
ovhit.update_layout(showlegend=False)


# ---------------------#
def dmg(selected_char):
    stats = pd.read_csv("data/stats.txt")
    mdf_selected_char = stats[stats.char == selected_char]
    dmg = mdf_selected_char[mdf_selected_char[" dmg"] == 1]
    xdmg = dmg[" r"].sum()
    return xdmg


mdmg = dmg("M")
gdmg = dmg("G")
fdmg = dmg("F")

ovdmg = go.Figure()
ovdmg.update_layout(
    title={"text": "Total Damage"},
    xaxis=dict(title="Characters"),
    yaxis=dict(title="Damage"),
)

# Add box plots
ovdmg = ovdmg.add_trace(go.Bar(x=["Meluk"], y=[mdmg], name="Meluk"))
ovdmg = ovdmg.add_trace(go.Bar(x=["Gehrman"], y=[gdmg], name="Gehrman"))
ovdmg = ovdmg.add_trace(go.Bar(x=["Far"], y=[fdmg], name="Far"))
ovdmg.update_layout(showlegend=False)

#######################
# Dashboard Main Panel
col = st.columns((1, 1), gap="medium")

with col[0]:
    st.plotly_chart(ovhit, use_container_width=True)

with col[1]:
    st.plotly_chart(ovdmg, use_container_width=True)

char_list = ["Gehrman", "Meluk", "Far"]
char_s = st.selectbox("Select a character", char_list)
if char_s == "Gehrman":
    selected_char = "G"
elif char_s == "Far":
    selected_char = "F"
else:
    selected_char = "M"

# ---------------------#

stats = pd.read_csv("data/stats.txt")
mdf_sel_char = stats[stats.char == selected_char]


def dsplit(d, mdf_selected_char):
    dx = mdf_selected_char[mdf_selected_char[" d"] == d]
    return dx


d4 = dsplit(4, mdf_sel_char)
d6 = dsplit(6, mdf_sel_char)
d8 = dsplit(8, mdf_sel_char)
d10 = dsplit(10, mdf_sel_char)
d12 = dsplit(12, mdf_sel_char)
d20 = dsplit(20, mdf_sel_char)

ovchar = go.Figure()
ovchar.update_layout(
    title={"text": char_s},
    xaxis=dict(title="Dice"),
    yaxis=dict(title="Rolls"),
)
ovchar.update_yaxes(range=[0, 20])
# Add box plots
ovchar = ovchar.add_trace(go.Box(y=d4[" r"], name="d4"))
ovchar = ovchar.add_trace(go.Box(y=d6[" r"], name="d6"))
ovchar = ovchar.add_trace(go.Box(y=d8[" r"], name="d8"))
ovchar = ovchar.add_trace(go.Box(y=d10[" r"], name="d10"))
ovchar = ovchar.add_trace(go.Box(y=d12[" r"], name="d12"))
ovchar = ovchar.add_trace(go.Box(y=d20[" r"], name="d20"))
ovchar.update_layout(showlegend=False)

st.plotly_chart(ovchar, use_container_width=True)

# -----------------------#

mdf_sel_char = stats[stats.char == "M"]

d4 = dsplit(4, "Meluk")
d6 = dsplit(6, "Meluk")
d8 = dsplit(8, "Meluk")
d10 = dsplit(10, "Meluk")
d12 = dsplit(12, "Meluk")
d20 = dsplit(20, "Meluk")

mov = go.Figure()
mov.update_layout(
    title={"text": "Meluk"},
    xaxis=dict(title="Dice"),
    yaxis=dict(title="Rolls"),
)
mov.update_yaxes(range=[0, 20])
# Add box plots
mov = mov.add_trace(go.Box(y=d4[" r"], name="d4"))
mov = mov.add_trace(go.Box(y=d6[" r"], name="d6"))
mov = mov.add_trace(go.Box(y=d8[" r"], name="d8"))
mov = mov.add_trace(go.Box(y=d10[" r"], name="d10"))
mov = mov.add_trace(go.Box(y=d12[" r"], name="d12"))
mov = mov.add_trace(go.Box(y=d20[" r"], name="d20"))
mov.update_layout(showlegend=False)

st.plotly_chart(mov,use_container_width=True)

st.dataframe(
    data=pd.DataFrame(stats),
    use_container_width=True,
    column_config={
        "char": "Character",
        " d": "Dice (dx)",
        " r": "Roll",
        " date": "Date",
        " dmg": "Damage",
    },
)
