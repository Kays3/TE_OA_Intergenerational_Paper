# Liver-versus-brain TE + DGE quantitative analysis

This directory contains the reproducible quantitative comparison requested for
the preliminary manuscript.

## Run

```bash
python3 run_analysis.py
```

The script uses the compact, versioned snapshot under `input-snapshot/` and
writes statistical tables, a narrative summary, and publication figures to
`output/`.

## Statistical design

- pooled Fisher exact tests compare the proportion of FDR-significant results;
- exact sign-flip tests compare liver/brain log rate ratios across six matched
  parental-phenotype-by-contrast strata;
- stratum-specific Fisher tests are BH-adjusted across matched comparisons;
- TE-gene results are collapsed to one summary per TE before Mann-Whitney tests
  and Cliff's delta calculations;
- raw TE-gene pair tests are retained as screening-only sensitivity results.

The compact snapshot does not contain raw sample-level count matrices, so this
analysis does not refit a joint tissue-by-treatment DESeq2 model.

## Figure outputs

Each figure is exported as PDF, SVG, and 600-dpi PNG:

- Figure 1: artistic study design with deterministic labels and workflow
- Figure 2: pooled DGE and TE significance rates
- Figure 3: matched-stratum liver-versus-brain odds ratios
- Figure 4: TE-gene association summaries collapsed by TE
- Figure 5: highest-ranked TE-gene candidates in brain and liver
- Figure S2: STAR mapping QC summary

The artistic background in Figure 1 was generated specifically for this
project. It is decorative and carries no quantitative evidence.

## Provenance

The input snapshot was copied from `Kays3/TE_Ocean_Acidification` remote-main
commit `8d2a294` on 31 July 2026. File checksums are generated on every run.
