# Exporter

Below are some charateristics of the Exporters and suggestions on modifying for future expansion of the DeMuniRES model.

## Battery_SoC

The ***Parameter definitions*** is filtered with the expression ***node_state_cap*** and the ***Entities*** is set to be ***BatterySto*** to extract the rated capacity of the battery in Wh from InputDB. Future additional batteries should follow this naming format, e.g. ***BatterySto(District1_E)***.

## Battery_state

The ***Parameter definitions*** is filtered with the expression ***node_state*** and the ***Entities*** is set to be ***BatterySto*** to extract the time series of the electricity remaining in battery in Wh from OutputDB. 

## Import_Elec

The ***Parameter definitions*** is filtered with the expression ***unit_flow*** and the ***Entities*** is filtered with the expression ***variables.\*Import_E.\*Distric1_E|variables.\*Import_E.\*Distric2_E*** to extract the time series of the imported electricity to the districts (currently only District 1 and 2 available) in Wh from OutputDB. The filtering expression may be modified or extended when additional districts are to be included.

## ImportE_CHP_GasBoiler

The ***Parameter definitions*** is filtered with the expression ***^(unit_flow|connection_flow)$*** and the ***Entities*** is filtered with the expression ***.\*(Import|CHP|GasBoiler).\**** to extract the time series of the unit flows or energy flows of different energy sources to and from the nodes (currently, only grid electricity, CHP units, and gas boilers are considered for carbon emissions) in Wh from OutputDB. The filtering expression may be modified or extended when additional energy sources are considered for carbon emissions.

## objectives

The ***Entities*** is set to be ***objective*** to extract the optimized results of different costs (objectives) of different scenarios in CHF from OutputDB. Currently, only fuel costs, connection flow costs, fixed O&M costs, and variable O&M costs are present. More costs will be available once relevant economic parameters are configured in the InputDB.

## Carbon_Intensity (Data Connection item)

Connects the external CSV file of the directory of emission factors of different energy sources (currently, only grid electricity, CHP, and gas boilers are considered). Future improvement shoudl consider integrating this directory into InputDB for enabling alternative values for uncertainties and scenario comparisons.

## unit_or_connection_flow_export

Similar to *ImportE_CHP_GasBoiler*, but extracts time series of all unit flows or connection flows to and from the nodes Values to the nodes can be viewed as "supplies", while values from the nodes can be viewed as "excess".

## demand_export

Extracts the time series of demand of each node from the InputDB.
