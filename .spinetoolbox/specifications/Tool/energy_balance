import pandas as pd
import plotly.graph_objects as go
import sys
import re

#
# 1) Define the same map to aggregate unit names into fewer categories
#    (as in your "supply_node" script)
#
unit_aggregation_map = {
    r"^Battery.*":           "Battery",
    r"^CHP_.*":              "CHP",
    r"^Edistr.*":            "District Grid Electricity",
    r"^Hdistr.*":            "District Heating",
    r"^HeatPump.*":          "Heat Pump",
    r"^Import_E.*":          "Imported Electricity",
    r"^RooftopPV.*":         "PV",
    r"^GasBoiler_.*":        "Gas Boiler",
    # fallback: remain unchanged
}

def aggregate_unit_name(unit_name: str) -> str:
    for pattern, agg_name in unit_aggregation_map.items():
        if re.match(pattern, unit_name):
            return agg_name
    return unit_name

#
# 2) Read CSVs from command line
#
demand_csv_path = sys.argv[1]   # e.g. demand_export
flow_csv_path   = sys.argv[2]   # e.g. unit_or_connection_flow_export

demand_data = pd.read_csv(demand_csv_path, header=0)
flow_data   = pd.read_csv(flow_csv_path,   header=0)

# Convert times to datetime
demand_data['Time'] = pd.to_datetime(demand_data['Time'], errors='coerce')
flow_data['Time']   = pd.to_datetime(flow_data['Time'],   errors='coerce')

#
# 3) Classify each row in flow_data by its AggregatedSource
#
flow_data['AggregatedSource'] = flow_data['Unit'].apply(aggregate_unit_name)

#
# 4) Separate flow_data into "to_node" (supply) and "from_node" (exports)
#    Then sum up the MWh for each (Node, AggregatedSource)
#    Note: converting from kWh to MWh by dividing by 1,000,000
#
to_node_df = flow_data[flow_data['Direction'].str.lower().str.strip() == 'to_node'].copy()
to_node_df['Value_MWh'] = to_node_df['Value'] / 1_000_000

from_node_df = flow_data[flow_data['Direction'].str.lower().str.strip() == 'from_node'].copy()
from_node_df['Value_MWh'] = from_node_df['Value'] / 1_000_000

#
# 5) Sum demand (also converting to MWh)
#
demand_data['Demand_MWh'] = demand_data['Demand'] / 1_000_000

#
# 6) Figure out which nodes appear in both demand and flow data
#
nodes_demand = demand_data['Node'].unique()
nodes_flow   = flow_data['Node'].unique()
common_nodes = sorted(set(nodes_demand).intersection(set(nodes_flow)))

#
# 7) Summarize supply by (node, aggregated source)
#
grouped_supply = (
    to_node_df.groupby(['Node','AggregatedSource'], as_index=False)['Value_MWh']
    .sum()
)

# Pivot so each supply source is a separate column
pivot_supply = grouped_supply.pivot(
    index='Node',
    columns='AggregatedSource',
    values='Value_MWh'
).fillna(0)

# Keep only the common nodes, reindex in sorted order
pivot_supply = pivot_supply.reindex(common_nodes, fill_value=0)

#
# 8) Summarize from_node as a single "Export to District Network" column
#
grouped_export = from_node_df.groupby('Node', as_index=False)['Value_MWh'].sum()
export_map = dict(zip(grouped_export['Node'], grouped_export['Value_MWh']))

#
# 9) Summarize demand as a single column
#
grouped_demand = demand_data.groupby('Node', as_index=False)['Demand_MWh'].sum()
demand_map = dict(zip(grouped_demand['Node'], grouped_demand['Demand_MWh']))

#
# 10) Build a final DataFrame with:
#     - each supply source as a column,
#     - one column for 'Export to District Network'
#     - one column for 'Demand'
#
final_df = pivot_supply.copy()
final_df['Export to District Network'] = final_df.index.map(export_map).fillna(0)
final_df['Demand'] = final_df.index.map(demand_map).fillna(0)

# For convenience, store node names in a column (rather than the index)
final_df.reset_index(inplace=True)
final_df.rename(columns={'index':'Node'}, inplace=True)

#
# 11) Add District and Municipality columns
#
def get_district(node_name):
    # Example logic: if 'District1' in name => District1, else District2
    return 'District1' if 'District1' in node_name else 'District2'

final_df['District'] = final_df['Node'].apply(get_district)
final_df['Municipality'] = 'Municipality'  # Single municipality, as per original code

#
# 12) Create aggregated DataFrames for district and municipality
#
district_aggregates = final_df.groupby('District', as_index=True).sum()
municipality_aggregates = final_df.groupby('Municipality', as_index=True).sum()

#
# 13) Prepare color arrays
#     We have up to 8 supply categories, each with a green shade
#     Demand: #4d7dbf
#     Export: #C51017
#
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

# We will plot all supply columns in the order they appear. If there are more
# supply columns than 8, they’ll wrap around color array (or you could merge them).
#
# We do NOT rename or reorder columns here—since you used the aggregator map,
# you should only get up to 8 distinct supply categories anyway.
#
def create_plot(df, x_labels, title_text):
    """Stacked bar for supply columns + single bar for export + single bar for demand."""
    fig = go.Figure()

    # Identify the supply columns by removing the known columns:
    known_cols = {'Node','District','Municipality','Export to District Network','Demand'}
    supply_cols = [c for c in df.columns if c not in known_cols]
    
    # Add one trace per supply category (positive values)
    for i, col in enumerate(supply_cols):
        fig.add_trace(go.Bar(
            x=x_labels,
            y=df[col],  # supply is positive
            name=col,
            marker_color=green_shades[i % len(green_shades)],
            # We want them stacked, so no negative sign
        ))
    
    # Export to district network (plot as negative or separate? 
    # The original code plots "Export" as negative. 
    # If you want it downward, do `y = -df['Export to District Network']`
    # or keep it upright. If you want to replicate the old approach of a
    # negative bar, do the minus sign below:
    export_values = -df['Export to District Network']
    fig.add_trace(go.Bar(
        x=x_labels,
        y=export_values,
        name='Export to District Network',
        marker_color='#C51017',
    ))

    # Demand (also negative if we want it to go downward)
    demand_values = -df['Demand']
    fig.add_trace(go.Bar(
        x=x_labels,
        y=demand_values,
        name='Demand',
        marker_color='#4d7dbf',
    ))

    # Layout
    fig.update_layout(
        title={
            'text': title_text,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 28, 'weight': 'bold'}
        },
        xaxis_title=title_text.replace('Energy Balance per ', ''),
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

#
# 14) Build & show the three plots:
#     a) per node
#     b) per district
#     c) per municipality
#

# (a) Per node
df_node = final_df.copy()
fig_node = create_plot(
    df_node, 
    x_labels=df_node['Node'],
    title_text='Energy Balance per Node'
)
fig_node.show()

# (b) Per district
df_dist = district_aggregates.copy()
fig_dist = create_plot(
    df_dist, 
    x_labels=df_dist.index,
    title_text='Energy Balance per District'
)
fig_dist.show()

# (c) Per municipality
df_muni = municipality_aggregates.copy()
fig_muni = create_plot(
    df_muni, 
    x_labels=df_muni.index,
    title_text='Energy Balance per Municipality'
)
fig_muni.show()
