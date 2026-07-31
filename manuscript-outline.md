# Manuscript outline

## Provisional title

Tissue-specific transposable-element expression during developmental and
intergenerational acclimation to ocean acidification in a coral reef fish

## Abstract structure

1. **Background:** OA responses are tissue- and generation-dependent, but the
   contribution of TEs is unknown.
2. **Approach:** Reanalyse public multi-tissue RNA-seq with a de novo
   species-specific TE annotation, multimapping-aware quantification, and
   family-aware statistical models.
3. **Results:** Populate only after analysis freeze.
4. **Interpretation:** State whether TE expression adds a distinct layer to
   the host-gene response; do not infer mobilization or causality.

## Introduction

### Paragraph 1: OA and intergenerational plasticity

Establish organismal and tissue-specific responses to elevated CO2 in reef
fish, ending with the unresolved regulatory mechanisms.

### Paragraph 2: Why TEs are plausible responders

Introduce stress-responsive TE transcription and TE-derived regulatory
sequence without presenting TE activation as necessarily harmful or adaptive.

### Paragraph 3: Technical gap

Explain why ordinary gene-centric RNA-seq workflows undercount repetitive
transcripts and why de novo annotation and multimapping-aware analysis are
needed in a non-model fish.

### Paragraph 4: Questions and hypotheses

State tissue, exposure-history, parental-phenotype, and TE-host-gene
association hypotheses without predicting a required direction.

## Results

1. A species-specific repeat annotation defines the TE landscape.
2. TE-derived expression is measurable and tissue structured.
3. Developmental and intergenerational CO2 exposures alter selected TE
   families.
4. TE response patterns differ among brain, gill, and liver.
5. Parental behavioural phenotype modifies selected responses, subject to
   family confounding.
6. Locus-supported candidates associate with selected host-gene programs.
7. Acute brain exposure distinguishes immediate from longer-term responses.
8. Optional zebrafish results test cross-species conservation or mechanism.

Each heading must be rewritten to match the observed results, including null
or contradictory findings.

## Discussion

1. Principal TE findings and how they extend—not reproduce—the source paper.
2. Tissue specificity and exposure-history patterns.
3. Relationship to stress, neural, metabolic, immune, and ion-regulation
   programs only where supported.
4. Family structure and what can and cannot be inferred about parental
   phenotype.
5. Annotation, multimapping, poly(A) selection, and short-read limitations.
6. Why TE RNA does not establish mobilization.
7. Meaning and limitations of any zebrafish cross-species follow-up.
8. Testable next steps.

## Methods

1. Source datasets and inclusion criteria
2. Metadata reconciliation
3. Reference genome and gene annotation
4. De novo repeat discovery and curation
5. RNA-seq QC and alignment
6. TE family quantification
7. Locus-level quantification
8. Statistical analysis
9. Response-pattern definitions
10. TE-host-gene integration
11. Zebrafish methods, if performed
12. Code and data availability

## Required limitation language

- The work is a secondary analysis of public short-read RNA-seq.
- The small number of family lines limits separation of phenotype and genetic
  background.
- RNA-seq library preparation may not capture all TE-derived transcripts.
- Ambiguous mapping remains a source of uncertainty despite multimapping-aware
  methods.
- TE expression is not evidence of transposition.
- Proximity and co-expression do not establish TE regulation of a gene.
- Zebrafish experiments test cross-species conservation, not direct
  replication in *A. polyacanthus*.

