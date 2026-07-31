# Computational study protocol

Version: 0.1  
Status: prospective analysis plan; freeze before full-cohort differential testing

## 1. Objectives

### Primary objective

Identify TE families whose expression changes under developmental or
intergenerational elevated-CO2 exposure within brain, gill, or liver.

### Secondary objectives

1. Test whether TE responses differ between sensitive and tolerant parental
   behavioural phenotypes.
2. Classify supported responses as persistent CO2, developmental-specific,
   intergenerational-specific, or return-toward-control patterns.
3. Determine whether leading TE signals are consistent across family lines.
4. Identify locus-supported TE signals and test their association with nearby
   host-gene expression.
5. Determine whether acute brain exposure produces a distinct TE response.

## 2. Cohorts

### Primary cohort

Use the 162 libraries described in the source study:

- tissues: brain, gill, liver;
- exposure: control, developmental elevated CO2, intergenerational elevated
  CO2;
- parental phenotype: sensitive, tolerant;
- nominal replication: nine samples per tissue-by-exposure-by-phenotype cell.

The run manifest must be reconciled against the source Supplementary Table S1.
No run enters the primary analysis based only on a filename or inferred label.

### Secondary acute cohort

PRJNA311159 contains 72 experiments, whereas the matched three-treatment brain
cohort contains 54. The remaining 18 putative acute-exposure libraries will be
included only after their metadata and experimental meaning are verified.
They will not be pooled with the three-tissue primary analysis.

### Exclusions

Exclusions must use predefined technical criteria or documented metadata
errors. PCA position alone is not sufficient. Report results both with and
without any influential samples when feasible.

## 3. TE reference construction

1. Use one genome assembly and matching sequence names throughout.
2. Build a de novo repeat library with RepeatModeler2.
3. Annotate loci with RepeatMasker.
4. Curate classifications, prioritising expressed and differential families.
5. Report genome fraction and locus counts by class, superfamily, and family.
6. Label automated `Unknown` families as unclassified unless manual evidence
   supports a more specific assignment.
7. Record software versions, databases, commands, checksums, and complete logs.

The final analysis must compare the de novo annotation with an available
curated or homology-supported library where possible.

## 4. RNA-seq processing

1. Validate FASTQ checksums.
2. Assess adapters, base quality, duplication, and read length.
3. Determine library strandedness empirically and from protocol metadata.
4. Align with STAR while retaining multimapping reads required for TE
   quantification.
5. Generate MultiQC summaries including total, unique, multimapping, unmapped,
   and assigned-read fractions.
6. Count genes and TE families with TEcount in multimapping mode.
7. Retain uniquely mapped counts as a sensitivity analysis.
8. Apply a locus-level method to preregistered leading candidates.

All tissues use the same reference and annotation versions. Tissue-specific
models are fit separately.

## 5. Statistical design

### Metadata audit

Before modelling, tabulate sample counts across:

- run and BioSample;
- individual fish;
- tissue;
- family;
- parental phenotype;
- offspring exposure;
- parental exposure;
- sequencing project, instrument, and processing batch.

Family may be nested within parental phenotype. The model matrix must be tested
for estimability before fitting interaction contrasts. Phenotype effects must
not be described as independent genetic effects when family and phenotype
cannot be separated.

### Primary models

Candidate models will be compared during the design audit:

```text
count ~ family + treatment
```

within tissue and phenotype, and:

```text
count ~ family + parental_phenotype * treatment
```

within tissue when estimable.

If repeated observations, nesting, or rank deficiency make these models
inappropriate, use a documented mixed-model or pseudobulk strategy that
preserves the family-level experimental structure.

### Filtering and significance

- Define expression filtering before testing.
- Control the false-discovery rate within each prespecified contrast family.
- Primary statistical threshold: Benjamini-Hochberg FDR < 0.05.
- Report shrunken log2 fold changes and confidence intervals.
- Do not select candidates by fold change alone.
- Display individual biological samples and family identities for candidates.

## 6. Prespecified response patterns

Let C be control, D developmental exposure, and I intergenerational exposure.

### Persistent CO2 response

- D versus C and I versus C pass FDR;
- effects have the same direction;
- neither effect is trivially small under the predefined effect-size rule.

### Developmental-specific response

- D versus C passes FDR;
- D versus I supports a difference;
- I versus C is smaller than D versus C.

### Return toward control

- D versus C passes FDR;
- D versus I supports a return;
- I versus C lies within a predefined equivalence interval.

A nonsignificant I-versus-C test is insufficient evidence of equivalence.

### Intergenerational-specific response

- I versus C passes FDR;
- I versus D supports a difference;
- D versus C does not show a comparable effect.

### Phenotype-dependent response

- the parental-phenotype-by-treatment interaction passes FDR; and
- within-phenotype estimates are reported with family-level observations.

## 7. Robustness analyses

A leading TE must be evaluated for:

1. multimapping versus unique-read quantification;
2. de novo versus homology-supported annotation;
3. reasonable expression-filter alternatives;
4. inclusion versus exclusion of influential samples;
5. family-line consistency;
6. locus-level read support;
7. overlap with genes, introns, and read-through transcription;
8. association with sequencing depth, mapping rate, or batch.

Candidates failing key robustness tests remain exploratory.

## 8. TE and host-gene integration

For supported TE loci:

- identify overlapping and nearest genes;
- use prespecified 2-kb and 10-kb windows;
- quantify TE-gene expression association in matched samples;
- adjust for treatment, parental phenotype, family, and technical covariates;
- test enrichment against source-study gene sets and pathways;
- inspect read orientation and transcript structure.

Use “associated with” rather than “regulates” unless functional evidence
supports causality.

## 9. Go/no-go criteria for the primary biological paper

Proceed with an acclimation-focused manuscript only if:

- full-cohort QC is acceptable without major treatment-batch confounding;
- multiple TE signals pass FDR and a meaningful effect-size criterion;
- primary signals are not driven by one family or one sample;
- direction and approximate magnitude survive key quantification choices;
- at least some signals have locus-level support excluding obvious read-through;
- TE results provide information not reducible to the original gene analysis.

Otherwise reframe as a TE annotation/resource or negative-results study.

## 10. Terminology

Use “intergenerational” for the source experiment unless exposure history
supports a strict transgenerational definition. Preserve legacy treatment
labels in machine-readable manifests only when required for compatibility.
