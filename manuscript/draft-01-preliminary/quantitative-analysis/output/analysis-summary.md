# Liver-versus-brain TE + DGE quantitative analysis

## Executive result

At the pooled result-row level, liver had a higher FDR-significant rate than brain for both genes (3.341% vs 2.637%; odds ratio 1.28, BH-adjusted Fisher P 1.4e-20) and strict TEs (2.021% vs 1.579%; odds ratio 1.29, BH-adjusted Fisher P 0.0736). These row-level tests are highly powered but anti-conservative because the same features recur across contrasts.

Across the six matched phenotype-by-contrast strata, liver had the higher strict-TE rate in 3 strata and brain in 3. The exact paired sign-flip test gave BH-adjusted P 0.938; this matched-stratum result is the preferred tissue-level inference.

For TE-gene association screening, 15,637/109,799 liver pairs and 12,566/55,488 brain pairs had stable direction and approximate Spearman FDR < 0.05. The pooled pair-level odds ratio was 0.57 (Fisher P <2.2e-308), but this is descriptive only because candidate pairs share TEs and genes. After collapsing to one summary per TE, brain TEs had a higher median fraction of FDR-significant candidate genes (0.486 vs 0.247; BH-adjusted Mann-Whitney P 6.55e-06, Cliff's delta for liver-minus-brain -0.43) and a modestly higher maximum robust score (0.681 vs 0.622; BH-adjusted P 0.0245).

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
