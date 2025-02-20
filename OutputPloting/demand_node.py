import pandas as pd
import plotly.graph_objects as go
import sys

# Command line arguments to get the path of CSV file
demand_csv_path = sys.argv[1]

# Read the CSV file into pandas DataFrame
demand_data = pd.read_csv(demand_csv_path, header=0)

# Convert the time index to datetime
demand_data['Time'] = pd.to_datetime(demand_data.iloc[:, 0], errors='coerce')

# Extract unique nodes from the demand dataset
nodes = demand_data['Node'].unique()

# Initialize dictionary to store aggregate values
demand_aggregates = {node: 0 for node in nodes}

# Aggregate values for each node
for node in nodes:
    demand_aggregates[node] = pd.to_numeric(
        demand_data[demand_data['Node'] == node]['Demand'], errors='coerce'
    ).sum() / 1_000_000  # Convert to MWh

# Create the main DataFrame for plotting
demand_df = pd.DataFrame({
    'Node': list(nodes),
    'Demand': [demand_aggregates[node] for node in nodes],
})

# Add District and Municipality columns
def get_district(node_name):
    # Example logic: if 'District1' in name => District1, else District2
    return 'District1' if 'District1' in node_name else 'District2'

demand_df['District'] = demand_df['Node'].apply(get_district)
demand_df['Municipality'] = 'Municipality'  # Single municipality, as per original code

# Aggregate values by district and municipality
district_aggregates = demand_df.groupby('District', as_index=True).sum()
municipality_aggregates = demand_df.groupby('Municipality', as_index=True).sum()

# Function to create a bar plot for a specific view type
def create_plot(df, x_labels, title_text):
    """Bar plot for demand data."""
    fig = go.Figure()

    # Add bars for demand
    fig.add_trace(go.Bar(
        x=x_labels,
        y=df['Demand'],
        name='Demand',
        marker_color='#4d7dbf'  # Blue color for demand
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
        xaxis_title=title_text.replace('Aggregated Demand per ', ''),
        yaxis_title='Energy (MWh)',
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

# Generate plots for each view type
# (a) Per node
fig_node = create_plot(
    demand_df,
    x_labels=demand_df['Node'],
    title_text='Annual Demand per Node'
)
fig_node.show()

# (b) Per district
fig_district = create_plot(
    district_aggregates,
    x_labels=district_aggregates.index,
    title_text='Annual Demand per District'
)
fig_district.show()

# (c) Per municipality
fig_municipality = create_plot(
    municipality_aggregates,
    x_labels=municipality_aggregates.index,
    title_text='Annual Demand per Municipality'
)
fig_municipality.show()
