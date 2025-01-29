import pandas as pd
import plotly.graph_objects as go
import sys

# ------------------------------------------------------------------------------
# 1) Command line argument for the CSV file path
# ------------------------------------------------------------------------------
csv_file_path = sys.argv[1]

# ------------------------------------------------------------------------------
# 2) Read CSV and rename columns
#    0: Time
#    1: District1
#    2: District2
# ------------------------------------------------------------------------------
data = pd.read_csv(csv_file_path, header=0)

# Rename columns for clarity
data.rename(columns={
    data.columns[0]: 'Time',
    data.columns[1]: 'District1',
    data.columns[2]: 'District2'
}, inplace=True)

# ------------------------------------------------------------------------------
# 3) Convert columns to proper dtypes (datetime, numeric)
# ------------------------------------------------------------------------------
data['Time'] = pd.to_datetime(data['Time'], errors='coerce')
data['District1'] = pd.to_numeric(data['District1'], errors='coerce')
data['District2'] = pd.to_numeric(data['District2'], errors='coerce')

# ------------------------------------------------------------------------------
# 4) Aggregate data for daily and monthly views
#    Note: resample requires 'Time' to be recognized as a DateTimeIndex
# ------------------------------------------------------------------------------
daily_data = data.resample('D', on='Time').sum()
monthly_data = data.resample('MS', on='Time').sum()

# ------------------------------------------------------------------------------
# 5) Compute annual sums (in kWh) for the legend
#    If District1, District2 were in Wh, we divide by 1000 to get kWh
# ------------------------------------------------------------------------------
annual_dist1 = data['District1'].sum() / 1000.0
annual_dist2 = data['District2'].sum() / 1000.0

# ------------------------------------------------------------------------------
# 6) Create a function to generate time-series plots (hourly, daily, monthly)
# ------------------------------------------------------------------------------
def create_plot(view_type):
    # Decide which DataFrame to plot
    if view_type == 'hourly':
        plot_data = data.set_index('Time')
        title = 'Hourly Imported Electricity to Districts'
    elif view_type == 'daily':
        plot_data = daily_data
        title = 'Daily Imported Electricity to Districts'
    elif view_type == 'monthly':
        plot_data = monthly_data
        title = 'Monthly Imported Electricity to Districts'
    else:
        raise ValueError("Invalid view type. Choose from 'hourly', 'daily', or 'monthly'.")

    # Create the figure
    fig = go.Figure()

    # District 1 line (convert Wh → kWh)
    fig.add_trace(go.Scatter(
        x=plot_data.index,
        y=plot_data['District1'] / 1000,
        mode='lines',
        name='To District 1',
        line=dict(width=2)
    ))

    # District 2 line (convert Wh → kWh)
    fig.add_trace(go.Scatter(
        x=plot_data.index,
        y=plot_data['District2'] / 1000,
        mode='lines',
        name='To District 2',
        line=dict(width=2)
    ))

    # ---- Dummy traces for annual totals in the legend ----
    fig.add_trace(go.Scatter(
        x=[None],  # no actual data
        y=[None],
        mode='lines',
        line=dict(color='rgba(0,0,0,0)'),  # invisible line
        showlegend=True,
        name=f'Annual Imported to Dist.1: {annual_dist1:.2f} kWh'
    ))
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='lines',
        line=dict(color='rgba(0,0,0,0)'),
        showlegend=True,
        name=f'Annual Imported to Dist.2: {annual_dist2:.2f} kWh'
    ))
    # ------------------------------------------------------

    # Update layout
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 30, 'weight': 'bold'}
        },
        xaxis_title='Time',
        yaxis_title='Imported Electricity (kWh)',
        template='plotly_white',
        hovermode='x',
        xaxis=dict(
            tickformat='%d-%b',   # example date format, e.g. "06-Jan"
            title_font=dict(size=24),
            tickfont=dict(size=18)
        ),
        yaxis=dict(
            title_font=dict(size=24),
            tickfont=dict(size=18)
        ),
        legend=dict(
            font=dict(size=20)
        )
    )

    return fig

# ------------------------------------------------------------------------------
# 7) Generate and show plots for each view type
# ------------------------------------------------------------------------------
view_types = ['hourly', 'daily', 'monthly']
for view_type in view_types:
    fig = create_plot(view_type)
    fig.show()
