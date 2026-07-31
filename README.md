# TE ocean-acidification paper project

## Working title

**Tissue-specific transposable-element expression during developmental and
intergenerational acclimation to ocean acidification in a coral reef fish**

This independent repository is a transparent secondary analysis of public RNA-seq data from
*Acanthochromis polyacanthus*. It extends the gene-focused analysis reported
by Suresh et al. (2024) to transposable-element (TE) annotation, expression,
and association with host-gene responses.

The title and all biological claims are provisional until the full analysis
passes the decision criteria in `study-protocol.md`.

## Primary question

How do developmental and parental exposures to elevated CO2 alter TE
expression across brain, gill, and liver, and are any changes consistent with
intergenerational acclimation?

## Study scope

- **Primary cohort:** the 162 matched libraries used by Suresh et al.: brain,
  gill, and liver; control, developmental CO2, and intergenerational CO2;
  sensitive and tolerant parental behavioural phenotypes.
- **Secondary cohort:** 18 additional acute-exposure brain libraries from
  PRJNA311159, subject to metadata reconciliation.
- **No archived damselfish material:** the study will not claim molecular
  validation in the original animals.
- **Validation-independent manuscript:** the paper is scoped as a reproducible
  computational secondary analysis and does not require wet-lab validation.
- **Possible future zebrafish follow-up:** a cross-species experiment may test
  a later mechanistic hypothesis, but it is outside the evidence required for
  this manuscript and is not direct replication of the damselfish effect.

## Project files

| File | Purpose |
|---|---|
| `study-protocol.md` | Frozen questions, cohorts, models, contrasts, QC, and decision rules |
| `manuscript-outline.md` | Paper narrative and section-level writing scaffold |
| `figures-and-tables.md` | Planned main and supplementary display items |
| `zebrafish-validation-brief.md` | PI discussion brief and feasible validation tiers |
| `claims-evidence.tsv` | Claim-to-evidence register to prevent overstatement |
| `PROJECT_STATUS.md` | Current phase, incoming-results checklist, decisions, and blockers |
| `data/` | Versioned manifests, metadata dictionaries, and compact provenance |
| `results/` | Compact derived tables approved for Git |
| `figures/` | Publication figures and source-ready visual outputs |
| `notebooks/` | Reproducible analysis and result-review notebooks |
| `manuscript/` | Draft text, supplement, cover letter, and response files |
| `pi-materials/` | Candidate summaries and zebrafish PI discussion materials |

## Analysis stages

1. Reconcile every NCBI/ENA run against the source paper metadata.
2. Freeze the 162-library primary cohort and separate the acute brain cohort.
3. Complete and curate the de novo repeat annotation.
4. Run family-level TE quantification and differential analysis.
5. Run locus-level sensitivity analysis for leading candidates.
6. Integrate TE and nearby host-gene expression.
7. Select candidates without using zebrafish assay convenience as a filter.
8. Discuss feasibility with the zebrafish PI.
9. Freeze figures, supplement, code release, and manuscript.

## Reproducibility and publication boundaries

- Raw FASTQ, BAM, RepeatModeler working directories, and large intermediate
  results remain on compute storage and are not committed to Git.
- Git contains code, manifests, checksums, compact result tables, figures,
  notebooks, environment records, and manuscript files.
- “TE expression” does not imply TE mobilization.
- A nearby or correlated gene does not establish TE-mediated regulation.
- A nonsignificant intergenerational-versus-control contrast does not by
  itself demonstrate rescue.
- Zebrafish results will be labelled cross-species functional follow-up.

The executable TE discovery and RNA-seq pipeline is developed separately in
[`Kays3/TE_Ocean_Acidification`](https://github.com/Kays3/TE_Ocean_Acidification).
This repository owns the paper protocol, frozen manifests, compact results,
figures, manuscript, and validation planning. Pipeline code should be imported
by release or pinned commit rather than copied without provenance.

## Core data sources

- Suresh S. et al. *Communications Biology* 7, 1531 (2024).
  <https://doi.org/10.1038/s42003-024-07241-y>
- Brain RNA-seq: NCBI BioProject PRJNA311159.
- Gill and liver RNA-seq: NCBI BioProject PRJNA989422.
