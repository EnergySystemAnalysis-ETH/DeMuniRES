# Tools (Python-based visualizations)

Below are some charateristics of the Python scripts for data visualizations and suggestions on modifying for future expansion of the DeMuniRES model.

## Battery_SoC

Receives the rated battery capacity value from the Exporter *battery_capacity* and the time series of the battery's remaining electrical energy in Wh from the Exporter *battery_state*. Generate three line charts of hourly, daily, and monthly resolutions of the battery's SoC. 

## Import_E_to_Districts

Receives the time series of the imported electricity to the districts (currenly only District 1 and 2) from the Exporter *Import_Elec* and battery capacity value from the Exporter *battery_capacity* and visualize them in three line charts of hourly, daily, and monthly resolutions. Additional colors should be defined if more districts are to be included.


## Tradeoffs

Three input files are required: time series of energy flows of the imported electricity, CHP, and gas boilers from the Exporter "ImportE_CHP_GasBoiler", system costs from the Exporter *objectives", and emission factors of the energy sources (currently grid electricity, CHP, and gas boilers) from the Data Connection *Carbon_Intensity*. Time series of the energy sources are multiplied with their corresponding emission factor, and aggregated to give the annual total emissions, which is shown on y-axis of a scatter plot as one of the two KPIs used for scenario comparison. Different system costs are summed to give the total costs and displayed on the x-axis as the other KPI used. Different pairs KPIs could be implemented for future development, or a third KPI can be in terms of e.g. color gradients or sizes of the scatter points. Currently, 7 blue colors of different intensities are defined. More colors can be added when more than 7 scenarios are compared.

## system_costs


Receives the cost breakdowns of the scenarios from the Exporter *objectives* and displays the results in a stacked bar chart. Currently, 7 blue colors of different intensities are defined. More colors can be added when more than 7 types of costs are available.

## Carbon_Emission

Receives the emission factors from the Data Connection *Carbon_Intensity* and energy flow time series from the Exporter *unit_or_connection_flow_export*. Generates a stacked bar chart of the annual total emissions by month of a specific scenario. Currently, 7 brown colors of different intensities are defined. More colors can be added when more than 7 types of costs are available.

## supply_node

Receives the time series of the annual unit flows or connection flows to and from the nodes from the Exporter *unit_or_connection_flow_export*, and generates 3 stacked bar charts with node (building), district, and municipality levels. Aggregated values to the nodes are considered positive as supplies and displayed in green (energy sources are reflected by segments of different intensities); while aggregated values from the nodes are considered negative as excess and displayed in red. Currently, 1 red color and 8 green colors of different intensities are defined. More colors can be added when additional energy sources are involved.

## energy_balance

Receives the time series of the annual unit flows or connection flows to and from the nodes from the Exporter *unit_or_connection_flow_export* and the demand from the Exporter *demand_export*. Generates 3 stacked bar charts with node (building), district, and municipality levels. Aggregated unit or connection flows to the nodes are considered positive as supplies and displayed in green (energy sources are reflected by segments of different intensities); aggregated unit or connection flows from the nodes are considered negative as excess and displayed in red; and aggregated demand values are displayed in blue. Currently, 1 red color, 1 blue color, and 8 green colors of different intensities are defined. More colors can be added when additional energy sources are involved. For future improvement, demand values should also be segmented into different color intensities to reflect more specific demands.

## demand_node

Receives the time series of the annual demands of the nodes from the Exporter *demand_export*, and generates 3 stacked bar charts with node (building), district, and municipality levels. Currently, only 1 blue color is defined. More colors can be added when additional energy sources are involved. For future improvement, demand values should also be segmented into different color intensities to reflect more specific demands.
