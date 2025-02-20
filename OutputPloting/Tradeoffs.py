import sys
import pandas as pd
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# Command line arguments:
#   sys.argv[1] -> path to flows CSV  (e.g., ImportE_CHP_GasBoiler.csv)
#   sys.argv[2] -> path to carbon intensities CSV (e.g., Commodity_Carbon_Intensity.csv)
#   sys.argv[3] -> path to objectives CSV
# ---------------------------------------------------------------------------

flows_csv = sys.argv[1]
intensity_csv = sys.argv[2]
objectives_csv = sys.argv[3]

# ---------------------------------------------------------------------------
# 1) Read input data
# ---------------------------------------------------------------------------

flows_df = pd.read_csv(flows_csv)
intensity_df = pd.read_csv(intensity_csv)
objectives_df = pd.read_csv(objectives_csv)

# ---------------------------------------------------------------------------
# 2) Dictionary to map recognized units to intensity sources.
#    e.g. if "Import_E" in unit name -> "Grid" in intensity CSV
#	 please update or extend if emissions from other commodities or energy systems are to be considered
# ---------------------------------------------------------------------------

unit_to_intensity_key = {
    "Import_E": "Grid",
    "CHP": "CHP",
    "GasBoiler": "Gas"
}

def map_unit_to_intensity_source(unit_name):
    """
    Return the appropriate emission source (e.g., "Grid", "CHP", "Gas")
    based on partial matching of certain keywords. If none match, returns None.
    """
    for keyword, source in unit_to_intensity_key.items():
        if keyword in unit_name:
            return source
    return None

# ---------------------------------------------------------------------------
# 3) Build an intensity map, e.g. {"Grid": 72, "CHP": 80, "Gas": 198}
# ---------------------------------------------------------------------------

intensity_map = intensity_df.set_index(intensity_df.columns[0])[intensity_df.columns[1]].to_dict()

# ---------------------------------------------------------------------------
# 4) Convert flows from Wh to kWh, then compute emissions (g CO2-eq)
# ---------------------------------------------------------------------------

flows_df['Value_kWh'] = flows_df['Value'] / 1000.0
flows_df['IntensitySource'] = flows_df['Unit'].apply(map_unit_to_intensity_source)

def compute_emission_g(row):
    source = row['IntensitySource']
    if source in intensity_map:
        return row['Value_kWh'] * intensity_map[source]
    else:
        return 0.0

flows_df['Emission_g'] = flows_df.apply(compute_emission_g, axis=1)

# ---------------------------------------------------------------------------
# 5) Sum up total emissions per scenario in grams, then convert to tons
# ---------------------------------------------------------------------------

scenario_emissions_df = flows_df.groupby('Scenario', as_index=False)['Emission_g'].sum()
scenario_emissions_df['Emission_t'] = scenario_emissions_df['Emission_g'] / 1e6  # g -> t

# ---------------------------------------------------------------------------
# 6) Read objectives and convert total_costs from CHF to million CHF
# ---------------------------------------------------------------------------

objectives_df['Costs_mCHF'] = objectives_df['total_costs'] / 1e6

costs_map = dict(zip(objectives_df['Scenario'], objectives_df['Costs_mCHF']))
scenario_emissions_df['Costs_mCHF'] = scenario_emissions_df['Scenario'].map(costs_map)

# Drop scenarios that are missing cost or emission values
scenario_emissions_df.dropna(subset=['Emission_t', 'Costs_mCHF'], inplace=True)

# ---------------------------------------------------------------------------
# 7) Prepare data for plotting
# ---------------------------------------------------------------------------

plot_scenarios = scenario_emissions_df['Scenario'].tolist()
x_vals = scenario_emissions_df['Costs_mCHF'].tolist()
y_vals = scenario_emissions_df['Emission_t'].tolist()

# ---------------------------------------------------------------------------
# 8) Define ETH Blue color gradations for up to 7 scenarios
#    Starting from darkest to lightest
# ---------------------------------------------------------------------------

color_list = [
    "#00234B",  # 1) Extra darker
    "#08407E",  # 2) 120%
    "#4D7DBF",  # 3) 80%
    "#7A9DCF",  # 4) 60%
    "#A6BEDF",  # 5) 40%
    "#D3DEEF",  # 6) 20%
    "#E9EFF7",  # 7) 10%
]

if len(plot_scenarios) > 7:
    # If you have more than 7 scenarios, either re-use the last color
    # or please expand color_list with more desired colors.
    pass

marker_colors = []
for i in range(len(plot_scenarios)):
    marker_colors.append(color_list[i] if i < 7 else color_list[-1])

# ---------------------------------------------------------------------------
# 9) Create Plotly scatter plot (one point per scenario)
#    Larger points: size=20
# ---------------------------------------------------------------------------

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x_vals,
    y=y_vals,
    mode='markers+text',
    text=plot_scenarios,             # label the point with the scenario name
    textposition='top center',
    marker=dict(size=20, color=marker_colors),
    textfont=dict(size=16),
    name='Scenarios'
))

# ---------------------------------------------------------------------------
# 10) Update layout (axes range, title, margins, etc.)
# ---------------------------------------------------------------------------

x_min, x_max = min(x_vals), max(x_vals)
y_min, y_max = min(y_vals), max(y_vals)

# Add some padding so points near edges don’t overlap with the axis
x_range = [x_min * 0.95 if x_min > 0 else 0, x_max * 1.05]
y_range = [y_min * 0.95 if y_min > 0 else 0, y_max * 1.05]

fig.update_layout(
    title={
        'text': 'Total Costs vs Total Carbon Emissions',
        'x': 0.5,
        'y': 0.95,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 28, 'weight': 'bold'}
    },
    xaxis=dict(
        range=x_range,
        title='Total Costs (million CHF)',
        title_font=dict(size=24),
        tickfont=dict(size=20)
    ),
    yaxis=dict(
        range=y_range,
        title='Total Carbon Emissions (t CO2-eq)',
        title_font=dict(size=24),
        tickfont=dict(size=20)
    ),
    margin=dict(l=80, r=80, t=80, b=80),
    template='plotly_white'
)

fig.show()