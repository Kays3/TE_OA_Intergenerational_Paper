# Computational manuscript outline

## Publication concept

This paper is designed as a complete, validation-independent secondary analysis
of public RNA-seq data. Its publishable contribution is a reproducible,
species-specific analysis of transposable-element (TE) expression and
TE-associated host-gene responses across tissues and CO2 exposure histories.

No wet-lab experiment is required for the claims defined here. Experimental
work may be proposed as a future direction, but it is not part of the evidence
base and must not appear as a missing validation step.

## Provisional title

**Tissue-specific transposable-element and host-gene responses across
developmental and intergenerational ocean-acidification exposures in a coral
reef fish**

Shorter alternative:

**Transposable-element responses to developmental and intergenerational ocean
acidification in a coral reef fish**

## Central contribution

The study will determine whether TE-derived transcription provides a distinct,
tissue-dependent layer of the response to developmental and parental elevated
CO2 exposure in *Acanthochromis polyacanthus*. It will deliver:

1. a curated species-specific repeat annotation;
2. family- and, where support permits, locus-level TE expression results;
3. tissue- and exposure-specific differential-response maps;
4. transparent integration of TE and host-gene expression; and
5. a ranked set of computationally supported regulatory candidates.

The paper will report association and prioritization, not TE mobilization,
causal regulation, adaptation, or experimentally proven mechanism.

## Candidate journal positioning

The manuscript is suitable for journals that publish rigorous computational
genomics, environmental transcriptomics, genome-resource, or secondary-data
studies. Journal selection should occur after the result freeze and should be
based on the strength of the tissue/exposure contrasts, robustness analyses,
and biological coherence—not on the availability of wet-lab validation.

## Abstract structure

### Background

Ocean-acidification responses vary among tissues and exposure histories, but
the contribution of repetitive elements is poorly resolved in non-model reef
fish.

### Methods

Describe the public multi-tissue RNA-seq cohorts, species-specific repeat
annotation, multimapping-aware TE quantification, family-aware differential
models, locus-level sensitivity analysis, and TE–host-gene integration.

### Results

Report only frozen values: cohort size, TE annotation summary, number and effect
sizes of differential TE families or loci, tissue specificity, exposure-history
patterns, robustness across quantification strategies, and the strongest
TE–gene associations.

### Conclusion

State whether TE transcription adds information beyond the published
gene-centric response. Describe leading candidates as hypotheses supported by
public-data reanalysis, without causal or mobilization language.

## Introduction

### 1. Ocean acidification and exposure history

Summarize developmental plasticity and parental or intergenerational exposure
in reef fish. End with the need to understand regulatory layers beyond
conventional gene-level differential expression.

### 2. Why TEs are relevant

Explain that TEs can be transcribed during environmental stress and can contain
regulatory sequence, while emphasizing that TE RNA is not equivalent to
transposition or functional regulation.

### 3. Analytical gap in non-model species

Explain why standard gene-centric workflows underrepresent repetitive
transcripts and why de novo repeat annotation plus multimapping-aware
quantification are necessary.

### 4. Study questions

Ask:

1. What is the TE composition of the study genome under a curated,
   species-specific annotation?
2. Is TE expression structured primarily by tissue, CO2 exposure history, or
   their interaction?
3. Which TE families or supported loci respond within brain, gill, and liver?
4. Are TE responses associated with nearby or co-expressed host-gene programs?
5. Which findings remain stable across family structure, mapping, and
   quantification sensitivity analyses?

Do not specify a required direction of effect.

## Results

Use answer-first headings and rewrite every heading after the result freeze.
Null or tissue-restricted results remain publishable when reported clearly.

### 1. Cohort reconstruction and quality control establish the analysis set

- Reconcile NCBI/ENA accessions with the source-study metadata.
- Show sample counts by tissue, exposure, parental phenotype, family line, and
  sequencing batch.
- Report exclusions and QC without hiding imbalanced cells.
- Separate the acute brain cohort from the primary developmental and
  intergenerational cohort.

### 2. A curated species-specific annotation defines the repeat landscape

- Summarize repeat classes, families, genomic coverage, copy-number
  distribution, and filtering stages.
- Compare de novo and reference-library classifications.
- Document the fraction of ambiguous or unclassified repeats.

### 3. TE-derived transcription is strongly structured by tissue

- Present global expression structure using PCA or another prespecified
  ordination.
- Quantify variance attributable to tissue, exposure, family line, and batch.
- Distinguish descriptive global structure from differential-testing results.

### 4. Developmental and intergenerational CO2 histories alter selected TE
responses

- Report prespecified within-tissue contrasts at family level.
- Show effect sizes and uncertainty, not significance counts alone.
- Classify shared, exposure-specific, opposite-direction, and null responses.
- Avoid calling a return toward control “rescue” unless the prespecified
  equivalence criterion is met.

### 5. TE responses differ among brain, gill, and liver

- Compare response magnitude and direction across tissues.
- Highlight neural, ion-regulatory, metabolic, detoxification, immune, or stress
  programs only when supported by enrichment or matched gene-level evidence.
- Report whether apparently shared TE families arise from the same or different
  supported loci.

### 6. Family structure and technical sensitivity define robust TE signals

- Refit leading models with the prespecified family-line treatment.
- Compare multimapping-aware family estimates with alternative counting or
  filtering settings.
- Report which findings survive effect-size, mapping, and model sensitivity
  checks.
- Make this robustness section central to validation-independent publication.

### 7. Locus-supported TE candidates associate with host-gene responses

- Integrate TE proximity, genomic context, expression direction, and host-gene
  differential expression.
