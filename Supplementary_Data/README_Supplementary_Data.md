# Supplementary Data README

## Associated manuscript

**Title:** *Coverage-Induced Agreement Inflation in Sparse Network Representations*

**Supplementary-data package version:** 1.1  
**Package date:** 22 September 2026

## Purpose and scope

This package contains the non-confidential machine-readable outputs supporting the APPLIES `q = 2` degree-preserving fixed-margin audit reported in Sections 6.5 and 7.6, Supplementary Table S1, and Supplementary Figs. S1–S2 of the associated manuscript, together with the additional dispersed-initialization sensitivity audit reported in Supplementary Table S2.

The files support inspection of the reported chain configuration, retained midrank Spearman statistics, tail indicators, chain diagnostics, exact margin-preservation checks, and figure source data. They do not contain the APPLIES raw affiliation records, enterprise identifiers, record-level enterprise data, credentials, enterprise-specific schemas, or the integrated preprocessing and analysis codebase.

## Package contents

| File | Description |
|---|---|
| `applies_q2_null_audit_v3_20260806.json` | Machine-readable audit record containing the frozen design, statistic definition, pooled inference, chain-level reports, convergence diagnostics, exact margin-preservation checks, software metadata, and artifact metadata. |
| `supplementary_table_null_chains_20260806.csv` | Four-row, full-precision chain summary supporting Supplementary Table S1. It records seeds, initialization, proposal counts, acceptance rates, sampled-null summaries, tail counts and frequencies, effective sample sizes, Monte Carlo standard errors, and software identifiers. |
| `applies_q2_retained_C_r_20260806.csv` | One row for each of the 4,000 retained graphs. Fields include chain and sample identifiers, proposal accounting, the exact-margin check, retained `C_r`, the tail indicator, and aggregate totals for `K`, `P_q`, `S_q`, and the auxiliary `M_q = P_q - S_q`. No entity-level vectors or randomized edge lists are included. |
| `applies_q2_null_trace_review_20260806.md` | Human-readable record of the predefined 20-checkpoint burn-in trace assessment and its diagnostic decision. |
| `Source_Data_Fig_S1.csv` | Source data for Supplementary Fig. S1. It contains the chain identifier, sample identifier, retained `C_r`, and tail indicator for all 4,000 retained graphs. |
| `Supplementary_Fig_S2_trace_source_data.csv` | Source data for Supplementary Fig. S2. It contains the burn-in checkpoints and retained-sample trajectories for all four chains, including proposal counts and cumulative accepted-switch counts. |
| `applies_q2_dispersed_start_audit_v1_20260902.json` | Machine-readable record of the additional dispersed-initialization sensitivity audit. It records the independent initialization seeds, initialization distances, formal-chain configuration, retained `rho_r` values, two-sided and upper-tail diagnostics, effective sample sizes, exact margin-preservation checks, and software/source provenance. |
| `audit_null_model_dispersed_starts_v1.py` | Audit driver used for the dispersed-initialization sensitivity analysis. It is provided for transparency and provenance; regeneration of the analysis still requires the confidential APPLIES input and the project modules on which the driver depends. |

## Frozen audit configuration

- Relation: APPLIES.
- Higher-order level: `q = 2`.
- Observed bipartite edge count: `|E| = 153`.
- Number of chains: 4.
- Initialization: all chains started from the observed APPLIES bipartite graph.
- Random seeds: `2026080501`, `2026080502`, `2026080503`, and `2026080504`.
- Burn-in: `100|E| = 15,300` proposal attempts per chain.
- Sampling interval: one retained graph every `|E| = 153` proposal attempts.
- Retained graphs: 1,000 per chain and 4,000 in total.
- Invalid or rejected proposals: counted in proposal totals and treated as Markov-chain self-loops.
- Preserved quantities: every labelled entity degree, every labelled context size, the binary incidence constraint, matrix dimensions, and the total edge count.

## Statistic and tail definition

**Notation note.** The legacy field name `C_r` in the frozen same-start machine-readable files corresponds exactly to the retained-sample Spearman statistic denoted by `rho_r` in the final manuscript and Supplementary Information. The legacy file and field names are retained to preserve the frozen audit artifacts.

For retained graph `r`, `C_r` is the midrank Spearman correlation between the first-order degree summary `K^(r)` and the provenance-counted second-order participation summary `P_2^(r)` over the fixed APPLIES-active entity population.

The observed statistic is:

`C_obs = 0.7154799251`.

The two-sided tail indicator is defined relative to the pooled sampled-null mean:

`I_r = 1{|C_r - C_bar_0| >= |C_obs - C_bar_0|}`.

The reported plus-one quantity is:

`p_MC = (1 + sum_r I_r) / (R + 1)`,

where `R = 4,000`. Because the retained graphs are autocorrelated switch-chain samples and exact finite-run uniform sampling from the complete fixed-margin state space has not been established, `p_MC` is interpreted as an approximate mean-centered two-sided MCMC tail diagnostic rather than an exact randomization-test p-value.

The frozen rerun is not described as a preregistered confirmatory test.

## Principal reported values

- Pooled sampled-null mean: `0.5709541982`.
- Pooled population standard deviation: `0.0887987450`.
- Pooled 2.5%, 50%, and 97.5% quantiles: `0.3765862222`, `0.5766076104`, and `0.7287877984`.
- Tail count: `421/4,000`.
- Uncorrected empirical tail proportion: `0.1052500000`.
- Approximate plus-one two-sided `p_MC`: `0.1054736316`.
- Split `R-hat` for `C_r`: `1.000000`.
- Minimum per-chain effective sample size for `C_r`: `525.6299`.
- Minimum per-chain effective sample size for the tail indicator: `872.0225`.
- Exact labelled-margin preservation: passed for all 4,000 retained graphs.
- Predefined 20-checkpoint burn-in trace review: passed; the `200|E|` rerun rule was not triggered.

