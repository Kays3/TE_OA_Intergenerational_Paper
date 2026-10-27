# Source and claim notes for draft 01

## Source roles

### PhD thesis

Source: Kaisar Dauyey, *Deciphering Intelligence in Ancient Humans and
Adaptation in Coral Reef Fish*, SOKENDAI, 2024.

Used for:

- the 72-sample brain-pilot design
- control, acute, developmental, and intergenerational exposure descriptions
- the earlier STAR/HTSeq/DESeq2 workflow
- reported TE-related families and qualitative exposure patterns
- preliminary DEG and TE-related differential-expression counts
- prior neural/GABA functional context

The draft paraphrases the thesis rather than copying prose. All legacy numbers
must be checked against the original result tables because the thesis contains
counts at several non-equivalent levels: contrast-specific calls, transcript
calls, and deduplicated TE families.

### Preliminary 31 July 2026 localization output

Used for:

- 29,923 annotated genes
- 743,008 strict TE instances
- 202,483 gene differential-expression rows
- 5,184 rows at absolute log2 fold change >= 0.5
- 727 candidate gene-contrast records
- tissue-by-context summary for brain and liver
- preliminary `LOC127531358` and `sptbn5` locus-map examples

These values are preliminary and must be linked to a pipeline commit, output
checksum, schema, and frozen result import before submission.

## Claims allowed in this draft

- TE-related expression differs among selected exposure contrasts in the brain
  pilot.
- The localization workflow identifies TE-associated differentially expressed
  gene candidates.
- Promoter overlap is the largest raw candidate context in the preliminary
  brain and liver output.
- Specific TE-gene pairs can be prioritized for future investigation.
- Analytical robustness can support an associative computational paper without
  wet-lab validation.

## Claims not allowed

- a TE regulates a named host gene
- elevated CO2 causes TE mobilization
- any candidate is functionally validated
- promoter overlap is enriched until a matched-background test is complete
- similarity to control demonstrates rescue or adaptation
- parental phenotype is a general genetic effect independent of family
- the design proves strict transgenerational inheritance
- the preliminary brain/liver module represents gill without a gill result

## Numerical audit items

1. Reconcile the thesis statements reporting nine TE families, 17 tolerant-
   parent TE-related calls, eight sensitive-parent calls, and 12 significant
   TE-related transcripts. Determine whether these are unique transcripts,
   contrast-level calls, or deduplicated families.
2. Restore exact labels for the thesis DEG counts 6,501, 928, 3,829, 2,320,
   5,363, and 1,913.
3. Confirm whether the 202,483 records are gene-by-contrast rows and whether
   727 is the count after all localization and priority filters.
4. Confirm unique-gene versus record counts in every context.
5. Explain why the preliminary localization summary currently reports brain
   and liver but not gill.
6. Verify gene symbols, coordinates, strands, and functional annotations for
   `LOC127531358` and `sptbn5`.
7. Record pipeline commit, source directory, creation time, and checksums for
   every imported result.

## Privacy status

GitHub repository `Kays3/TE_OA_Intergenerational_Paper` was verified as
**PRIVATE** on 31 July 2026 before this draft was added.
