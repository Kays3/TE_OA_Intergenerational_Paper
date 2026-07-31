#!/usr/bin/env python3
"""Liver-versus-brain TE + DGE analysis and Nature-style figure generation."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import math
from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Patch
from scipy.stats import fisher_exact, mannwhitneyu
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import proportion_confint


INK = "#252525"
GREY = "#6B6B6B"
LIGHT_GREY = "#D9D9D9"
BLUE = "#3B6FB6"
ORANGE = "#D97932"
TEAL = "#2A8C82"
PURPLE = "#8064A2"
PAPER = "#FFFFFF"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path(__file__).parent / "input-snapshot")
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "output")
    parser.add_argument("--asset", type=Path, default=Path(__file__).parent / "assets" / "artistic-fish-background.png")
    return parser.parse_args()


def set_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
            "font.size": 7,
            "axes.titlesize": 8,
            "axes.labelsize": 7,
            "axes.linewidth": 0.6,
            "xtick.labelsize": 6.5,
            "ytick.labelsize": 6.5,
            "xtick.major.width": 0.6,
            "ytick.major.width": 0.6,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "figure.facecolor": PAPER,
            "axes.facecolor": PAPER,
            "savefig.facecolor": PAPER,
            "savefig.bbox": "tight",
        }
    )


def save_figure(fig: plt.Figure, figure_dir: Path, stem: str) -> None:
    for suffix in ("pdf", "png", "svg"):
        fig.savefig(figure_dir / f"{stem}.{suffix}", dpi=600 if suffix == "png" else 300)
    plt.close(fig)
    svg = figure_dir / f"{stem}.svg"
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")


def safe_rate(success: float, total: float) -> float:
    return success / total if total else np.nan


def odds_ratio_ci(a: int, b: int, c: int, d: int) -> tuple[float, float, float]:
    values = np.array([a, b, c, d], dtype=float)
    if np.any(values == 0):
        values += 0.5
    aa, bb, cc, dd = values
    log_or = math.log((aa * dd) / (bb * cc))
    se = math.sqrt(1 / aa + 1 / bb + 1 / cc + 1 / dd)
    return math.exp(log_or), math.exp(log_or - 1.96 * se), math.exp(log_or + 1.96 * se)


def exact_sign_flip_p(values: np.ndarray) -> float:
    values = np.asarray(values, dtype=float)
    observed = abs(values.mean())
    permuted = []
    for signs in itertools.product((-1, 1), repeat=len(values)):
        permuted.append(abs(np.mean(values * np.asarray(signs))))
    permuted = np.asarray(permuted)
    return float(np.sum(permuted >= observed - 1e-12) / len(permuted))


def cliffs_delta(x: np.ndarray, y: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    comparisons = np.subtract.outer(x, y)
    return float((np.sum(comparisons > 0) - np.sum(comparisons < 0)) / comparisons.size)


def hash_inputs(input_dir: Path) -> pd.DataFrame:
    rows = []
    for path in sorted(input_dir.iterdir()):
        if path.is_file():
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            rows.append({"file": path.name, "bytes": path.stat().st_size, "sha256": digest})
    return pd.DataFrame(rows)


def validate_inputs(input_dir: Path) -> dict[str, pd.DataFrame]:
    required = {
        "aggregate": "aggregate_summary.csv",
        "matched": "matched_tissue_comparison.csv",
        "strata": "summary_by_stratum.csv",
        "within": "within_tissue_gene_repeat_comparison.csv",
        "qc": "star_qc_by_tissue.csv",
        "te_gene_summary": "te_gene_analysis_summary.csv",
        "brain_pairs": "brain_ranked_candidates.csv.gz",
        "liver_pairs": "liver_ranked_candidates.csv.gz",
        "brain_top": "brain_top5_candidates.csv",
        "liver_top": "liver_top5_candidates.csv",
    }
    missing = [name for name in required.values() if not (input_dir / name).exists()]
    if missing:
        raise FileNotFoundError(f"Missing required inputs: {missing}")
    tables = {key: pd.read_csv(input_dir / name) for key, name in required.items()}
    if set(tables["matched"]["tissue"].unique()) if "tissue" in tables["matched"] else set():
        raise ValueError("Matched table unexpectedly contains a tissue column")
    if set(tables["aggregate"]["tissue"]) != {"brain", "liver"}:
        raise ValueError("Expected brain and liver in aggregate summary")
    if tables["matched"].duplicated(["parental_phenotype", "contrast", "analysis_type"]).any():
        raise ValueError("Duplicate matched tissue strata")
    return tables


def pooled_tests(aggregate: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for analysis_type in ["gene", "all_repeat", "strict_TE"]:
        sub = aggregate[aggregate["analysis_type"] == analysis_type].set_index("tissue")
        for endpoint in ["significant", "strong_significant"]:
            brain_yes = int(sub.loc["brain", endpoint])
            liver_yes = int(sub.loc["liver", endpoint])
            brain_total = int(sub.loc["brain", "tested"])
            liver_total = int(sub.loc["liver", "tested"])
            table = [[liver_yes, liver_total - liver_yes], [brain_yes, brain_total - brain_yes]]
            odds, p = fisher_exact(table, alternative="two-sided")
            odds_ci, ci_low, ci_high = odds_ratio_ci(*np.asarray(table).ravel())
            rows.append(
                {
                    "analysis_type": analysis_type,
                    "endpoint": endpoint,
                    "brain_events": brain_yes,
                    "brain_tested": brain_total,
                    "brain_rate": safe_rate(brain_yes, brain_total),
                    "liver_events": liver_yes,
                    "liver_tested": liver_total,
                    "liver_rate": safe_rate(liver_yes, liver_total),
                    "liver_vs_brain_odds_ratio": odds,
                    "odds_ratio_ci_low": ci_low,
                    "odds_ratio_ci_high": ci_high,
                    "fisher_p": p,
                }
            )
    out = pd.DataFrame(rows)
    out["fisher_padj_bh"] = multipletests(out["fisher_p"], method="fdr_bh")[1]
    return out


def stratum_tests(matched: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    for _, r in matched.iterrows():
        table = [
            [int(r.liver_significant), int(r.liver_tested - r.liver_significant)],
            [int(r.brain_significant), int(r.brain_tested - r.brain_significant)],
        ]
        odds, p = fisher_exact(table)
        _, low, high = odds_ratio_ci(*np.asarray(table).ravel())
        rows.append(
            {
                "parental_phenotype": r.parental_phenotype,
                "contrast": r.contrast,
                "analysis_type": r.analysis_type,
                "brain_tested": int(r.brain_tested),
                "brain_significant": int(r.brain_significant),
                "brain_rate": r.brain_rate,
                "liver_tested": int(r.liver_tested),
                "liver_significant": int(r.liver_significant),
                "liver_rate": r.liver_rate,
                "liver_vs_brain_odds_ratio": odds,
                "odds_ratio_ci_low": low,
                "odds_ratio_ci_high": high,
                "fisher_p": max(float(p), np.finfo(float).tiny),
                "fisher_p_underflow": bool(p == 0),
            }
        )
    per_stratum = pd.DataFrame(rows)
    per_stratum["fisher_padj_bh"] = multipletests(per_stratum["fisher_p"], method="fdr_bh")[1]

    paired_rows = []
    for analysis_type, sub in per_stratum.groupby("analysis_type", sort=False):
        log2_rr = np.log2((sub["liver_significant"] + 0.5) / (sub["liver_tested"] + 1)) - np.log2(
            (sub["brain_significant"] + 0.5) / (sub["brain_tested"] + 1)
        )
        paired_rows.append(
            {
                "analysis_type": analysis_type,
                "matched_strata": len(sub),
                "median_liver_vs_brain_log2_rate_ratio": float(np.median(log2_rr)),
                "mean_liver_vs_brain_log2_rate_ratio": float(np.mean(log2_rr)),
                "liver_higher_strata": int(np.sum(log2_rr > 0)),
                "brain_higher_strata": int(np.sum(log2_rr < 0)),
                "exact_sign_flip_p": exact_sign_flip_p(log2_rr.to_numpy()),
            }
        )
    paired = pd.DataFrame(paired_rows)
    paired["exact_sign_flip_padj_bh"] = multipletests(paired["exact_sign_flip_p"], method="fdr_bh")[1]
    return per_stratum, paired


def within_tissue_tests(within: pd.DataFrame) -> pd.DataFrame:
    strict = within[within["repeat_type"] == "strict_TE"].copy()
    rows = []
    for tissue, sub in strict.groupby("tissue"):
        log2_ratio = np.log2((sub["repeat_rate"] + 1e-9) / (sub["gene_rate"] + 1e-9))
        rows.append(
            {
                "tissue": tissue,
                "matched_strata": len(sub),
                "median_strict_te_to_gene_rate_ratio": float(np.median(sub["repeat_to_gene_rate_ratio"])),
                "mean_log2_strict_te_to_gene_rate_ratio": float(np.mean(log2_ratio)),
                "strict_te_higher_strata": int(np.sum(log2_ratio > 0)),
                "gene_higher_strata": int(np.sum(log2_ratio < 0)),
                "exact_sign_flip_p": exact_sign_flip_p(log2_ratio.to_numpy()),
            }
        )
    out = pd.DataFrame(rows)
    out["exact_sign_flip_padj_bh"] = multipletests(out["exact_sign_flip_p"], method="fdr_bh")[1]
    return out


def summarize_per_te(table: pd.DataFrame) -> pd.DataFrame:
    table = table.copy()
    table["significant_pair_fdr_0_05"] = table["padj_spearman_approx"] < 0.05
    table["abs_rho_residual"] = table["rho_residual"].abs()
    grouped = table.groupby(["tissue", "te_id", "te_element", "te_family", "te_class"], dropna=False)
    return grouped.agg(
        candidate_pairs=("gene_id", "size"),
        significant_pairs=("significant_pair_fdr_0_05", "sum"),
        significant_pair_fraction=("significant_pair_fdr_0_05", "mean"),
        median_robust_score=("robust_score", "median"),
        max_robust_score=("robust_score", "max"),
        median_abs_rho_residual=("abs_rho_residual", "median"),
        max_abs_rho_residual=("abs_rho_residual", "max"),
    ).reset_index()


def te_gene_tests(tables: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    pairs = pd.concat([tables["brain_pairs"], tables["liver_pairs"]], ignore_index=True)
    per_te = summarize_per_te(pairs)
    metrics = ["significant_pair_fraction", "median_robust_score", "max_robust_score", "median_abs_rho_residual"]
    rows = []
    for metric in metrics:
        brain = per_te.loc[per_te.tissue == "brain", metric].dropna().to_numpy()
        liver = per_te.loc[per_te.tissue == "liver", metric].dropna().to_numpy()
        u, p = mannwhitneyu(liver, brain, alternative="two-sided")
        rows.append(
            {
                "metric": metric,
                "brain_tes": len(brain),
                "brain_median": float(np.median(brain)),
                "liver_tes": len(liver),
                "liver_median": float(np.median(liver)),
                "mannwhitney_u": u,
                "mannwhitney_p": p,
                "cliffs_delta_liver_minus_brain": cliffs_delta(liver, brain),
            }
        )
    tests = pd.DataFrame(rows)
    tests["mannwhitney_padj_bh"] = multipletests(tests["mannwhitney_p"], method="fdr_bh")[1]

    s = tables["te_gene_summary"].set_index("tissue")
    pair_table = [
        [int(s.loc["liver", "stable_pairs_fdr_lt_0_05"]), int(s.loc["liver", "shared_de_pairs"] - s.loc["liver", "stable_pairs_fdr_lt_0_05"])],
        [int(s.loc["brain", "stable_pairs_fdr_lt_0_05"]), int(s.loc["brain", "shared_de_pairs"] - s.loc["brain", "stable_pairs_fdr_lt_0_05"])],
    ]
    odds, p = fisher_exact(pair_table)
    _, low, high = odds_ratio_ci(*np.asarray(pair_table).ravel())
    pair_screen = pd.DataFrame(
        [
            {
                "brain_significant_pairs": pair_table[1][0],
                "brain_shared_de_pairs": int(s.loc["brain", "shared_de_pairs"]),
                "brain_rate": safe_rate(pair_table[1][0], int(s.loc["brain", "shared_de_pairs"])),
                "liver_significant_pairs": pair_table[0][0],
                "liver_shared_de_pairs": int(s.loc["liver", "shared_de_pairs"]),
                "liver_rate": safe_rate(pair_table[0][0], int(s.loc["liver", "shared_de_pairs"])),
                "liver_vs_brain_odds_ratio": odds,
                "odds_ratio_ci_low": low,
                "odds_ratio_ci_high": high,
                "fisher_p": max(float(p), np.finfo(float).tiny),
                "fisher_p_underflow": bool(p == 0),
                "interpretation": "screening-only; TE-gene pairs are non-independent",
            }
        ]
    )
    return per_te, tests, pair_screen


def figure_artistic_design(asset: Path, figure_dir: Path) -> None:
    image = mpimg.imread(asset)
    fig, ax = plt.subplots(figsize=(7.2, 4.5))
    ax.imshow(image, extent=(0, 1, 0, 1), aspect="auto")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.49, 0.57), 0.47, 0.35, boxstyle="round,pad=0.018", facecolor=(1, 1, 1, 0.88), edgecolor="none"))
    ax.text(0.515, 0.88, "Ocean-acidification RNA-seq design", fontsize=11, weight="bold", va="top")
    ax.text(0.515, 0.82, "Acanthochromis polyacanthus", fontsize=7, style="italic", color=GREY)

    labels = [
        (0.54, "Control", "414 μatm"),
        (0.68, "Developmental", "754 μatm"),
        (0.84, "Intergenerational", "754 μatm"),
    ]
    for x, title, subtitle in labels:
        ax.add_patch(Circle((x, 0.70), 0.026, facecolor=BLUE if title == "Control" else ORANGE, edgecolor=INK, lw=0.6))
        ax.text(x, 0.655, title, ha="center", fontsize=6.2, weight="bold")
        ax.text(x, 0.625, subtitle, ha="center", fontsize=5.8, color=GREY)
    for x1, x2 in [(0.57, 0.65), (0.71, 0.81)]:
        ax.add_patch(FancyArrowPatch((x1, 0.70), (x2, 0.70), arrowstyle="-|>", mutation_scale=8, lw=0.7, color=INK))
    ax.text(0.515, 0.58, "Sensitive and tolerant parental phenotypes", fontsize=6.2, color=GREY)

    tissues = [(0.56, "Brain", BLUE), (0.70, "Gill", TEAL), (0.84, "Liver", ORANGE)]
    for x, name, color in tissues:
        ax.add_patch(FancyBboxPatch((x - 0.05, 0.48), 0.10, 0.055, boxstyle="round,pad=0.006", facecolor=(1, 1, 1, 0.92), edgecolor=color, lw=1.0))
        ax.text(x, 0.507, name, ha="center", va="center", fontsize=6.4, weight="bold", color=color)
    ax.add_patch(FancyBboxPatch((0.49, 0.365), 0.19, 0.075, boxstyle="round,pad=0.007", facecolor=(1, 1, 1, 0.92), edgecolor=BLUE, lw=0.8))
    ax.text(0.585, 0.402, "Species-specific\nTE annotation", fontsize=6.3, weight="bold", ha="center", va="center")
    ax.text(0.705, 0.402, "+", fontsize=8, weight="bold", ha="center", va="center")
    ax.add_patch(FancyBboxPatch((0.73, 0.365), 0.12, 0.075, boxstyle="round,pad=0.007", facecolor=(1, 1, 1, 0.92), edgecolor=ORANGE, lw=0.8))
    ax.text(0.79, 0.402, "Gene\nDGE", fontsize=6.3, weight="bold", ha="center", va="center")
    ax.add_patch(FancyArrowPatch((0.67, 0.355), (0.67, 0.31), arrowstyle="-|>", mutation_scale=9, lw=0.8, color=INK))
    ax.add_patch(FancyBboxPatch((0.48, 0.20), 0.32, 0.10, boxstyle="round,pad=0.01", facecolor=(1, 1, 1, 0.90), edgecolor=PURPLE, lw=1.0))
    ax.text(0.64, 0.25, "TE expression +\nTE-host-gene association", ha="center", va="center", fontsize=6.7, weight="bold")
    ax.add_patch(FancyArrowPatch((0.80, 0.25), (0.835, 0.25), arrowstyle="-|>", mutation_scale=9, lw=0.8, color=INK))
    ax.add_patch(FancyBboxPatch((0.84, 0.205), 0.13, 0.09, boxstyle="round,pad=0.008", facecolor=(1, 1, 1, 0.90), edgecolor=TEAL, lw=1.0))
    ax.text(0.905, 0.25, "Ranked\ncandidates", ha="center", va="center", fontsize=6.2, weight="bold")
    ax.text(0.015, 0.018, "Artistic background generated for this study; all labels and data overlays are deterministic.", fontsize=4.8, color=GREY)
    save_figure(fig, figure_dir, "figure-1-artistic-study-design")


def figure_rates(aggregate: pd.DataFrame, figure_dir: Path) -> None:
    data = aggregate[aggregate.analysis_type.isin(["gene", "strict_TE", "all_repeat"])].copy()
    data["low"], data["high"] = zip(*data.apply(lambda r: proportion_confint(int(r.significant), int(r.tested), alpha=0.05, method="wilson"), axis=1))
    labels = {"gene": "Genes", "strict_TE": "Strict TEs", "all_repeat": "All repeats"}
    fig, ax = plt.subplots(figsize=(3.5, 2.7))
    positions = {"gene": 2, "strict_TE": 1, "all_repeat": 0}
    offsets = {"brain": -0.11, "liver": 0.11}
    colors = {"brain": BLUE, "liver": ORANGE}
    for tissue in ["brain", "liver"]:
        sub = data[data.tissue == tissue]
        for _, r in sub.iterrows():
            y = positions[r.analysis_type] + offsets[tissue]
            ax.errorbar(r.significance_rate * 100, y, xerr=[[r.significance_rate * 100 - r.low * 100], [r.high * 100 - r.significance_rate * 100]], fmt="o", color=colors[tissue], mec=INK, mew=0.4, ms=4.5, capsize=2, lw=0.8, label=tissue.capitalize() if r.analysis_type == "gene" else None)
    ax.set_yticks([0, 1, 2], [labels["all_repeat"], labels["strict_TE"], labels["gene"]])
    ax.set_xlabel("FDR-significant results among tested features (%)")
    ax.set_title("Differential-expression significance rates", loc="left", weight="bold")
    ax.grid(axis="x", color=LIGHT_GREY, lw=0.5)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.legend(frameon=False, loc="lower right")
    ax.text(0, -0.34, "Points show pooled rates; bars are 95% Wilson intervals.\nRows across contrasts are not independent biological replicates.", transform=ax.transAxes, fontsize=5.5, color=GREY)
    fig.subplots_adjust(left=0.27, right=0.97, top=0.84, bottom=0.28)
    save_figure(fig, figure_dir, "figure-2-dge-te-significance-rates")


def figure_strata(per_stratum: pd.DataFrame, figure_dir: Path) -> None:
    data = per_stratum[per_stratum.analysis_type.isin(["gene", "strict_TE"])].copy()
    data["label"] = data["parental_phenotype"].str[0].str.upper() + ": " + data["contrast"].str.replace("_vs_", " vs ").str.replace("transgenerational", "intergenerational").str.replace("developmental", "developmental")
    order = data[data.analysis_type == "gene"]["label"].tolist()[::-1]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.2), sharey=True)
    for ax, analysis_type, title in zip(axes, ["gene", "strict_TE"], ["Genes", "Strict TEs"]):
        sub = data[data.analysis_type == analysis_type].set_index("label").loc[order].reset_index()
        y = np.arange(len(sub))
        x = np.log2(sub.liver_vs_brain_odds_ratio)
        low = np.log2(sub.odds_ratio_ci_low)
        high = np.log2(sub.odds_ratio_ci_high)
        colors = [BLUE if p.startswith("S:") else ORANGE for p in sub.label]
        ax.errorbar(x, y, xerr=[x - low, high - x], fmt="none", ecolor=GREY, elinewidth=0.7, capsize=1.5)
        ax.scatter(x, y, c=colors, s=20, edgecolor=INK, linewidth=0.4, zorder=3)
        sig = sub.fisher_padj_bh < 0.05
        ax.scatter(x[sig], y[sig], facecolors="none", edgecolors=INK, s=45, linewidth=0.8, zorder=4)
        ax.axvline(0, color=INK, lw=0.7, ls="--")
        ax.set_title(title, loc="left", weight="bold")
        ax.set_xlabel("log2 odds ratio: liver / brain")
        ax.grid(axis="x", color=LIGHT_GREY, lw=0.45)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.tick_params(axis="y", length=0)
    axes[0].set_yticks(np.arange(len(order)), order)
    fig.suptitle("Matched tissue comparisons by phenotype and exposure contrast", x=0.07, ha="left", fontsize=9, weight="bold")
    fig.text(0.07, 0.015, "Open rings: BH-adjusted Fisher P < 0.05. S, sensitive parents; T, tolerant parents. Intervals are row-level 95% OR intervals.", fontsize=5.4, color=GREY)
    fig.subplots_adjust(left=0.36, right=0.98, top=0.82, bottom=0.20, wspace=0.18)
    save_figure(fig, figure_dir, "figure-3-matched-stratum-odds-ratios")


def figure_per_te(per_te: pd.DataFrame, tests: pd.DataFrame, figure_dir: Path) -> None:
    rng = np.random.default_rng(17)
    metrics = [("max_robust_score", "Maximum robust score per TE"), ("significant_pair_fraction", "FDR-significant TE-gene pairs per TE")]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.1))
    for ax, (metric, title) in zip(axes, metrics):
        groups = [per_te.loc[per_te.tissue == tissue, metric].dropna().to_numpy() for tissue in ["brain", "liver"]]
        bp = ax.boxplot(groups, positions=[0, 1], widths=0.5, patch_artist=True, showfliers=False, medianprops={"color": INK, "lw": 1.2}, boxprops={"lw": 0.7}, whiskerprops={"lw": 0.7}, capprops={"lw": 0.7})
        for patch, color in zip(bp["boxes"], [BLUE, ORANGE]):
            patch.set_facecolor(color)
            patch.set_alpha(0.35)
            patch.set_edgecolor(INK)
        for position, values, color in zip([0, 1], groups, [BLUE, ORANGE]):
            jitter = rng.normal(position, 0.055, size=len(values))
            ax.scatter(jitter, values, s=8, alpha=0.55, color=color, edgecolor="none")
        test = tests[tests.metric == metric].iloc[0]
        ax.set_title(title, loc="left", weight="bold")
        ax.set_xticks([0, 1], [f"Brain\n(n={len(groups[0])} TEs)", f"Liver\n(n={len(groups[1])} TEs)"])
        ax.text(0.02, 0.98, f"MWU BH P = {test.mannwhitney_padj_bh:.2g}\nCliff Δ = {test.cliffs_delta_liver_minus_brain:.2f}", transform=ax.transAxes, va="top", fontsize=5.8)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", color=LIGHT_GREY, lw=0.45)
    axes[1].set_ylim(-0.02, 1.02)
    fig.suptitle("TE-gene association strength collapsed to one summary per TE", x=0.07, ha="left", fontsize=9, weight="bold")
    fig.text(0.07, 0.015, "Collapsing by TE reduces, but does not eliminate, dependence among TE-gene candidate pairs.", fontsize=5.5, color=GREY)
    fig.subplots_adjust(left=0.09, right=0.98, top=0.80, bottom=0.19, wspace=0.28)
    save_figure(fig, figure_dir, "figure-4-per-te-association-summary")


def figure_top_candidates(tables: dict[str, pd.DataFrame], figure_dir: Path) -> pd.DataFrame:
    combined = pd.concat([tables["brain_pairs"].nsmallest(8, "rank"), tables["liver_pairs"].nsmallest(8, "rank")], ignore_index=True)
    combined["label"] = combined["gene_symbol"].fillna(combined["gene_id"]) + "  |  " + combined["te_family"].fillna(combined["te_element"])
    combined = combined.sort_values(["tissue", "robust_score"], ascending=[True, True]).reset_index(drop=True)
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 4.4), sharex=True)
    for ax, tissue, color in zip(axes, ["brain", "liver"], [BLUE, ORANGE]):
        sub = combined[combined.tissue == tissue].copy()
        y = np.arange(len(sub))
        sizes = np.clip(-np.log10(sub.padj_spearman_approx) * 7, 15, 80)
        ax.scatter(sub.robust_score, y, s=sizes, color=color, edgecolor=INK, linewidth=0.5)
        ax.set_yticks(y, sub.label)
        ax.set_title(tissue.capitalize(), loc="left", weight="bold")
        ax.set_xlabel("Robust score")
        ax.grid(axis="x", color=LIGHT_GREY, lw=0.45)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.tick_params(axis="y", length=0, labelsize=5.4)
    fig.suptitle("Top TE-gene candidate pairs", x=0.08, ha="left", fontsize=9, weight="bold")
    fig.text(0.08, 0.015, "Point area scales with -log10 approximate Spearman FDR. Ranking is screening-level and does not establish regulation.", fontsize=5.4, color=GREY)
    fig.subplots_adjust(left=0.25, right=0.98, top=0.84, bottom=0.14, wspace=0.48)
    save_figure(fig, figure_dir, "figure-5-top-te-gene-candidates")
    return combined


def figure_qc(qc: pd.DataFrame, figure_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(3.5, 2.6))
    x = np.arange(2)
    width = 0.32
    ax.bar(x - width / 2, qc.set_index("tissue").loc[["brain", "liver"], "mean_unique_mapping_percent"], width, label="Unique", color=[BLUE, ORANGE], edgecolor=INK, lw=0.5)
    ax.bar(x + width / 2, qc.set_index("tissue").loc[["brain", "liver"], "mean_multi_mapping_percent"], width, label="Multimapping", color=[BLUE, ORANGE], alpha=0.35, edgecolor=INK, lw=0.5, hatch="//")
    ax.set_xticks(x, ["Brain\n(n=30)", "Liver\n(n=30)"])
    ax.set_ylabel("Mean mapped reads (%)")
    ax.set_title("STAR mapping quality by tissue", loc="left", weight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=LIGHT_GREY, lw=0.45)
    legend_handles = [
        Patch(facecolor="white", edgecolor=INK, label="Unique"),
        Patch(facecolor="white", edgecolor=INK, hatch="//", label="Multimapping"),
    ]
    ax.legend(handles=legend_handles, frameon=False, fontsize=6)
    ax.text(0, -0.28, "Bars summarize tissue means; sample-level distributions were not present in the compact snapshot.", transform=ax.transAxes, fontsize=5.4, color=GREY)
    fig.subplots_adjust(left=0.19, right=0.96, top=0.82, bottom=0.27)
    save_figure(fig, figure_dir, "figure-s2-star-mapping-qc")


def write_summary(output: Path, pooled: pd.DataFrame, paired: pd.DataFrame, within: pd.DataFrame, te_tests: pd.DataFrame, pair_screen: pd.DataFrame) -> None:
    strict_pooled = pooled[(pooled.analysis_type == "strict_TE") & (pooled.endpoint == "significant")].iloc[0]
    gene_pooled = pooled[(pooled.analysis_type == "gene") & (pooled.endpoint == "significant")].iloc[0]
    strict_paired = paired[paired.analysis_type == "strict_TE"].iloc[0]
    pair = pair_screen.iloc[0]
    fraction_test = te_tests[te_tests.metric == "significant_pair_fraction"].iloc[0]
    score_test = te_tests[te_tests.metric == "max_robust_score"].iloc[0]
    pair_p_text = f"<{np.finfo(float).tiny:.2g}" if pair.fisher_p_underflow else f"{pair.fisher_p:.3g}"
    text = f"""# Liver-versus-brain TE + DGE quantitative analysis

