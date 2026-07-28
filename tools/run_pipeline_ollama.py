"""
run_pipeline_ollama.py
======================
LLM evaluation pipeline for the Modelio BPMN Automation experiment.
Same as run_pipeline.py but uses a local Ollama instance instead of OpenRouter.

Reads a JSONL file where each record has an ``input`` field (natural-language
process description), calls a local Ollama model, and appends the generated
Python script together with token-usage and timing metrics to each record.

The system prompt is loaded automatically from the approach directory:
  • config-helpers → approaches/config-helpers/system_prompt.md
  • no-helper      → approaches/no-helper/system_prompt.md

Usage
-----
    # Config+Helpers approach, qwen2.5:1.5b
    python tools/run_pipeline_ollama.py --approach config-helpers --model qwen2.5:1.5b --input evaluation/dataset/PMo_input_processed.jsonl --output evaluation/results/raw_jsonl/exp_config_helper/generated_qwen.jsonl

    # No-Helper approach, tinyllama
    python tools/run_pipeline_ollama.py --approach no-helper --model tinyllama --input evaluation/dataset/PMo_input_processed.jsonl --output evaluation/results/raw_jsonl/exp_no_helper/generated_tinyllama.jsonl

    # Resume an interrupted run (skips already-written lines)
    python tools/run_pipeline_ollama.py --approach config-helpers --model qwen2.5:1.5b --input evaluation/dataset/PMo_input_processed.jsonl --output evaluation/results/raw_jsonl/exp_config_helper/generated_qwen.jsonl --resume

Environment
-----------
Ollama must be running locally. Start it with:
    ollama serve
Or it may already be running as a background service after installation.
Default host: http://localhost:11434
"""

from __future__ import annotations

import json
import os
import re
import sys
import argparse
import time
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent

SYSTEM_PROMPT_PATHS: dict[str, Path] = {
    "config-helpers": REPO_ROOT / "approaches" / "config-helpers" / "system_prompt.md",
    "no-helper":      REPO_ROOT / "approaches" / "no-helper"      / "system_prompt.md",
}

OLLAMA_URL      = "http://localhost:11434/api/chat"
DEFAULT_MODEL   = "qwen2.5:1.5b"
DEFAULT_DELAY   = 0.5     # seconds between requests (Ollama is local, less needed)
REQUEST_TIMEOUT = 300     # seconds — local models can be slow, give them time


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _model_attr(model: str) -> str:
    """
    Derive the output attribute prefix from an Ollama model identifier.

    Examples
    --------
    "qwen2.5:1.5b"  → "qwen2515b"
    "tinyllama"     → "tinyllama"
    "llama3:8b"     → "llama38b"
    """
    name = re.sub(r"[.\-_: ]", "", model)  # strip all punctuation including colon
    return name


def _extract_python(text: str) -> str:
    """Return the first ```python … ``` block, or the full text if none found."""
    blocks = re.findall(r"```python\n(.*?)```", text, re.DOTALL)
    return "\n\n".join(blocks).strip() if blocks else text.strip()


def _load_system_prompt(approach: str) -> str:
    path = SYSTEM_PROMPT_PATHS[approach]
    if not path.exists():
        raise FileNotFoundError(
            f"System prompt not found for approach '{approach}': {path}"
        )
    return path.read_text(encoding="utf-8")


def _count_existing_lines(path: Path) -> int:
    """Return the number of non-empty lines already written to *path*."""
    if not path.exists():
        return 0
    count = 0
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                count += 1
    return count


def _check_ollama_running() -> bool:
    """Return True if the Ollama server is reachable."""
    try:
        resp = requests.get("http://localhost:11434", timeout=5)
        return resp.status_code == 200
    except requests.exceptions.RequestException:
        return False


def _check_model_available(model: str) -> bool:
    """Return True if the model is pulled and listed in Ollama."""
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=10)
        resp.raise_for_status()
        models = [m["name"] for m in resp.json().get("models", [])]
        # Ollama may store "qwen2.5:1.5b" or "qwen2.5:latest" etc.
        return any(model in m or m in model for m in models)
    except requests.exceptions.RequestException:
        return False


