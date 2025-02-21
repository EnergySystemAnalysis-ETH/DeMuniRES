import pandas as pd
import plotly.graph_objects as go
import sys

# Command line arguments to get the paths of CSV files
csv_file_path = sys.argv[1]
battery_csv_path = sys.argv[2]  # New CSV file with battery capacity

# Read the battery capacity from the CSV file
battery_data = pd.read_csv(battery_csv_path, header=0)
battery_capacity = battery_data.iloc[0, 1] / 1000  # Extract capacity (convert from Wh to kWh)

# Read the main CSV file into a pandas DataFrame
data = pd.read_csv(csv_file_path, header=0)

# Extract the time column and other columns for plotting
time = pd.to_datetime(data.iloc[:, 0], errors='coerce')  # Assuming the first column is time
battery_state_column = data.columns[1]  # Extract the battery state column

# Filter out non-numeric values in the battery state column
data[battery_state_column] = pd.to_numeric(data[battery_state_column], errors='coerce')

# Convert values from Wh to SoC (%) by dividing by battery capacity and multiplying by 100
data[battery_state_column] = (data[battery_state_column] / 1000.0 / battery_capacity) * 100

# Drop non-numeric columns before resampling
data_numeric = data.set_index(time)[[battery_state_column]]

# Aggregate data by hour, day, and month-start
hourly_data = data_numeric.resample('h').mean()
daily_data = data_numeric.resample('D').mean()
monthly_data = data_numeric.resample('MS').mean()  # Use 'MS' for month-start

def create_plot(aggregation_type):
    if aggregation_type == 'hourly':
        plot_data = hourly_data
        title = 'Hourly State of Charge (SoC)'
        tick_format = '%d-%b'
    elif aggregation_type == 'daily':
        plot_data = daily_data
        title = 'Daily State of Charge (SoC)'
        tick_format = '%d-%b'
    elif aggregation_type == 'monthly':
        plot_data = monthly_data
        title = 'Monthly State of Charge (SoC)'
        tick_format = '%d-%b'
    else:
        raise ValueError("Invalid aggregation type. Use 'hourly', 'daily', or 'monthly'.")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=plot_data.index, y=plot_data[battery_state_column],
                             mode='lines', name='Battery SoC'))

    # Calculate max and average values as floats
    max_value = plot_data[battery_state_column].max()
    average_value = plot_data[battery_state_column].mean()
    avg_kwh = average_value * battery_capacity / 100  # Convert average percentage back to kWh
    avg_percentage = f"{average_value:.1f}%"
    max_time = plot_data[battery_state_column].idxmax()

    # Add lines for max and average values
    fig.add_trace(go.Scatter(
        x=[plot_data.index.min(), plot_data.index.max()],
        y=[max_value, max_value],
        mode='lines',
        line=dict(dash='dash', color='red'),
        name=f'Max Value: {max_value:.1f}%'
    ))
    fig.add_trace(go.Scatter(
        x=[plot_data.index.min(), plot_data.index.max()],
        y=[average_value, average_value],
        mode='lines',
        line=dict(dash='dash', color='green'),
        name=f'Avg Value: {avg_percentage} ({avg_kwh:.2f} kWh)'
    ))

    # Add annotation for max value
    if pd.notnull(max_time):
        fig.add_trace(go.Scatter(
            x=[max_time], y=[max_value],
            mode='markers+text',
            marker=dict(color='red', size=10),
            text=[f'Max at {max_time.strftime("%Y-%m-%d %H:%M")}'],
            textposition='top center',
            name='Max Point'
        ))

    # Update layout
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 28, 'weight': 'bold'}
        },
        xaxis_title='Time',
        yaxis_title='SoC (%)',
        xaxis={
            'tickformat': tick_format,
            'tickangle': 45,
            'title_font': {'size': 24},
            'tickfont': {'size': 20}
        },
        yaxis={
            'tickmode': 'auto',
            'nticks': 10,
            'title_font': {'size': 24},
            'tickfont': {'size': 20}
        },
        template='plotly_white',
        legend={
            'font': {'size': 18},
            'title_text': None
        },
        hovermode='x'
    )

    # Add battery capacity to legend
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(size=0),
        name=f'Battery Capacity: {battery_capacity:.2f} kWh'
    ))

    return fig

# Create and show plots for each aggregation type
aggregation_types = ['hourly', 'daily', 'monthly']
for aggregation in aggregation_types:
    fig = create_plot(aggregation)
    fig.show()
