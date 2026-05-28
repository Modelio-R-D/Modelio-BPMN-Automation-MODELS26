# Preliminary tests (baseline experiments that motivated Config+Helpers)

This folder documents the **preliminary experiments** mentioned in Section 2
of the paper — the work that motivated the move from direct script generation
(No-Helper) to the intermediate-representation approach (Config+Helpers).

It addresses Reviewer 2 Q4 ("Could you please provide more information about
the preliminary tests?") and point 1 of the meta-review.

> **TODO (authors):** the content below is a scaffold. Fill in from lab notes
> the prompts that were tried, the LLMs they were tried with, and the
> failure modes that justified moving to Config+Helpers.

---

## What was tried

| Attempt | Date           | Prompt file                  | LLM(s)         | Outcome                          |
|---------|----------------|------------------------------|----------------|----------------------------------|
| 1       | `<<YYYY-MM>>`  | [`attempt_01_<<name>>.md`](.) | `<<LLM>>`      | `<<one-line summary>>`           |
| 2       | `<<YYYY-MM>>`  | [`attempt_02_<<name>>.md`](.) | `<<LLM>>`      | `<<one-line summary>>`           |
| …       |                |                              |                |                                  |

## Recurring failure modes (paraphrased from lab notes)

The motivation for Config+Helpers, as reported in §2 of the paper, comes from
the following recurring problems observed in the No-Helper baseline:

- **Token blow-up.** Direct generation requires the LLM to emit ~650 lines per
  process; ~5× the size of a Config+Helpers output.
- **API drift.** LLMs hallucinated method signatures that look plausible
  but don't exist in the Modelio Jython API. *(See `attempt_<<N>>` for
  examples.)*
- **Coordinate arithmetic errors.** LLMs occasionally produced overlapping
  elements when computing pixel positions inline; the Config+Helpers
  approach pushes coordinate maths into the helper.
- **Auto-unmask race conditions.** Inline retry logic was inconsistently
  generated.

## How this connects to the published baseline

The paper's *No-Helper* condition is **not the same as these preliminary
tests**. The No-Helper condition is a refined baseline that received the
same per-scenario user-prompt template as Config+Helpers, with a stable
system prompt at
[`../system_prompt_no_helper.md`](../system_prompt_no_helper.md). The
preliminary tests documented here predate the published baseline and used
freer-form prompting.

For each preliminary attempt, this folder will eventually contain:

- `attempt_NN.md` — the prompt used and the rationale for trying it
- `outputs/attempt_NN_<llm>.py` — the LLM's response
- `outputs/attempt_NN_<llm>_failure.txt` — the failure (Modelio traceback,
  rendered-diagram screenshot, or qualitative note)
