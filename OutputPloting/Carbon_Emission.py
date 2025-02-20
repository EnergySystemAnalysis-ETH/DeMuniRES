import pandas as pd
import plotly.graph_objects as go
import sys

# File paths for the CSV and Excel files
unit_flow_data_path = sys.argv[1]
carbon_intensity_data_path = sys.argv[2]

# Load the CSV and Excel data
unit_flow_data = pd.read_csv(unit_flow_data_path)
carbon_intensity_data = pd.read_csv(carbon_intensity_data_path)

# Filter rows based on Unit and Direction and explicitly create a copy
filtered_data = unit_flow_data[
    (unit_flow_data['Unit'].str.contains("Import_E|CHP|Gas", na=False)) &
    (unit_flow_data['Direction'] == 'to_node')
].copy()

# Ensure 'Time' is properly converted to datetime
filtered_data['Time'] = pd.to_datetime(filtered_data['Time'])

# Create a dictionary for carbon intensity values
carbon_intensity_dict = dict(zip(carbon_intensity_data['Source'], carbon_intensity_data['Carbon Intensity (g CO2-eq / kWh)']))

# Add a column to identify the energy source
filtered_data['Energy Source'] = filtered_data['Unit'].apply(lambda x: x.split('_')[0])

# Map energy source names directly to carbon intensity values
carbon_intensity_mapping = {
    "Import": carbon_intensity_dict.get("Grid", 0),  # Map "Import" to "Grid" in Excel
    "CHP": carbon_intensity_dict.get("CHP", 0),
    "GasBoiler": carbon_intensity_dict.get("Gas", 0)  # Map "GasBoiler" to "Gas" in Excel
}

# Calculate carbon emissions explicitly by energy source
filtered_data['Carbon Emission (g CO2-eq)'] = filtered_data.apply(
    lambda row: row['Value'] * carbon_intensity_mapping.get(row['Energy Source'], 0),
    axis=1
)

# Convert emissions from (g CO2-eq) to (t CO2-eq) and convert unit flows from Wh to kWh 
filtered_data['Carbon Emission (t CO2-eq)'] = filtered_data['Carbon Emission (g CO2-eq)'] / 1_000_000 / 1_000

# Aggregate carbon emissions by energy source and time (in tons)
monthly_emissions = filtered_data.groupby([pd.Grouper(key='Time', freq='MS'), 'Energy Source'])['Carbon Emission (t CO2-eq)'].sum().unstack(fill_value=0)

# Define the colors from darkest to lightest
color_palette = [
    "#704F12",  # Darkest
    "#A58542",
    "#BBA471",
    "#D2C2A1",
    "#E8E1D0",
    "#F4F0E7"   # Lightest
]

# Define the plotting function
def plot_stacked_emissions(data, title, total_emissions):
    fig = go.Figure()

    # Add bars for each energy source
    for i, source in enumerate(data.columns):
        color = color_palette[i % len(color_palette)]  # Cycle through colors if more than 6 types
        fig.add_trace(go.Bar(
            x=data.index,
            y=data[source],
            name=source,
            marker_color=color
        ))

    # Add total emissions annotation
    total_emissions_annotation = f"Total Emissions: {total_emissions:.1f} t CO2-eq"

    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 30, 'weight': 'bold'}
        },
        barmode='stack',
        xaxis=dict(
            title='Time',
            title_font=dict(size=24),
            tickformat='%b',
            tickfont=dict(size=18)
        ),
        yaxis=dict(
            title='Carbon Emissions (t CO2-eq)',
            title_font=dict(size=24),
            tickfont=dict(size=18)
        ),
        legend=dict(
            font=dict(size=20)
        ),
        annotations=[
            dict(
                x=1.02,
                y=1.05,
                xref='paper',
                yref='paper',
                text=total_emissions_annotation,
                showarrow=False,
                font={'size': 20, 'color': 'black', 'weight': 'bold'}
            )
        ],
        template='plotly_white'
    )

    # Display the figure
    fig.show()

# Calculate the total emissions for monthly data (in tons)
monthly_total_emissions = monthly_emissions.sum().sum()

# Plot the monthly emissions with the new title
plot_stacked_emissions(monthly_emissions, "Total Carbon Emissions", monthly_total_emissions)