## Dispersed-initialization sensitivity audit

As an additional initialization-sensitivity check, the four APPLIES `q = 2` fixed-margin switch chains were re-run from independently randomized fixed-margin starting realizations rather than directly from the observed APPLIES graph. Each starting realization was generated using `1000|E| = 153,000` proposal attempts under the same degree-preserving switch mechanism. The subsequent formal audit retained the same `100|E| = 15,300` burn-in, `|E| = 153` sampling interval, and 1,000 retained samples per chain used in the primary audit.

The four randomized starting realizations had edge-set symmetric differences of `218`, `216`, `244`, and `220` from the observed graph, with pairwise distances ranging from `216` to `250`. Across 4,000 retained graphs, the pooled mean `rho_r` was `0.5726841610`, with 2.5%, 50%, and 97.5% quantiles of `0.3865994709`, `0.5790241457`, and `0.7313256059`. The mean-centered two-sided tail count was `421/4,000`, giving `p_MC = 0.1054736316`; the directional upper-tail count was `168/4,000`, giving `p_+ = 0.0422394401`. Split `R-hat` for `rho_r` was `1.0003138340`, and the minimum per-chain ESS for `rho_r` was `601.2222`.

This analysis is an additional robustness check and does not replace the frozen same-start audit. Its close agreement with the primary audit reduces concern about sensitivity to the tested initialization scheme, but it does not establish exact finite-run convergence, independence of retained states, or uniform sampling over the complete fixed-margin state space.

## Diagnostic conventions

- Population standard deviations use denominator `n`.
- Effective sample sizes use an autocorrelation-adjusted initial-positive-sequence estimator.
- Chain-specific tail-frequency Monte Carlo standard errors are calculated as `sqrt[p_j(1-p_j)/ESS(I,j)]`.
- Switch-acceptance rates are descriptive and are not treated as an independent convergence criterion.
- The diagnostics support practical stability under the frozen criteria; they do not establish exact finite-run convergence or independence of retained states.

## Recorded software environment

- Program: `audit_null_model_chains_v3.py`.
- Program version: `3.0.0-20260806`.
- Python implementation: CPython.
- Python version: 3.12.10, 64-bit.
- Recorded operating system: Windows 11, 64-bit.
- Pseudo-random-number generator: Python `random.Random` using MT19937.
- Local run date: 6 August 2026, Asia/Shanghai time.

The confidential APPLIES input and the integrated APPLIES-specific analysis codebase are not included in this package. The dispersed-initialization audit driver is supplied for transparency and provenance, but it does not by itself permit regeneration of the randomized graphs without the confidential input and its project dependencies. The machine-readable files permit inspection and independent recalculation of the reported summaries from the retained statistics.

## Relationship between files and manuscript items

- Supplementary Table S1 is supported by `supplementary_table_null_chains_20260806.csv` and the aggregate records in `applies_q2_null_audit_v3_20260806.json`.
- Supplementary Fig. S1 is supported by `Source_Data_Fig_S1.csv`; the same retained `C_r` values and tail indicators also appear in `applies_q2_retained_C_r_20260806.csv`.
- Supplementary Fig. S2 is supported by `Supplementary_Fig_S2_trace_source_data.csv` and the trace assessment recorded in `applies_q2_null_trace_review_20260806.md`.
- The full retained-sample audit trail for the primary same-start audit is provided in `applies_q2_retained_C_r_20260806.csv`.
- Supplementary Table S2 is supported by `applies_q2_dispersed_start_audit_v1_20260902.json`; the associated audit driver is `audit_null_model_dispersed_starts_v1.py`.

## Reproducibility boundary

The package permits verification of the reported pooled and chain-level summaries from the retained statistics. It does not contain:

- APPLIES raw or record-level derived data;
- entity or context identifiers;
- entity-level `K^(r)`, `P_2^(r)`, or `S_2^(r)` vectors;
- retained randomized edge lists or incidence matrices;
- the confidential enterprise-specific preprocessing workflow; or
- the integrated executable APPLIES-specific analysis codebase.

Consequently, the package cannot be used to reconstruct fixed-margin reference distributions for the strict-inversion or top-`L` decision metrics, which were not retained as realization-level statistics in the frozen rerun. This limitation is also stated in the manuscript.

## Confidentiality and data availability

The APPLIES data contain commercially confidential enterprise information. Ownership and disclosure rights remain with the data-owning enterprise, which does not permit external access. The authors are not authorized to share or redistribute the raw records, record-level derived data, confidential identifiers, enterprise-specific schemas, or the integrated APPLIES-specific codebase.

This supplementary package is restricted to non-confidential retained statistics, aggregate diagnostics, and figure source data approved for disclosure. The public DBLP and MovieLens datasets used elsewhere in the manuscript are not redistributed in this package and should be obtained from their original providers as stated in the Data Availability section of the article.

## File handling

- Files are encoded as UTF-8 text.
- CSV files use a comma delimiter and include a header row.
- Boolean values are represented as `True` or `False` where applicable.
- Missing values, if any, are left empty rather than replaced by undocumented numeric codes.
- Full floating-point precision is retained in the machine-readable files; rounded values are used in the manuscript and supplementary figures for readability.

Questions about these supplementary materials should be directed to the corresponding author through the journal's correspondence channel.
