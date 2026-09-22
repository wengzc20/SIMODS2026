# APPLIES q=2 burn-in trace review (2026-08-06)

## Scope

This note records the manual trace review for the final four-chain run
reported in the manuscript and documented in
`applies_q2_null_audit_v3_20260806.json`. Earlier development runs were not
used as confirmatory evidence.

Each chain started from the observed APPLIES bipartite graph. The burn-in was
15,300 proposal attempts (`100|E|`, with `|E|=153`) and was inspected at 20
equally spaced checkpoints. Invalid proposals were counted and retained as
self-loops.

## Trace summary

| Chain | Seed | OLS slope per checkpoint | First-half mean | Second-half mean | Difference |
|---:|---:|---:|---:|---:|---:|
| 1 | 2026080501 | 0.005133 | 0.554491 | 0.609672 | 0.055181 |
| 2 | 2026080502 | 0.001606 | 0.608053 | 0.619295 | 0.011242 |
| 3 | 2026080503 | 0.001737 | 0.552001 | 0.553177 | 0.001176 |
| 4 | 2026080504 | -0.005197 | 0.607691 | 0.550106 | -0.057585 |

The trajectories fluctuate around the retained-sample pooled mean rather than
showing a sustained common-direction drift. Chain 1 has a positive endpoint
contrast and chain 4 has a similar-magnitude negative contrast; chains 2 and 3
have small contrasts. The complete 20-point values remain in the JSON result.

## Decision

Manual trace review: **PASS**. Together with split `R-hat=1.0000`, minimum
per-chain `C_r` ESS `=525.63`, and minimum tail-indicator ESS `=872.02`, the
predefined rule does not trigger extension of burn-in to `200|E|`. Acceptance
rates are reported descriptively and were not used as a convergence criterion.
