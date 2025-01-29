import pandas as pd
import plotly.graph_objects as go
import sys

# Command-line argument: path to CSV file with multiple scenarios
csv_file_path = sys.argv[1]

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path, header=0)

# Define the objectives we want to stack
# For this toy model, the total costs only consist these 4 costs. Please update and extend if more costs are to contribute to total costs
objectives_map = {
    'objective_connection_flow_costs': 'Connection Flow',
    'objective_fixed_om_costs': 'Fixed O&M',
    'objective_fuel_costs': 'Fuel Costs',
    'objective_variable_om_costs': 'Variable O&M',
}

# Filter only the columns we need and ensure they exist in df
cost_columns = [col for col in objectives_map if col in df.columns]

# Choose colors from the ETH corporate design palette
# For this toy model, only 4 colors are chosen for the 4 costs above. Please update or extend if desired or needed.
eth_colors = [
    "#00234B",  # 1) Extra darker
    "#08407E",  # 2) 120%
    "#4D7DBF",  # 3) 80%
    "#7A9DCF",  # 4) 60%
    "#A6BEDF",  # 5) 40%
    "#D3DEEF",  # 6) 20%
    "#E9EFF7",  # 7) 10%
]

# Set bar width
bar_width = 0.5

# Create the plot
fig = go.Figure()

# Add one stacked bar trace for each cost objective
for i, col in enumerate(cost_columns):
    fig.add_trace(go.Bar(
        x=df['Scenario'],             # Each scenario on x-axis
        y=df[col],                    # Values for this particular cost objective
        name=objectives_map[col],     # More readable name in legend
        marker_color=eth_colors[i % len(eth_colors)],  # Cycle through selected ETH colors
        width=bar_width               # Make bars thinner
    ))

# Update layout for a stacked bar chart and improved formatting
fig.update_layout(
    title={
        'text': 'Urban Energy System Costs',
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 30, 'weight': 'bold'}
    },
    xaxis_title='Scenario',
    yaxis_title='Cost (CHF)',
    template='plotly_white',
    barmode='stack',  # Stack bars for each scenario
    legend=dict(
        font=dict(size=20)
    ),
    xaxis=dict(
        zeroline=False,
        tickangle=45,
        title_font=dict(size=24),
        tickfont=dict(size=18),
        categoryorder='category ascending',  # Ensure proper ordering
        tickvals=df['Scenario'].unique(),    # Avoid overlaps
        tickmode='array'
    ),
    yaxis=dict(
        zeroline=False,
        title_font=dict(size=24),
        tickfont=dict(size=18)
    ),
    hovermode='x'
)

# Show the figure
fig.show()