- Present promoter-overlap, gene-body, proximal, and distal contexts separately.
- Rank candidates using frozen criteria rather than biological convenience.
- Use locus diagrams for the strongest brain and liver candidates.
- Describe all relationships as associations unless an analysis directly tests
  a narrower claim.

### 8. Acute brain exposure provides an independent temporal comparison

Include this section only if metadata reconciliation and QC support the 18-run
acute cohort. Treat it as a distinct comparison, not a replication of the
developmental or intergenerational design.

### 9. A reproducible candidate resource supports future functional studies

- Release compact ranked tables, annotated loci, figure source data, manifests,
  checksums, software environments, and workflow versions.
- Distinguish high-confidence computational candidates from exploratory ones.
- Present experimental work only as a future application of this resource.

## Discussion

### 1. Principal findings

State the two or three strongest frozen findings and explain how they extend
the source paper rather than repeat its gene-centric analysis.

### 2. Tissue specificity and exposure history

Interpret tissue-restricted and shared TE responses in relation to the study
design. Do not infer organism-wide effects from a single tissue.

### 3. TE–host-gene relationships

Discuss biological coherence while separating genomic proximity, correlated
expression, and causal regulation.

### 4. Robustness and uncertainty

Explain how family-aware models, multimapping-aware quantification, locus-level
support, negative or null contrasts, and sensitivity analyses strengthen the
computational evidence.

### 5. What the study does not establish

Explicitly state that the analysis does not demonstrate transposition,
heritable epigenetic change, adaptive fitness benefit, or TE-mediated causality.

### 6. Future work

Propose long-read transcriptomics, chromatin assays, reporter assays, or
cross-species experiments as future tests. These are opportunities created by
the study, not prerequisites for its conclusions.

## Methods

1. Study design and public datasets
2. Accession and metadata reconciliation
3. Cohort inclusion and exclusion criteria
4. Reference genome and gene annotation
5. De novo repeat discovery, classification, and curation
6. RNA-seq quality control and alignment
7. Multimapping-aware TE family quantification
8. Locus-level TE quantification and eligibility criteria
9. Gene-expression quantification
10. Statistical design, contrasts, covariates, and family-line handling
11. Multiple-testing correction and effect-size thresholds
12. Cross-tissue and exposure-pattern classification
13. TE–host-gene integration and candidate ranking
14. Functional enrichment with an explicit background universe
15. Sensitivity, robustness, and negative-control analyses
16. Software environments, workflow versions, and reproducibility
17. Data, code, and compact-result availability

## Main figures

1. Study design, cohorts, and computational workflow
2. Species-specific TE annotation landscape
3. Global tissue and exposure structure of TE expression
4. Within-tissue differential TE responses across exposure histories
5. Cross-tissue sharing and specificity
6. Robustness across models and quantification assumptions
7. Integrated TE–host-gene candidates and representative locus maps

## Main tables

1. Cohort composition and QC summary
2. Repeat-annotation summary
3. Prespecified contrasts and statistical models
4. Highest-confidence TE families or loci with sensitivity status
5. Highest-confidence TE–host-gene associations

## Supplementary material

- Complete accession and sample manifest
- Metadata reconciliation and exclusion log
- Repeat-library curation report
- Full differential-result tables
- Family-line and mapping sensitivity results
- Locus-level evidence tables
- Enrichment results with tested background sets
- Candidate-ranking rubric and complete ranked output
- Software versions, checksums, and workflow provenance

## Validation-independent publication requirements

The manuscript can be submitted without wet-lab validation when all of the
following are met:

- the public cohort and sample metadata are completely reconciled;
- the repeat library and filtering decisions are documented and versioned;
- primary contrasts and effect-size thresholds are frozen before narrative
  selection;
- family-line, batch, multimapping, and locus-support sensitivities are reported;
- leading claims have direct entries in `claims-evidence.tsv`;
- figures can be regenerated from versioned code and compact source data;
- null and contradictory findings are retained;
- candidate language remains associative and hypothesis-generating; and
- code, manifests, environment records, and eligible compact outputs are
  publicly available.

These requirements provide analytical validation. They do not substitute for
experimental evidence and must not be described as functional validation.

## Required limitation language

- This is a secondary analysis of public short-read RNA-seq.
- The small number of family lines limits separation of parental phenotype from
  genetic background.
- Library preparation may not capture all TE-derived transcripts.
- Ambiguous mapping remains a source of uncertainty despite
  multimapping-aware methods.
- TE expression is not evidence of mobilization or genomic insertion.
- Proximity and co-expression do not establish TE regulation of a host gene.
- Intergenerational exposure does not by itself establish transgenerational
  inheritance.
- A nonsignificant difference from control does not demonstrate biological
  restoration or adaptation.

## Claim language guide

Use:

- “TE-derived expression was associated with …”
- “The analysis prioritized …”
- “The candidate was robust to …”
- “The pattern is consistent with …”
- “These data generate the hypothesis that …”

Avoid:

- “The TE regulates …”
- “TE activation caused …”
- “The TE mobilized …”
- “The response is adaptive …”
- “The mechanism was validated …”
- “The effect is transgenerational …” unless the design and generation meet
  the formal definition.

## Stop/go rule before drafting the full paper

Proceed to a full manuscript when the cohort, TE annotation, primary models,
and robustness package are complete and at least one result supports a clear
answer to the primary question. A predominantly null result can still proceed
if the dataset is comprehensive, methods are rigorous, uncertainty is well
quantified, and the resource or negative finding materially advances the field.
