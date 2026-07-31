# Proposed figures and tables for draft 01

This plan distinguishes material that can be built now from material that
depends on the frozen full-cohort analysis.

## Priority main figures

### Figure 1 - Study design and computational workflow

**Status:** Can be drafted now; update sample counts after manifest freeze.

**Panels**

- A: parental behavioural classification and exposure histories
- B: brain, gill, and liver primary cohort plus separate acute-brain cohort
- C: repeat discovery -> RNA-seq alignment -> TE quantification -> statistical
  modelling -> TE-host-gene localization -> candidate ranking

**Why it matters:** Makes the experimental unit, intergenerational terminology,
family structure, and secondary-analysis design immediately clear.

### Figure 2 - Species-specific repeat landscape

**Status:** Requires frozen RepeatModeler/RepeatMasker summary.

**Panels**

- genomic coverage and locus counts by TE class
- family counts and classification confidence
- genomic distribution relative to promoters, gene bodies, and intergenic space

**Avoid:** Interpreting all 743,008 annotated instances as active elements.

### Figure 3 - Audited brain-pilot TE expression

**Status:** Thesis figures provide a prototype; regenerate from frozen data.

**Panels**

- PCA with treatment, parental phenotype, family line, and batch
- effect-size heatmap for audited Pogo-, PiggyBac-, LINE-1-, TX1-, and related
  records
- sample-level expression for two or three representative TE families

**Improve over thesis:** Show effect direction, confidence, sample values, and
family lines instead of significance-count heatmaps alone.

### Figure 4 - Tissue-by-genomic-context candidate landscape

**Status:** Can be drafted from preliminary brain/liver summaries; add gill and
matched-background enrichment later.

**Current values available:**

- liver promoter overlap: 292 records, 226 genes, 190 priority genes
- brain promoter overlap: 200 records, 142 genes, 78 priority genes
- liver gene body/proximal/distal: 78/31/23 records
- brain gene body/proximal/distal: 57/34/12 records

**Recommended form:** Dot plot or proportional bar chart with separate encodings
for candidate records, unique genes, and priority genes.

### Figure 5 - Representative TE-host-gene locus maps

**Status:** Preliminary locus image exists; regenerate with full evidence.

**Candidates**

- liver: `LOC127531358` - `rnd-5_family-4732/DNA`
- brain: `sptbn5` - `rnd-5_family-4070/DNA`

**Required annotations:** Coordinates, TE class/family, gene exons, promoter
definition, strand, distance/overlap, read mappability, treatment contrast,
effect size, FDR, and per-sample TE/gene expression.

### Figure 6 - Functional synthesis

**Status:** Requires re-run enrichment with explicit backgrounds.

**Panels**

- brain neural/neurotransmitter-related categories
- liver stress/metabolic/detoxification categories
- all candidates versus robustness-filtered candidates

**Avoid:** Claiming a pathway is TE-regulated from gene proximity alone.

### Figure 7 - Robustness matrix

**Status:** Requires completed sensitivity analyses.

**Columns:** Family-aware model, mapping strategy, annotation library,
expression filter, influential-sample analysis, locus support, overlap/read-
through check, and batch/depth association.

**Why it matters:** This is the central analytical-validation figure supporting
publication without wet-lab experiments.

## Main tables

### Table 1 - Cohort composition and exclusions

Include BioProject, run accession, tissue, treatment, parental phenotype,
family, individual, batch, inclusion status, and exclusion reason.

### Table 2 - Repeat annotation summary

Include TE class, families, instances, covered bases, genome percentage,
expressed families, and curation confidence.

### Table 3 - Prespecified contrasts and models

Include tissue, contrast, experimental unit, covariates, family treatment,
tested features, effect-size threshold, FDR family, and estimability notes.

### Table 4 - Highest-confidence TE results

Include TE family/locus, tissue, contrast, log2 fold change, confidence interval,
FDR, mapping sensitivity, family-line consistency, and confidence tier.

### Table 5 - Ranked TE-host-gene associations

Include gene, TE, coordinates, genomic context, distance, orientation, both
differential-expression results, adjusted association, enrichment context,
and robustness status.

## Supplementary figures

- complete sample QC and MultiQC distributions
- PCA variants labelled by family and batch
- full contrast effect-size heatmaps
- unique-read versus multimapping comparisons
- de novo versus homology-supported annotation comparisons
- influential-sample and family-line sensitivity panels
- locus-level read and mappability views
- null and contradictory candidate examples

## Supplementary tables

- frozen accession manifest and metadata provenance
- exclusion log
- RepeatModeler/RepeatMasker curation ledger
- complete family-level and locus-level differential results
- all TE-host-gene pairs and data dictionary
- full enrichment results with tested backgrounds
- candidate-ranking rubric and score components
- software versions, commands, checksums, and workflow commits

## Figure callout checklist

Every main figure should state:

- sample size and biological unit
- tissue and exact contrast
- effect size and uncertainty
- FDR method where applicable
- family-line display or adjustment
- whether estimates are family- or locus-level
- whether reads are multimapping-aware
- whether the result is preliminary or frozen

No figure should use "activation," "regulation," "mobilization," "rescue," or
"adaptation" unless the corresponding claim has direct evidence under the
claims-evidence register.
