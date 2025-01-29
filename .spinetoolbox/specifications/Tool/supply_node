import re
import sys
import pandas as pd
import plotly.graph_objects as go

# --------------------------------------------------------------------------
# 1) Command-line arguments
# --------------------------------------------------------------------------
flow_csv_path = sys.argv[1]

# --------------------------------------------------------------------------
# 2) Read CSV and check columns
# --------------------------------------------------------------------------
flow_data = pd.read_csv(flow_csv_path, header=0)
flow_data['Time'] = pd.to_datetime(flow_data['Time'], errors='coerce')

required_cols = {'Node', 'Direction', 'Value', 'Unit'}
if not required_cols.issubset(flow_data.columns):
    raise ValueError(f"Flow data must have columns {required_cols}")

# Convert from kWh to MWh if your CSV is in kWh
flow_data['Value_MWh'] = flow_data['Value'] / 1_000_000

# --------------------------------------------------------------------------
# 3) Define a map to aggregate unit names into fewer categories
# --------------------------------------------------------------------------
unit_aggregation_map = {
    r"^Battery.*":     "Battery",
    r"^CHP_.*":        "CHP",
    r"^Edistr.*":      "District Grid Electricity",
    r"^Hdistr.*":      "District Heating",
    r"^HeatPump.*":    "Heat Pump",
    r"^Import_E.*":    "Imported Electricity",
    r"^RooftopPV.*":   "PV",
    r"^GasBoiler_.*":  "Gas Boiler",
    # fallback: remain unchanged
}

def aggregate_unit_name(unit_name: str) -> str:
    for pattern, agg_name in unit_aggregation_map.items():
        if re.match(pattern, unit_name):
            return agg_name
    return unit_name

flow_data['AggregatedSource'] = flow_data['Unit'].apply(aggregate_unit_name)

# --------------------------------------------------------------------------
# 4) Summarize "to_node" flows by (Node, AggregatedSource)
# --------------------------------------------------------------------------
to_node_df = flow_data[flow_data['Direction'].str.strip().str.lower() == 'to_node']
grouped_to_node = (
    to_node_df.groupby(['Node', 'AggregatedSource'], as_index=False)['Value_MWh']
    .sum()
)
to_node_pivot = grouped_to_node.pivot(
    index='Node', 
    columns='AggregatedSource', 
    values='Value_MWh'
).fillna(0)

# --------------------------------------------------------------------------
# 5) Summarize "from_node" flows by Node => negative bar
# --------------------------------------------------------------------------
from_node_df = flow_data[flow_data['Direction'].str.strip().str.lower() == 'from_node']
grouped_from_node = (
    from_node_df.groupby('Node', as_index=False)['Value_MWh']
    .sum()
)
grouped_from_node['Value_MWh'] = -grouped_from_node['Value_MWh']
excess_map = dict(zip(grouped_from_node['Node'], grouped_from_node['Value_MWh']))

# --------------------------------------------------------------------------
# 6) Add District and Municipality Columns
# --------------------------------------------------------------------------
def get_district(node_name):
    return 'District1' if 'District1' in node_name else 'District2' if 'District2' in node_name else None

to_node_pivot['District'] = [get_district(node) for node in to_node_pivot.index]
to_node_pivot['Municipality'] = ['Municipality' if district else None for district in to_node_pivot['District']]
to_node_pivot['Excess (Feed to District)'] = to_node_pivot.index.map(excess_map).fillna(0)

# --------------------------------------------------------------------------
# 7) Remove nodes without District1 or District2 for district/municipality views
# --------------------------------------------------------------------------
district_level_data = to_node_pivot[to_node_pivot['District'].notna()].groupby('District').sum()
municipality_level_data = to_node_pivot[to_node_pivot['Municipality'].notna()].groupby('Municipality').sum()

# --------------------------------------------------------------------------
# 8) Prepare color arrays for supply sources
# --------------------------------------------------------------------------
green_shades = [
    "#00441b",  # darkest
    "#006d2c",
    "#238b45",
    "#41ab5d",
    "#74c476",
    "#a1d99b",
    "#c7e9c0",
    "#e5f5e0"   # lightest
]

# --------------------------------------------------------------------------
# 9) Create Plotting Function
# --------------------------------------------------------------------------
def create_plot(df, x_labels, title_text):
    """Create a stacked bar plot."""
    fig = go.Figure()

    supply_categories = [col for col in df.columns if col not in ['District', 'Municipality', 'Excess (Feed to District)']]

    # Add bars for each supply category
    for i, category in enumerate(supply_categories):
        color = green_shades[i % len(green_shades)]
        fig.add_trace(go.Bar(
            x=x_labels,
            y=df[category],
            name=category,
            marker_color=color
        ))

    # Add bar for excess feed
    fig.add_trace(go.Bar(
        x=x_labels,
        y=df['Excess (Feed to District)'],
        name='Excess (Feed to District)',
        marker_color='#C51017'  # Red for excess
    ))

    # Layout settings
    fig.update_layout(
        title={
            'text': title_text,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 28, 'weight': 'bold'}
        },
        xaxis_title=title_text.replace('Aggregated Supply per ', ''),
        yaxis_title='Energy (MWh)',
        barmode='relative',
        template='plotly_white',
        legend={'font': {'size': 18}},
        hovermode='x',
        xaxis={
            'zeroline': False,
            'tickangle': 45,
            'title_font': {'size': 24},
            'tickfont': {'size': 20}
        },
        yaxis={
            'zeroline': False,
            'title_font': {'size': 24},
            'tickfont': {'size': 20}
        }
    )
    return fig

# --------------------------------------------------------------------------
# 10) Generate and Show Plots
# --------------------------------------------------------------------------
# (a) Per node
fig_node = create_plot(
    df=to_node_pivot.drop(columns=['District', 'Municipality']),
    x_labels=to_node_pivot.index,
    title_text='Annual Supply per Node'
)
fig_node.show()

# (b) Per district
fig_district = create_plot(
    df=district_level_data,
    x_labels=district_level_data.index,
    title_text='Annual Supply per District'
)
fig_district.show()

# (c) Per municipality
fig_municipality = create_plot(
    df=municipality_level_data,
    x_labels=municipality_level_data.index,
    title_text='Annual Supply per Municipality'
)
fig_municipality.show()
