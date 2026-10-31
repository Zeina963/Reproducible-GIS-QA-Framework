#!/usr/bin/env python3
"""
Script S1 - Sobol variance-based global sensitivity analysis
Case 9 (Section 3.3), Figure 8, Supplementary Table S2

Abu Romman, Z.; Weshah, A. Toward a Reproducible GIS Quality Assurance Framework:
Quantifying Error Mechanisms Across the Spatial Workflow Through Ten Illustrative Cases.
Geomatics 2026 (accepted).

Set-up as stated in Section 2.4 of the article:
  * four input factors: Data availability, Weights, Scale, Uncertainty
  * independent uniform distributions over [0.05, 0.50]
  * N = 10,000 base samples; first-order and total-effect indices only
    (calc_second_order=False), giving N x (D + 2) = 10,000 x 6 = 60,000 model evaluations
  * SALib 1.5.1: Sobol' sequence sampling (SALib.sample.sobol) and
    SALib.analyze.sobol (Saltelli et al. 2010 first-order estimator,
    Jansen total-effect estimator)
  * fixed random seed so that every run returns identical indices

Model
  The model is defined in composite_index_model(). The default is the linear composite
  index written in Section 2.4, Y = sum(w_i * r_i), with the four sampled factors as the
  coefficients w_i and unit ratings r_i = 1 (RATINGS below). To substitute a different
  model, replace the body of composite_index_model() and keep its signature: it receives
  an (n, 4) array of factor values and returns n scalar model outputs.

Outputs (written to outputs/ alongside this script's parent folder)
  table_s2_sobol_indices_computed.csv     S1, ST and 95% bootstrap confidence intervals
  Figure_8_Sobol_Sensitivity_computed.jpg Figure 8 drawn from the computed indices
  sobol_run_log.txt                       run settings and index values

Usage
  python code/script_s1_sobol_sensitivity.py
  python code/script_s1_sobol_sensitivity.py --dpi 600

Requirements: SALib>=1.5.1, numpy, pandas, matplotlib  (see requirements.txt)
"""

import os
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import argparse
import platform
import sys
import warnings
from importlib.metadata import version
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from SALib.analyze import sobol as sobol_analyze
from SALib.sample import sobol as sobol_sample

ROOT    = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs"
MIN_DPI = 300

# ---------------------------------------------------------------------------
# Analysis settings (Section 2.4)
# ---------------------------------------------------------------------------
PROBLEM = {
    "num_vars": 4,
    "names": ["Data availability", "Weights", "Scale", "Uncertainty"],
    "bounds": [[0.05, 0.50]] * 4,
}
N_BASE       = 10_000
SECOND_ORDER = False
SEED         = 2026
N_BOOTSTRAP  = 1000
RATINGS      = np.array([1.0, 1.0, 1.0, 1.0])   # r_i in Y = sum(w_i * r_i)

DISPLAY_NAMES = {
    "data availability": "Data Availability",
    "weights":           "Weights",
    "scale":             "Scale",
    "uncertainty":       "Uncertainty",
}
COLOUR_S1 = "#4472C4"
COLOUR_ST = "#ED7D31"


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------
def composite_index_model(X):
    """Composite index Y = sum(w_i * r_i) (Section 2.4).

    X : array of shape (n, 4) with columns in the order of PROBLEM['names'].
    Returns an array of shape (n,).
    """
    return X @ RATINGS


# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
def plot_sobol(df, output, dpi=MIN_DPI):
    """Draw the grouped S1 / ST bar chart and save to output."""
    if dpi < MIN_DPI:
        raise ValueError(f"dpi must be {MIN_DPI} or more (got {dpi}).")
    names = [DISPLAY_NAMES.get(str(p).strip().lower(), str(p)) for p in df["parameter"]]
    s1 = df["S1"].astype(float).to_numpy()
    st = df["ST"].astype(float).to_numpy()

    fig, ax = plt.subplots(figsize=(8, 5))
    x     = np.arange(len(names))
    width = 0.35
    bars1 = ax.bar(x - width / 2, s1, width, label="First-order (S1)",
                   color=COLOUR_S1, edgecolor="black", linewidth=0.5)
    bars2 = ax.bar(x + width / 2, st, width, label="Total-effect (ST)",
                   color=COLOUR_ST, edgecolor="black", linewidth=0.5)

    ax.set_ylabel("Sensitivity Index", fontsize=12)
    ax.set_xlabel("Parameter", fontsize=12)
    ax.set_title("Sobol Global Sensitivity Analysis\nDRASTIC Model Parameter Weights",
                 fontsize=13, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=10)
    ax.legend(fontsize=10, loc="upper right")
    top = max(0.60, float(np.ceil((max(s1.max(), st.max()) + 0.08) * 10) / 10))
    ax.set_ylim(0, top)
    ax.grid(axis="y", alpha=0.3, linewidth=0.5)
    for bar in list(bars1) + list(bars2):
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, h + 0.01,
                f"{h:.2f}", ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=dpi, bbox_inches="tight", facecolor="white", edgecolor="none")
    plt.close(fig)
    return output


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------
def run(dpi=MIN_DPI):
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)
        X = sobol_sample.sample(PROBLEM, N_BASE, calc_second_order=SECOND_ORDER, seed=SEED)
    expected = N_BASE * (PROBLEM["num_vars"] + 2)
    assert X.shape[0] == expected, f"expected {expected} evaluations, got {X.shape[0]}"

    Y = composite_index_model(X)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        Si = sobol_analyze.analyze(
            PROBLEM, Y,
            calc_second_order=SECOND_ORDER,
            num_resamples=N_BOOTSTRAP,
            conf_level=0.95,
            print_to_console=False,
            seed=SEED,
        )

    table = pd.DataFrame({
        "parameter":  PROBLEM["names"],
        "S1":         np.round(Si["S1"],      4),
        "S1_conf95":  np.round(Si["S1_conf"], 4),
        "ST":         np.round(Si["ST"],      4),
        "ST_conf95":  np.round(Si["ST_conf"], 4),
    })

    csv_path = OUT_DIR / "table_s2_sobol_indices_computed.csv"
    table.to_csv(csv_path, index=False)

    fig_path = plot_sobol(table, OUT_DIR / "Figure_8_Sobol_Sensitivity_computed.jpg", dpi=dpi)

    lines = [
        "Script S1 - Sobol global sensitivity analysis",
        f"Python {platform.python_version()}; "
        f"SALib {version('SALib')}; NumPy {np.__version__}; pandas {pd.__version__}",
        f"Factors: {', '.join(PROBLEM['names'])}; bounds U[0.05, 0.50]",
        f"N = {N_BASE:,}; calc_second_order = {SECOND_ORDER}; "
        f"model evaluations = {X.shape[0]:,}; seed = {SEED}",
        f"Bootstrap resamples = {N_BOOTSTRAP}; confidence level = 95%",
        "Model: Y = sum(w_i * r_i), r_i = " + ", ".join(f"{r:g}" for r in RATINGS),
        f"Output variance Var(Y) = {np.var(Y):.6f}",
        "",
        f"{'Parameter':<18}{'S1':>8}{'+/-':>8}{'ST':>8}{'+/-':>8}",
    ]
    for _, r in table.iterrows():
        lines.append(
            f"{r['parameter']:<18}{r['S1']:>8.3f}{r['S1_conf95']:>8.3f}"
            f"{r['ST']:>8.3f}{r['ST_conf95']:>8.3f}"
        )
    lines += [
        f"Sum S1 = {table['S1'].sum():.3f};  Sum ST = {table['ST'].sum():.3f}",
        "",
        f"Table  saved: {csv_path}",
        f"Figure saved: {fig_path} ({dpi} dpi)",
    ]
    log = "\n".join(lines)
    (OUT_DIR / "sobol_run_log.txt").write_text(log + "\n", encoding="utf-8")
    print(log)
    return table


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--dpi", type=int, default=MIN_DPI,
                    help="figure resolution, 300 or more (default 300)")
    args = ap.parse_args()
    run(dpi=args.dpi)


if __name__ == "__main__":
    main()
