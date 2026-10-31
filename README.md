# Reproducible GIS Quality Assurance Framework

[![Article: Geomatics](https://img.shields.io/badge/Journal-Geomatics%20(MDPI)-blue)](https://www.mdpi.com/journal/geomatics)
[![Status: Accepted](https://img.shields.io/badge/Status-Accepted%20(Oct%202026)-success)](https://www.mdpi.com/journal/geomatics)
[![License: CC BY 4.0 & MIT](https://img.shields.io/badge/License-CC%20BY%204.0%20%7C%20MIT-green.svg)](LICENSE)
[![Python: 3.10 | 3.12](https://img.shields.io/badge/Python-3.10%20%7C%203.12-informational)](requirements.txt)

This repository provides open code, geodatabases, and supplementary materials supporting the peer-reviewed research article:

> **Toward a Reproducible GIS Quality Assurance Framework: Quantifying Error Mechanisms Across the Spatial Workflow Through Ten Illustrative Cases**  
> **Authors:** Zeinab Abu Romman and Auws Weshah  
> **Affiliation:** Canada Chinook for Trading and Construction, Calgary, AB, Canada  
> **Journal:** *Geomatics* (MDPI), 2026  
> **Status:** Accepted (12 October 2026) | **Manuscript ID:** `geomatics-4550629`  
> **Academic Editor:** Enrico Corrado Borgogno Mondino  
> **Corresponding Author:** Zeinab Abu Romman ([abu.romman.z@canadachinook.ca](mailto:abu.romman.z@canadachinook.ca))  

> [!NOTE]
> **Open Access & Publication Status:**  
> This paper is accepted for publication in *Geomatics* (MDPI). This public repository serves as the official open-access code and data archive required prior to publication. The final published Version of Record (PDF) and permanent DOI will be linked here immediately upon final production release by the publisher.

---

## Overview

Geographic Information Systems (GIS) increasingly guide high-stakes decisions across public health, environmental management, urban planning, and regulatory governance. However, spatial data workflows frequently suffer from unquantified, silent errors that compound across processing stages.

This repository operationalizes the five-pillar standard-of-care framework proposed in the article, providing benchmark datasets and reproducible analytical scripts across ten illustrative case studies:

| Case # | Workflow Stage | Error Type Examined | Key Dataset / Study Area | Associated Repository Asset |
| :---: | :--- | :--- | :--- | :--- |
| **Case 1** | I: Data Acquisition | Raster resampling artifacts | Aquifer Vulnerability Index (AVI), Calgary region | `geodatabases/AVI.gdb.zip` |
| **Case 2** | I: Data Acquisition | Temporal misalignment | NRN vs. City of Calgary road networks | Open data links in Section 2.2 |
| **Case 3** | II: CRS & Projection | Area distortion from CRS misspecification | Glenmore Reservoir, Calgary, AB (+20.6% error in Web Mercator) | `geodatabases/Gelnmore_Misalignment_Study.gdb.zip` |
| **Case 4** | II: CRS & Projection | Datum / projection transformation errors | Glenmore Reservoir, Calgary, AB | `geodatabases/Gelnmore_Misalignment_Study.gdb.zip` |
| **Case 5** | II: CRS & Projection | Datum-induced spurious topology violations | City of Calgary municipal road network | `geodatabases/Gelnmore_Misalignment_Study.gdb.zip` |
| **Case 6** | III: Analysis | Spatial interpolation method sensitivity | Calgary total precipitation (47 rain gauges) | `geodatabases/Rainfall_Class.gdb.zip` |
| **Case 7** | III: Analysis | Classification scheme sensitivity | Amman-Zarqa Basin (AZB) annual production, Jordan | `geodatabases/Classification.gdb.zip` |
| **Case 8** | III: Analysis | Positional misalignment in multi-source integration | NRN + municipal road overlay | Open data links in Section 2.2 |
| **Case 9** | III: Analysis | Global sensitivity analysis of parameter weights | DRASTIC model parameter weighting | `code/script_s1_sobol_sensitivity.py` |
| **Case 10** | IV: Output | Pairwise error interdependency matrix | 50 analytical cases (1982–2024) | `supplementary/Supplementary_Material.pdf` (Table S1) |

---

## Repository Structure

```
Reproducible-GIS-QA-Framework/
|-- code/
|   `-- script_s1_sobol_sensitivity.py    # Script S1: Standalone Sobol global sensitivity analysis
|-- geodatabases/
|   |-- AVI.gdb.zip                       # Case 1: Aquifer Vulnerability Index layers
|   |-- Classification.gdb.zip            # Case 7: AZB Watershed production data
|   |-- Rainfall_Class.gdb.zip            # Case 6: 47 precipitation gauges & interpolation surfaces
|   `-- Gelnmore_Misalignment_Study.gdb.zip # Cases 3-5: Glenmore Reservoir CRS & projection error layers
|-- supplementary/
|   `-- Supplementary_Material.pdf        # Tables S1 & S2 (traceability matrix & Sobol indices)
|-- history/
|   `-- CHANGELOG.md                      # Release notes and version history
|-- .gitignore                            # Ignores runtime outputs and unzipped temporary folders
|-- CITATION.cff                          # Machine-readable citation metadata
|-- LICENSE                               # Dual open license (MIT for code, CC BY 4.0 for data)
|-- requirements.txt                      # Python dependencies with exact versions
`-- README.md                             # Repository documentation
```

---

## Geodatabases

Four ESRI File Geodatabases are provided in `geodatabases/` as compressed zip archives. Each archive can be extracted and opened directly in ArcGIS Pro or QGIS (using the OpenFileGDB driver).

> **Note on `.zip` format:** To ensure clean repository tracking and prevent accidental corruption of internal geodatabase tables, geodatabases are committed as `.zip` files. When working locally, extract the archives to your workspace; the repository `.gitignore` automatically prevents extracted `.gdb` folders from cluttering Git.

### 1. `AVI.gdb.zip` (60 KB)
* **Study Area:** Calgary Region, Alberta, Canada.
* **Layers:**
  * `Calgary_Boundary` — Municipal boundary polygon (CRS: NAD83 UTM Zone 11N).
  * `AquiferVulnerabilityIndex` — Raster-derived AVI classification polygons.
* **Paper Reference:** Case 1 (Figure 1: Effects of down-sampling and up-sampling).

### 2. `Classification.gdb.zip` (88 KB)
* **Study Area:** Amman-Zarqa Basin (AZB) Watershed, Jordan.
* **Layers:**
  * `Annual_Production_AZB` — Annual groundwater production ($m^3/\text{yr}$) by sub-basin.
  * `Sub_basin` — AZB watershed boundary and sub-basin polygons.
* **Data Origin:** Shared as provided by the Ministry of Water and Irrigation (MWI), Jordan.
* **Paper Reference:** Case 7 (Figure 7: Classification scheme sensitivity under skewed distributions).

### 3. `Rainfall_Class.gdb.zip` (156 KB)
* **Study Area:** Calgary Region, Alberta (47 rain gauge stations).
* **Layers:**
  * `gauges_projected`, `gauges_raw`, `gauges_avg_2025_09` — Gauge point locations and precipitation observations.
  * `pts_train`, `pts_val` — Cross-validation training and validation splits.
  * `surf_idw`, `surf_krig`, `surf_nn`, `surf_spline`, `surf_trend` — Interpolated raster surfaces.
* **Paper Reference:** Case 6 (Figure 6 & Table 3: Cross-validation of interpolation methods).

### 4. `Gelnmore_Misalignment_Study.gdb.zip` (68 KB)
* **Study Area:** Glenmore Reservoir, Calgary, AB.
* **Layers:**
  * `Glenmore_CORRECT_WM` — Correct geometry in Web Mercator (EPSG:3857).
  * `Glenmore_CORRECT_WM_to_26911` — Correct re-projection to NAD83 UTM Zone 11N (EPSG:26911).
  * `Glenmore_CORRECT_WM_to_26911_noTFM` — Re-projection without geographic transformation.
  * `Glenmore_ERR_Misdefined_NAD27_UTM11` — Error scenario: CRS misdefined as NAD27 UTM Zone 11.
  * `Glenmore_ERR_WrongZone_UTM12` — Error scenario: Incorrect UTM zone assignment (Zone 12).
  * `Glenmore_ERR_UTM11_WGS84_vs_NAD83` — Error scenario: Datum confusion between WGS84 and NAD83.
  * `Glenmore_ERR_UTM11_CSRS_vs_NAD83` — Error scenario: Datum confusion between NAD83(CSRS) and NAD83(Original).
  * `Glenmore_ERR_MetersAsDegrees_GCS84` — Error scenario: Cartesian misuse of angular coordinates (degrees as metres).
  * `Area_Summary` — Summary table of computed planar areas across all projection scenarios.
* *Provenance Note:* The archive name retains the original case study filename (`Gelnmore`); the correct geographic name is Glenmore Reservoir.
* **Paper Reference:** Cases 3, 4, and 5 (Figure 4, Figure 5, Table 2).

---

## Reproducible Python Code

### Script S1: Global Sobol Sensitivity Analysis
* **File:** [code/script_s1_sobol_sensitivity.py](code/script_s1_sobol_sensitivity.py)
* **Description:** Implements the variance-based global sensitivity analysis described in Section 2.4 and Case 9 (Figure 8, Table S2).
* **Setup:** Evaluates four input factors (*Data availability*, *Weights*, *Scale*, *Uncertainty*) sampled uniformly over $[0.05, 0.50]$ with $N = 10{,}000$ Saltelli base samples ($60{,}000$ model evaluations). A fixed seed (`SEED = 2026`) guarantees identical reproduction of published indices.
* **Self-Contained:** Contains inline plotting and bootstrapping logic; no external private dependencies required.

#### How to Run

1. Open your terminal or command prompt and clone/navigate to the repository:
   ```bash
   cd Reproducible-GIS-QA-Framework
   ```
2. Create and activate a clean virtual environment:
   ```bash
   # On macOS/Linux:
   python3 -m venv .venv
   source .venv/bin/activate

   # On Windows:
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install required libraries:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute the sensitivity analysis:
   ```bash
   python code/script_s1_sobol_sensitivity.py
   ```
   *(Optional)* To export the figure at publication quality (600 DPI):
   ```bash
   python code/script_s1_sobol_sensitivity.py --dpi 600
   ```

**Generated Outputs** (automatically written to an `outputs/` folder created at runtime):
* `table_s2_sobol_indices_computed.csv` — Computed first-order ($S_1$) and total-effect ($S_T$) indices with 95% bootstrap confidence intervals.
* `Figure_8_Sobol_Sensitivity_computed.jpg` — Publication-ready grouped bar chart reproducing Figure 8.
* `sobol_run_log.txt` — Full execution log including environment versions, variance decomposition, and verification checks.

---

## Supplementary Material

* **File:** [supplementary/Supplementary_Material.pdf](supplementary/Supplementary_Material.pdf)
* **Contents:**
  * **Table S1:** Full traceability matrix of 40 historical case studies (1982–2024) across 21 unique references used to construct the pairwise error interdependency matrix (Case 10, Figure 9, Table 4).
  * **Table S2:** Complete numerical output and 95% bootstrap confidence intervals for the Sobol sensitivity analysis.
  * **References:** Comprehensive bibliography for all cited supplementary case studies.

---

## License & Intellectual Property

To ensure maximum scientific utility while protecting author attribution, this repository is dual-licensed:

* **Code & Scripts (`code/`):** Licensed under the **[MIT License](LICENSE)**. Anyone is free to inspect, adapt, and run the code.
* **Geodatabases, Documentation, and Supplementary Material:** Licensed under the **[Creative Commons Attribution 4.0 International License (CC BY 4.0)](LICENSE)**.

Under CC BY 4.0, users are legally required to provide appropriate credit and cite the original publication.

---

## How to Cite

If you use this framework, code, or datasets in your research or teaching, please cite both the accepted article and this repository:

### Article Citation
```bibtex
@article{AbuRomman2026Geomatics,
  author    = {Abu Romman, Zeinab and Weshah, Auws},
  title     = {Toward a Reproducible {GIS} Quality Assurance Framework: Quantifying Error Mechanisms Across the Spatial Workflow Through Ten Illustrative Cases},
  journal   = {Geomatics},
  year      = {2026},
  note      = {Accepted: 12 October 2026. Manuscript ID: geomatics-4550629. DOI will be updated upon final publication.}
}
```

### Repository Citation
See [CITATION.cff](CITATION.cff) for complete citation metadata.

```bibtex
@software{AbuRomman_Reproducible_GIS_Framework_2026,
  author    = {Abu Romman, Zeinab and Weshah, Auws},
  title     = {Reproducible {GIS} Quality Assurance Framework - Code and Data},
  version   = {1.1.0},
  year      = {2026},
  url       = {https://github.com/Zeina963/Reproducible-GIS-QA-Framework}
}
```

---

## Acknowledgments and Data Sources

The authors gratefully acknowledge the open data portals that made this reproducibility benchmark possible:
* **Natural Resources Canada (NRCan):** National Road Network (NRN).
* **City of Calgary Open Data:** Municipal road networks and boundary polygons.
* **Alberta Open Data & GeoDiscover Alberta:** Provincial GIS baseline and precipitation records.
* **Ministry of Water and Irrigation (MWI), Jordan:** Annual groundwater production records for the Amman-Zarqa Basin.
* The open-source geospatial community, including the developers of Python, `SALib`, `matplotlib`, `numpy`, and `pandas`.
* The authors also thank Abdallah Aburumman for assistance in configuring the repository.
