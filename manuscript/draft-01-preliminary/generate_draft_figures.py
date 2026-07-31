#!/usr/bin/env python3
"""Generate preliminary manuscript figures from compact reviewed summaries."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "figure-source"
OUTPUT = ROOT / "figures"
OUTPUT.mkdir(exist_ok=True)

INK = "#202A35"
MUTED = "#66717E"
GRID = "#DCE2E8"
BLUE = "#2E6F9E"
BLUE_LIGHT = "#A9C8DD"
ORANGE = "#D77A32"
ORANGE_LIGHT = "#F2C39D"
GOLD = "#B78A24"
PAPER = "#FCFCFA"


def set_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.titlesize": 12,
            "axes.titleweight": "bold",
            "axes.labelcolor": INK,
            "axes.edgecolor": MUTED,
            "axes.facecolor": PAPER,
            "figure.facecolor": PAPER,
            "xtick.color": MUTED,
            "ytick.color": INK,
            "text.color": INK,
            "savefig.facecolor": PAPER,
            "savefig.bbox": "tight",
        }
    )


def save(fig: plt.Figure, stem: str) -> None:
    for suffix in ("png", "pdf", "svg"):
        fig.savefig(OUTPUT / f"{stem}.{suffix}", dpi=300)
    plt.close(fig)


def rounded_box(ax, xy, width, height, text, face, edge, fontsize=9):
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.025",
        linewidth=1.2,
        edgecolor=edge,
        facecolor=face,
    )
    ax.add_patch(patch)
    ax.text(
        xy[0] + width / 2,
        xy[1] + height / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        linespacing=1.25,
    )
    return patch


def arrow(ax, start, end):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=12,
            linewidth=1.2,
            color=MUTED,
        )
    )


def figure_1_design() -> None:
    fig, ax = plt.subplots(figsize=(11.5, 6.7))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title(
        "Study design and computational workflow",
        loc="left",
        pad=16,
    )
    ax.text(
        0,
        0.965,
        "Public A. polyacanthus RNA-seq; preliminary cohort structure and analysis plan",
        color=MUTED,
        fontsize=9,
        va="top",
    )

    rounded_box(ax, (0.02, 0.69), 0.19, 0.16, "Parental phenotype\nSensitive | Tolerant", "#EEF3F7", BLUE)
    rounded_box(ax, (0.28, 0.69), 0.20, 0.16, "Exposure history\nControl\nDevelopmental\nIntergenerational", "#F8F0E8", ORANGE)
    rounded_box(ax, (0.55, 0.69), 0.18, 0.16, "Primary cohort\nBrain | Gill | Liver\nNominal n = 162", "#EEF3F7", BLUE)
    rounded_box(ax, (0.80, 0.69), 0.17, 0.16, "Secondary cohort\nAcute brain\nPlanned n = 18", "#F8F0E8", ORANGE)
    arrow(ax, (0.21, 0.77), (0.28, 0.77))
    arrow(ax, (0.48, 0.77), (0.55, 0.77))
    arrow(ax, (0.73, 0.77), (0.80, 0.77))

    steps = [
        ("Repeat discovery\nand curation", BLUE_LIGHT, BLUE),
        ("RNA-seq QC\nand alignment", ORANGE_LIGHT, ORANGE),
        ("Multimapping-aware\nTE quantification", BLUE_LIGHT, BLUE),
        ("Family-aware\ndifferential models", ORANGE_LIGHT, ORANGE),
        ("TE-host-gene\nlocalization", BLUE_LIGHT, BLUE),
        ("Robust candidate\nresource", ORANGE_LIGHT, ORANGE),
    ]
    xs = np.linspace(0.02, 0.86, len(steps))
    step_width = 0.115
    for i, (label, face, edge) in enumerate(steps):
        rounded_box(ax, (xs[i], 0.36), step_width, 0.14, label, face, edge, fontsize=8.2)
        if i < len(steps) - 1:
            arrow(ax, (xs[i] + step_width, 0.43), (xs[i + 1], 0.43))

    rounded_box(
        ax,
        (0.12, 0.08),
        0.76,
        0.13,
        "Claim boundary: association and prioritization - not TE mobilization, causal regulation, or adaptation",
        "#F2F3F4",
        MUTED,
        fontsize=9.5,
    )
    ax.text(
        0.99,
        0.015,
        "PRELIMINARY - sample manifest and model specification pending freeze",
        ha="right",
        color=MUTED,
        fontsize=7.5,
    )
    save(fig, "figure-1-study-design-workflow")


def figure_4_context() -> None:
    data = pd.read_csv(SOURCE / "context_summary.csv")
    order = ["Promoter overlap", "Gene body", "Proximal", "Distal"]
    metrics = [
        ("candidate_records", "Candidate records"),
        ("unique_genes", "Unique genes"),
        ("priority_genes", "Priority genes"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(12.3, 5.5), sharey=True)
    y = np.arange(len(order))
    height = 0.34
    colors = {"Brain": BLUE, "Liver": ORANGE}

    for ax, (column, label) in zip(axes, metrics):
        for offset, tissue in [(-height / 2, "Brain"), (height / 2, "Liver")]:
            subset = data[data["tissue"] == tissue].set_index("context").loc[order]
            values = subset[column].to_numpy()
            bars = ax.barh(
                y + offset,
                values,
                height=height,
                color=colors[tissue],
                edgecolor=INK,
                linewidth=0.45,
                label=tissue,
            )
            ax.bar_label(bars, padding=3, fontsize=8, color=INK)
        ax.set_title(label, loc="left")
        ax.set_xlim(0, max(data[column]) * 1.22)
        ax.xaxis.grid(True, color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.tick_params(axis="y", length=0)
        ax.set_xlabel("Count")

    axes[0].set_yticks(y, order)
    axes[0].invert_yaxis()
    handles, labels = axes[-1].get_legend_handles_labels()
    fig.legend(handles[:2], labels[:2], loc="upper right", frameon=False, ncol=2)
    fig.suptitle("TE-associated candidates by tissue and genomic context", x=0.07, ha="left", fontsize=13, fontweight="bold")
    fig.text(
        0.07,
        0.93,
        "Preliminary 31 July 2026 localization output; counts are records or unique genes, not causal regulatory events",
        color=MUTED,
        fontsize=9,
    )
    fig.subplots_adjust(left=0.19, right=0.98, top=0.82, bottom=0.15, wspace=0.27)
    save(fig, "figure-4-context-summary")


def figure_3_brain_pilot() -> None:
    data = pd.read_csv(SOURCE / "brain_pilot_summary.csv")
    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    bars = ax.barh(
        data["parental_phenotype"],
        data["te_differential_expression_calls"],
        color=[BLUE, ORANGE],
        edgecolor=INK,
        linewidth=0.6,
        height=0.55,
    )
    ax.bar_label(bars, padding=5, fontsize=11, fontweight="bold")
    ax.set_xlim(0, 20)
    ax.set_xlabel("Reported TE differential-expression calls across contrasts")
    ax.set_ylabel("Parental behavioural phenotype")
    ax.xaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_title("Brain pilot: reported TE-related differential-expression calls", loc="left", pad=18)
    ax.text(
        0,
        1.03,
        "72 brain libraries; nine reported TE families; legacy thesis analysis",
        transform=ax.transAxes,
        color=MUTED,
        fontsize=9,
    )
    ax.text(
        0,
        -0.27,
        "Counts aggregate contrast-level calls and may include repeated transcripts.\n"
        "They require reconciliation before inferential use and do not establish a phenotype mechanism.",
        transform=ax.transAxes,
        color=MUTED,
        fontsize=8.5,
        linespacing=1.35,
    )
    fig.subplots_adjust(left=0.25, right=0.96, top=0.82, bottom=0.27)
    save(fig, "figure-3-brain-pilot-summary")


def figure_s1_pipeline() -> None:
    data = pd.read_csv(SOURCE / "localization_pipeline_counts.csv")
    fig, ax = plt.subplots(figsize=(8.8, 5.2))
    values = data["count"].to_numpy()
    labels = data["stage"].to_list()
    y = np.arange(len(data))
    bars = ax.barh(y, values, color=[BLUE_LIGHT, ORANGE_LIGHT, GOLD], edgecolor=INK, linewidth=0.6)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xscale("log")
    ax.set_xlabel("Gene-contrast records (log scale)")
    ax.xaxis.grid(True, color=GRID, linewidth=0.8, which="both")
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    for bar, value in zip(bars, values):
        ax.text(value * 1.08, bar.get_y() + bar.get_height() / 2, f"{value:,}", va="center", fontsize=9, fontweight="bold")
    ax.set_xlim(400, 400000)
    ax.set_title("Preliminary TE-localization filtering stages", loc="left", pad=18)
    ax.text(
        0,
        1.03,
        "Input annotation: 29,923 genes and 743,008 strict TE instances",
        transform=ax.transAxes,
        color=MUTED,
        fontsize=9,
    )
    ax.text(
        0,
        -0.20,
        "Stage counts use different filters but the same gene-contrast record grain; this is not a sample attrition diagram.",
        transform=ax.transAxes,
        color=MUTED,
        fontsize=8.5,
    )
    fig.subplots_adjust(left=0.36, right=0.94, top=0.80, bottom=0.23)
    save(fig, "figure-s1-localization-pipeline")


def main() -> None:
    set_style()
    figure_1_design()
    figure_3_brain_pilot()
    figure_4_context()
    figure_s1_pipeline()


if __name__ == "__main__":
    main()