## Executive result

At the pooled result-row level, liver had a higher FDR-significant rate than brain for both genes ({gene_pooled.liver_rate:.3%} vs {gene_pooled.brain_rate:.3%}; odds ratio {gene_pooled.liver_vs_brain_odds_ratio:.2f}, BH-adjusted Fisher P {gene_pooled.fisher_padj_bh:.3g}) and strict TEs ({strict_pooled.liver_rate:.3%} vs {strict_pooled.brain_rate:.3%}; odds ratio {strict_pooled.liver_vs_brain_odds_ratio:.2f}, BH-adjusted Fisher P {strict_pooled.fisher_padj_bh:.3g}). These row-level tests are highly powered but anti-conservative because the same features recur across contrasts.

Across the six matched phenotype-by-contrast strata, liver had the higher strict-TE rate in {int(strict_paired.liver_higher_strata)} strata and brain in {int(strict_paired.brain_higher_strata)}. The exact paired sign-flip test gave BH-adjusted P {strict_paired.exact_sign_flip_padj_bh:.3g}; this matched-stratum result is the preferred tissue-level inference.

For TE-gene association screening, {int(pair.liver_significant_pairs):,}/{int(pair.liver_shared_de_pairs):,} liver pairs and {int(pair.brain_significant_pairs):,}/{int(pair.brain_shared_de_pairs):,} brain pairs had stable direction and approximate Spearman FDR < 0.05. The pooled pair-level odds ratio was {pair.liver_vs_brain_odds_ratio:.2f} (Fisher P {pair_p_text}), but this is descriptive only because candidate pairs share TEs and genes. After collapsing to one summary per TE, brain TEs had a higher median fraction of FDR-significant candidate genes ({fraction_test.brain_median:.3f} vs {fraction_test.liver_median:.3f}; BH-adjusted Mann-Whitney P {fraction_test.mannwhitney_padj_bh:.3g}, Cliff's delta for liver-minus-brain {fraction_test.cliffs_delta_liver_minus_brain:.2f}) and a modestly higher maximum robust score ({score_test.brain_median:.3f} vs {score_test.liver_median:.3f}; BH-adjusted P {score_test.mannwhitney_padj_bh:.3g}).

## Statistical hierarchy

1. **Preferred tissue inference:** exact sign-flip tests on log rate ratios across six matched parental-phenotype-by-contrast strata.
2. **Stratum localization:** Fisher exact tests within each matched stratum, BH-adjusted across 18 tissue comparisons.
3. **Pooled sensitivity:** Fisher exact tests on all result rows; useful descriptively but not independent.
4. **TE-gene screening:** Mann-Whitney tests after collapsing candidate pairs to one summary per TE, with Cliff's delta and BH correction.

## Key limitations

- Differential-result rows are not biological replicates; features recur across contrasts.
- Only 30 brain and 30 liver libraries are represented in the compact correlation analysis.
- Liver and brain differ in sequencing depth and mapping composition.
- TE-gene correlations are screening associations, not causal regulation.
- Compact inputs do not contain raw sample-level counts, so a joint tissue-by-treatment count model cannot be refit here.
- Approximate Spearman FDR values inherit the assumptions of the upstream residual-correlation workflow.

## Source

Input snapshot copied from `Kays3/TE_Ocean_Acidification` commit `8d2a294` (remote `main`) on 31 July 2026. Checksums are recorded in `input_checksums.csv`.
"""
    (output / "analysis-summary.md").write_text(text)


def main() -> None:
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    figure_dir = args.output / "figures"
    figure_dir.mkdir(exist_ok=True)
    set_style()

    tables = validate_inputs(args.input)
    hashes = hash_inputs(args.input)
    pooled = pooled_tests(tables["aggregate"])
    per_stratum, paired = stratum_tests(tables["matched"])
    within = within_tissue_tests(tables["within"])
    per_te, te_tests, pair_screen = te_gene_tests(tables)

    hashes.to_csv(args.output / "input_checksums.csv", index=False)
    pooled.to_csv(args.output / "pooled_tissue_tests.csv", index=False)
    per_stratum.to_csv(args.output / "matched_stratum_fisher_tests.csv", index=False)
    paired.to_csv(args.output / "matched_stratum_paired_tests.csv", index=False)
    within.to_csv(args.output / "within_tissue_te_vs_gene_tests.csv", index=False)
    per_te.to_csv(args.output / "per_te_association_summary.csv", index=False)
    te_tests.to_csv(args.output / "te_gene_per_te_tests.csv", index=False)
    pair_screen.to_csv(args.output / "te_gene_pair_screening_test.csv", index=False)

    figure_artistic_design(args.asset, figure_dir)
    figure_rates(tables["aggregate"], figure_dir)
    figure_strata(per_stratum, figure_dir)
    figure_per_te(per_te, te_tests, figure_dir)
    top = figure_top_candidates(tables, figure_dir)
    top.to_csv(args.output / "top_candidates_figure_data.csv", index=False)
    figure_qc(tables["qc"], figure_dir)
    write_summary(args.output, pooled, paired, within, te_tests, pair_screen)


if __name__ == "__main__":
    main()