# ---------------------------------------------------------------------------
# API call
# ---------------------------------------------------------------------------

def call_llm(
    text: str,
    system_prompt: str,
    model: str,
    verbose: bool = False,
) -> tuple[str | None, int, int, float]:
    """
    Call the local Ollama chat endpoint.

    Returns
    -------
    (response_text, input_tokens, output_tokens, elapsed_seconds)
    response_text is None on failure.
    """
    user_message = f"Create a BPMN diagram for the following process:\n\n{text}"

    if verbose:
        print("\n" + "=" * 70)
        print(f"MODEL : {model}")
        print(f"SYSTEM PROMPT [{len(system_prompt)} chars]:")
        print("-" * 70)
        print(system_prompt)
        print("-" * 70)
        print("USER MESSAGE:")
        print("-" * 70)
        print(user_message)
        print("=" * 70)

    payload = {
        "model":  model,
        "stream": False,          # get a single response, not a stream
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message},
        ],
        "options": {
            "num_predict": 8000,  # Ollama's equivalent of max_tokens
        },
    }

    try:
        t0 = time.time()
        resp = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        elapsed = time.time() - t0

        body = resp.json()

        # Ollama response shape:
        # { "message": { "role": "assistant", "content": "..." },
        #   "prompt_eval_count": 123,
        #   "eval_count": 456, ... }
        content = body["message"]["content"]
        in_tok  = body.get("prompt_eval_count", 0)
        out_tok = body.get("eval_count", 0)

        return content, in_tok, out_tok, elapsed

    except requests.exceptions.HTTPError as exc:
        print(f"  ✗ HTTP {exc.response.status_code}: {exc.response.text[:200]}")
    except requests.exceptions.Timeout:
        print(f"  ✗ Request timed out after {REQUEST_TIMEOUT}s")
    except requests.exceptions.RequestException as exc:
        print(f"  ✗ Network error: {exc}")
    except (KeyError, IndexError, ValueError) as exc:
        print(f"  ✗ Unexpected response shape: {exc}")

    return None, 0, 0, 0.0


# ---------------------------------------------------------------------------
# Main processing loop
# ---------------------------------------------------------------------------

