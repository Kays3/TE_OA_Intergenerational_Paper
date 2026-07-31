# Project status

Last updated: 2026-07-31

## Current phase

**Protocol and repository setup**

The computational protocol and manuscript structure exist. Full-cohort
results have not yet been imported or scientifically reviewed in this
repository.

## Incoming-results checklist

- [ ] Record source machine, source path, pipeline commit, and completion time.
- [ ] Copy compact checksums and run-completion summaries.
- [ ] Confirm the sample manifest matches the frozen cohort.
- [ ] Confirm all expected tissue-treatment-phenotype cells are present.
- [ ] Review MultiQC and sample-level exclusions.
- [ ] Confirm reference genome, gene annotation, and TE-library checksums.
- [ ] Import compact count summaries and differential-result tables.
- [ ] Import publication-resolution figures or regenerate them from a notebook.
- [ ] Run family-line and multimapping sensitivity checks.
- [ ] Update `claims-evidence.tsv` without promoting unsupported claims.
- [ ] Select zebrafish candidates only after robustness review.

## Decisions pending

- Exact 162-library primary manifest after NCBI/ENA reconciliation
- Inclusion and interpretation of the 18 acute brain libraries
- Final family-aware statistical model
- Equivalence interval for return-toward-control classification
- Minimum effect-size threshold
- Locus-level quantification method and candidate count
- Zebrafish PI interest, available existing material, and feasible assays

## Current blockers

None for repository setup. Biological interpretation is intentionally blocked
until the complete result package and provenance arrive.

