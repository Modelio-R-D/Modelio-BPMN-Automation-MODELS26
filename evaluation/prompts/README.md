# Prompts used in the controlled benchmark

The full text of every prompt sent to the LLMs is reproduced from authoritative
sources within this repository — there is no separate "secret" prompt file.

## System prompts

| Approach        | Location                                                                                  |
|-----------------|-------------------------------------------------------------------------------------------|
| Config+Helpers  | [`../../approaches/config-helpers/system_prompt.md`](../../approaches/config-helpers/system_prompt.md) |
| No-Helper       | [`../../approaches/no-helper/system_prompt.md`](../../approaches/no-helper/system_prompt.md)           |

These are the same files that a user downloads to configure their LLM (see
the project [`README.md`](../../README.md)). The artifact and the live tool
use the **same** prompts; there is no benchmark-only variant.

## User-prompt content

There is no separate user-prompt template: the user message sent to the
LLM for each run is the scenario's natural-language description from
[`../scenarios/scenario_NN.md`](../scenarios/), verbatim, with no
additional wrapper. The system prompt (one of the two above) carries
all role / format / output instructions. The exact text submitted for
each of the 330 runs is reconstructable from the raw JSONL's `input`
field.

## Per-scenario inputs

The 55 PMo natural-language descriptions are at
[`../scenarios/`](../scenarios/).

## Preliminary tests

The exploratory prompts that *predate* the published baseline — the
ones that motivated the move to Config+Helpers — are documented in
[`../preliminary_tests/`](../preliminary_tests/). They are a separate
evaluation track (different LLM set, different scenarios, different
purpose) and now live as a peer folder of [`runs/`](../runs/) and
[`matisse/`](../matisse/) rather than as a prompts sub-collection.
