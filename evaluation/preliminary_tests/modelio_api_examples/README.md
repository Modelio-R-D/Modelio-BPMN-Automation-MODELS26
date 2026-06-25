# Modelio API examples (LLM context)

The two Jython files in this folder are sample macros that ship with
**Modelio Open Source** (Author: Modeliosoft; the file headers carry
their version history). They are *not* contributions of this paper.

## Why they are committed here

These two scripts were given to the LLMs as **context examples** during
the preliminary evaluation, alongside the per-scenario prompt. They are
the "working example scripts" the paper's §2.2 names as the variable
that flipped the zero-shot outcome:

> "Without providing any Modelio API examples, all three models failed
> completely (0% success rate). […] **By adding working example scripts
> in the LLM context, GPT succeeded in creating a BPMN model on its
> first attempt but the generated layout information was corrupted.**"
> — paper §2.2

The experiment's independent variable, in other words, is the presence
or absence of these two files in the LLM's context window:

- **Zero-shot condition** = system prompt + scenario prompt only.
- **With-examples condition** = system prompt + scenario prompt +
  `MakeSingleton.py` + `Sort.py`.

## What each file does

| File              | Lines | What it demonstrates                                                                                                                  |
|-------------------|------:|---------------------------------------------------------------------------------------------------------------------------------------|
| `MakeSingleton.py`|    93 | Macro that turns an existing class into a singleton, or creates a new singleton class inside a package. Shows `modelingSession.getModel().createX()`, the standard model-mutation transaction pattern, and stereotype application. |
| `Sort.py`         |   214 | Macro that sorts model elements inside a Classifier/Package. Shows element iteration, comparator wiring, the explorer-refresh idiom, and the `selectedElements`/`Applicable on:` macro contract. |

Together they expose enough of the Modelio Jython API surface — class
creation, attribute/operation creation, lane membership idioms,
transactions, element iteration — for an LLM to pattern-match against
when asked to generate a BPMN-creation script.

## Source

These ship with Modelio at `<Modelio install>/.modelio/<version>/macros/`
(or are installable from the Modelio macro repository). They are
distributed under the same license as Modelio itself; this folder
re-publishes them verbatim only as part of the preliminary-evaluation
artifact, with full author attribution preserved in their headers.

## Cross-reference

For the round-by-round results that show how each LLM did or did not
benefit from having these in context, see
[`../README.md`](../README.md) (full narrative).