def process(
    approach:      str,
    model:         str,
    input_path:    Path,
    output_path:   Path,
    delay:         float,
    resume:        bool,
    verbose:       bool,
    limit:         int | None = None,
) -> None:
    system_prompt = _load_system_prompt(approach)
    attr          = _model_attr(model)
    config_key    = f"{attr}_config"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Resume: count lines already written so we can skip them.
    skip = _count_existing_lines(output_path) if resume else 0
    if skip:
        print(f"Resuming — skipping first {skip} already-processed record(s).")

    print(f"\nApproach : {approach}")
    print(f"Model    : {model}")
    print(f"Attr key : {config_key}")
    print(f"Input    : {input_path}")
    print(f"Output   : {output_path}")
    if limit:
        print(f"Limit    : first {limit} record(s)")
    print("-" * 60)

    processed = skipped = errors = 0

    write_mode = "a" if (resume and skip) else "w"
    with (
        input_path.open(encoding="utf-8")              as inf,
        output_path.open(write_mode, encoding="utf-8") as outf,
    ):
        for line_no, raw in enumerate(inf, start=1):
            if not raw.strip():
                continue

            # Resume: fast-forward past already-written records.
            if line_no <= skip:
                skipped += 1
                continue

            try:
                record = json.loads(raw)
            except json.JSONDecodeError as exc:
                print(f"[{line_no}] ✗ JSON parse error: {exc}")
                errors += 1
                continue

            text = record.get("input", "")
            if not text:
                print(f"[{line_no}] ⚠  Empty 'input' field — skipping.")
                errors += 1
                continue

            if limit and processed >= limit:
                break

            print(f"[{line_no}] {text[:80]}…" if len(text) > 80 else f"[{line_no}] {text}")

            response, in_tok, out_tok, gen_time = call_llm(
                text, system_prompt, model, verbose
            )

            if response is not None:
                code = _extract_python(response)
                record[config_key]                      = code
                record[f"{config_key}_input_tokens"]    = in_tok
                record[f"{config_key}_output_tokens"]   = out_tok
                record[f"{config_key}_total_tokens"]    = in_tok + out_tok
                record[f"{config_key}_generation_time"] = round(gen_time, 2)
                print(
                    f"  ✓ {len(code)} chars | "
                    f"{in_tok}+{out_tok}={in_tok+out_tok} tokens | "
                    f"{gen_time:.1f}s"
                )
                processed += 1
            else:
                record[config_key]                      = None
                record[f"{config_key}_input_tokens"]    = 0
                record[f"{config_key}_output_tokens"]   = 0
                record[f"{config_key}_total_tokens"]    = 0
                record[f"{config_key}_generation_time"] = 0.0
                print("  ✗ Failed — null written for this record.")
                errors += 1

            outf.write(json.dumps(record, ensure_ascii=False) + "\n")
            outf.flush()

            if delay > 0:
                time.sleep(delay)

    print("\n" + "=" * 60)
    print(f"Done.  Processed: {processed}  |  Errors: {errors}  |  Skipped: {skipped}")
    print(f"Output: {output_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the BPMN LLM generation pipeline via local Ollama.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--approach", "-a",
        required=True,
        choices=list(SYSTEM_PROMPT_PATHS),
        help="Which approach system prompt to use.",
    )
    parser.add_argument(
        "--model", "-m",
        default=DEFAULT_MODEL,
        help=f"Ollama model name (default: {DEFAULT_MODEL}). Must be already pulled.",
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        metavar="JSONL",
        help="Input JSONL file (path relative to repo root or absolute).",
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        metavar="JSONL",
        help="Output JSONL file (created / appended to).",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=DEFAULT_DELAY,
        metavar="SECS",
        help=f"Delay between API calls in seconds (default: {DEFAULT_DELAY}).",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Skip records already present in the output file and append the rest.",
    )
    parser.add_argument(
        "--limit", "-n",
        type=int,
        default=None,
        metavar="N",
        help="Stop after processing N records (useful for quick tests).",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print the full system prompt and user message sent to the model.",
    )
    parser.add_argument(
        "--host",
        default="http://localhost:11434",
        metavar="URL",
        help="Ollama server URL (default: http://localhost:11434).",
    )

    args = parser.parse_args()

    # Update the global URL if a custom host was given
    global OLLAMA_URL
    OLLAMA_URL = f"{args.host.rstrip('/')}/api/chat"

    # Check Ollama is actually running before starting
    print("Checking Ollama is running...")
    if not _check_ollama_running():
        print("ERROR: Ollama is not reachable at http://localhost:11434")
        print("  Make sure Ollama is running. Try: ollama serve")
        sys.exit(1)
    print("✓ Ollama is running.")

    # Check the model is available
    print(f"Checking model '{args.model}' is available...")
    if not _check_model_available(args.model):
        print(f"ERROR: Model '{args.model}' not found in Ollama.")
        print(f"  Pull it first with: ollama pull {args.model}")
        sys.exit(1)
    print(f"✓ Model '{args.model}' is available.\n")

    # Resolve paths relative to the repo root so callers can use either style.
    input_path  = Path(args.input)
    output_path = Path(args.output)
    if not input_path.is_absolute():
        input_path = REPO_ROOT / input_path
    if not output_path.is_absolute():
        output_path = REPO_ROOT / output_path

    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        sys.exit(1)

    process(
        approach=args.approach,
        model=args.model,
        input_path=input_path,
        output_path=output_path,
        delay=args.delay,
        resume=args.resume,
        verbose=args.verbose,
        limit=args.limit,
    )


if __name__ == "__main__":
    main()