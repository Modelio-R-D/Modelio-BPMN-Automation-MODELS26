"""
run_pipeline.py
===============
LLM evaluation pipeline for the Modelio BPMN Automation experiment.

Reads a JSONL file where each record has an ``input`` field (natural-language
process description), calls an LLM via OpenRouter, and appends the generated
Python script together with token-usage and timing metrics to each record.

The system prompt is loaded automatically from the approach directory:
  • config-helpers → approaches/config-helpers/system_prompt.md
  • no-helper      → approaches/no-helper/system_prompt.md

Output attribute names follow the convention already established in the raw
JSONL data (e.g. ``claudeopus_config``, ``gpt52_config``).

Usage
-----
    # Config+Helpers approach, GPT-5.2
    python tools/run_pipeline.py \\
        --approach config-helpers \\
        --model openai/gpt-5.2 \\
        --input  evaluation/dataset/PMo_input_processed.jsonl \\
        --output evaluation/results/raw_jsonl/exp_config_helper/generated_gpt52.jsonl

    # No-Helper approach, Claude Opus
    python tools/run_pipeline.py \\
        --approach no-helper \\
        --model anthropic/claude-opus-4-5 \\
        --input  evaluation/dataset/PMo_input_processed.jsonl \\
        --output evaluation/results/raw_jsonl/exp_no_helper/generated_claude_opus.jsonl

    # Resume an interrupted run (skips already-written lines)
    python tools/run_pipeline.py ... --resume

Environment
-----------
Set OPENROUTER_API_KEY in a ``.env`` file at the repository root or as an
environment variable before running.
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
# Optional .env support
# ---------------------------------------------------------------------------
try:
    from dotenv import load_dotenv
    _env_path = Path(__file__).resolve().parent.parent / ".env"
    if _env_path.exists():
        load_dotenv(_env_path)
except ImportError:
    print("⚠  python-dotenv not installed; reading env vars from the shell only.")
    print("   Install with: pip install python-dotenv\n")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent

SYSTEM_PROMPT_PATHS: dict[str, Path] = {
    "config-helpers": REPO_ROOT / "approaches" / "config-helpers" / "system_prompt.md",
    "no-helper":      REPO_ROOT / "approaches" / "no-helper"      / "system_prompt.md",
}

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL  = "openai/gpt-5.2"
DEFAULT_DELAY  = 1.0      # seconds between requests (rate-limit buffer)
REQUEST_TIMEOUT = 120     # seconds


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _model_attr(model: str) -> str:
    """
    Derive the output attribute prefix from an OpenRouter model identifier.

    Examples
    --------
    "anthropic/claude-opus-4-5" → "claudeopus45"
    "openai/gpt-5.2"            → "gpt52"
    "z-ai/glm-5"                → "glm5"
    """
    name = model.split("/")[-1]          # keep only the part after the slash
    name = re.sub(r"[.\-_ ]", "", name)  # strip punctuation
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


# ---------------------------------------------------------------------------
# API call
# ---------------------------------------------------------------------------

def call_llm(
    text: str,
    system_prompt: str,
    api_key: str,
    model: str,
    verbose: bool = False,
) -> tuple[str | None, int, int, float]:
    """
    Call the OpenRouter chat-completions endpoint.

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

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type":  "application/json",
    }
    payload = {
        "model":      model,
        "max_tokens": 8000,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message},
        ],
    }

    try:
        t0 = time.time()
        resp = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        elapsed = time.time() - t0

        body = resp.json()
        content = body["choices"][0]["message"]["content"]
        usage   = body.get("usage", {})
        in_tok  = usage.get("prompt_tokens",     0)
        out_tok = usage.get("completion_tokens",  0)

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
    api_key:       str,
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
                text, system_prompt, api_key, model, verbose
            )

            if response is not None:
                code = _extract_python(response)
                record[config_key]                        = code
                record[f"{config_key}_input_tokens"]      = in_tok
                record[f"{config_key}_output_tokens"]     = out_tok
                record[f"{config_key}_total_tokens"]      = in_tok + out_tok
                record[f"{config_key}_generation_time"]   = round(gen_time, 2)
                print(
                    f"  ✓ {len(code)} chars | "
                    f"{in_tok}+{out_tok}={in_tok+out_tok} tokens | "
                    f"{gen_time:.1f}s"
                )
                processed += 1
            else:
                record[config_key]                        = None
                record[f"{config_key}_input_tokens"]      = 0
                record[f"{config_key}_output_tokens"]     = 0
                record[f"{config_key}_total_tokens"]      = 0
                record[f"{config_key}_generation_time"]   = 0.0
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
        description="Run the BPMN LLM generation pipeline via OpenRouter.",
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
        help=f"OpenRouter model identifier (default: {DEFAULT_MODEL}).",
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

    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY is not set.")
        print("  Set it in .env or run: $env:OPENROUTER_API_KEY='your-key-here'")
        sys.exit(1)

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
        api_key=api_key,
        delay=args.delay,
        resume=args.resume,
        verbose=args.verbose,
        limit=args.limit,
    )


if __name__ == "__main__":
    main()
