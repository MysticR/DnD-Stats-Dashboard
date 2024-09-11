import pandas as pd
import plotly.graph_objects as go

# char_list = list(stats.char.unique())[::-1]


def d20(selected_char):
    stats = pd.read_csv("C:/Users/rahma/OneDrive/Documents/DnD/Stats/stats.txt")
    mdf_selected_char = stats[stats.char == selected_char]
    md20 = mdf_selected_char[mdf_selected_char[" d"] == 20]
    md20hit = md20[md20[" dmg"] == 0]
    return md20hit


# Data for different characters
md20 = d20("M")
gd20 = d20("G")
fd20 = d20("F")

# Create box plot figure
fig = go.Figure()

# Add box plots
fig.add_trace(go.Box(y=md20[" r"], name="Meluk"))
fig.add_trace(go.Box(y=gd20[" r"], name="Gehrman"))
fig = fig.add_trace(go.Box(y=fd20[" r"], name="Far"))
