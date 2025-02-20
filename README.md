# DeMuniRES

Repository for **De**centralised **Muni**cipality **R**enewable **E**nergy **S**ystem model

## Environment configuration

1. Python environment for [`spinetoolbox`](https://github.com/spine-tools/Spine-Toolbox)

- Prerequisites: 
	- **python 3.13**
	- [git](https://git-scm.com/downloads)

- **Option 1** Installation in [miniconda](https://docs.conda.io/en/latest/miniconda.html)

    - In OS terminal (cmd or PowerShell):

        ```console
        conda create -n DeMuniRES python=3.13 plotly
        conda activate DeMuniRES
        ```

    - Install the active dev version `spinetoolbox` (need `git` installed):

        ```console
        pip install git+https://github.com/spine-tools/spinetoolbox-dev
        ```
    
    - Update package to the latest commit: reinstall the package using the same command.

2. Set up Julia envirionment and `SpineOpt.jl` in the `spinetoolbox`

    - forllow the [instruction](https://spine-toolbox.readthedocs.io/en/latest/how_to_run_spineopt.html)

# Mathematical model

The project is built upon the existing optimization model RE3ASON: *Mainzer, K. (2019)*. **Analyse und Optimierung urbaner Energiesysteme - Entwicklung und Anwendung eines übertragbaren Modellierungswerkzeugs zur nachhaltigen Systemgestaltung**. Karlsruhe. [![DOI:10.5445/IR/1000092481](https://zenodo.org/badge/DOI/10.5445/IR/1000092481.svg)](https://doi.org/10.5445/IR/1000092481)

# Framework
The project utilizes the following frameworks:
* the SpineToolbox framework: *Kiviluoma, J., Pallonetto, F., Marin, M., Savolainen, P. T., Soininen, A., Vennström, P., … Dillon, J. (2022)*. **Spine Toolbox: A flexible open-source workflow management system with scenario and data management**. SoftwareX, 17. [![DOI:10.1016/J.SOFTX.2021.100967](https://zenodo.org/badge/DOI/10.1016/J.SOFTX.2021.100967.svg)](https://doi.org/10.1016/J.SOFTX.2021.100967)
* the SpineOpt plugin: *Ihlemann, M., Kouveliotis-Lysikatos, I., Huang, J., Dillon, J., O'Dwyer, C., Rasku, T., Marin, M., Poncelet, K., & Kiviluoma, J. (2022)*. **SpineOpt: A flexible open-source energy system modelling framework**. Energy Strategy Reviews, 43, [100902]. [![DOI:10.1016/J.ESR.2022.100902](https://zenodo.org/badge/DOI/10.1016/J.ESR.2022.100902.svg)](https://doi.org/10.1016/j.esr.2022.100902)
