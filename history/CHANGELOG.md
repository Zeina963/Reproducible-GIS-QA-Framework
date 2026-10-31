# Changelog

All notable changes to this repository are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.1.0] - 2026-10-31

### Added

- Four ESRI File Geodatabases in `geodatabases/`:
  - `AVI.gdb.zip` - Aquifer Vulnerability Index study, Calgary region
  - `Classification.gdb.zip` - Annual water production classification, AZB Watershed, Jordan
  - `Rainfall_Class.gdb.zip` - Calgary-region precipitation interpolation (47 gauges)
  - `Gelnmore_Misalignment_Study.gdb.zip` - CRS misalignment error study, Glenmore Reservoir
- Supplementary material PDF (`supplementary/Supplementary_Material.pdf`) containing
  Tables S1 and S2 as submitted with the accepted manuscript.
- `history/CHANGELOG.md` (this file).

### Changed

- Repository restructured into dedicated top-level folders:
  `code/`, `geodatabases/`, `supplementary/`, `history/`.
- `code/script_s1_sobol_sensitivity.py` (Script S1) made fully self-contained:
  the `plot_sobol` function is now inlined, removing the dependency on
  `figure8_sobol_plot.py`. The script runs with no other local imports.
- `README.md` updated to reflect the new structure and to document all geodatabase
  layers, Script S1 usage, and the supplementary PDF.
- `CITATION.cff` version updated to 1.1.0.

### Removed

- `data/` CSV files and their generating scripts: `figure8_sobol_plot.py`,
  `figure9_error_heatmap.py`, and `run_all.py` are not included in this release.
  These scripts drew from pre-computed tables and are not required to reproduce
  the Sobol analysis. The published figure and table values appear in the article
  and in `supplementary/Supplementary_Material.pdf`.
- `figures/published/` folder: published figures are available in the article PDF.
- `outputs/` folder: created at runtime by `script_s1_sobol_sensitivity.py`.

---

## [1.0.0] - 2026-10-20

### Added

- Initial release: Python scripts and data files supporting the accepted article
  Abu Romman, Z.; Weshah, A. *Geomatics* 2026.
- `code/script_s1_sobol_sensitivity.py` - Sobol sensitivity analysis (Script S1).
- `code/figure8_sobol_plot.py` - Figure 8 drawing script.
- `code/figure9_error_heatmap.py` - Figure 9 error heatmap and Table 4 ranking script.
- `data/` folder with published CSV tables for Sobol indices, co-occurrence matrix,
  and Table 4 top pairs.
- `figures/published/` folder with final published figures.
- `requirements.txt`, `CITATION.cff`, `README.md`.
