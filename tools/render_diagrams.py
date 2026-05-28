"""
render_diagrams.py
==================

Batch-renders every `evaluation/runs/<approach>/<llm>/scenario_<NN>/generated.py`
in Modelio via the ScriptServer (TCP :9999), then exports the resulting BPMN
diagram as a PNG next to the script as `diagram.png`.

This addresses Reviewer 2's request:
    "I could not find some artefacts needed to understand and verify the
     results, such as the generated BPMN models …"

Status: **stub** — the script structure and Modelio control flow are in
place. Two pieces still need verification on the target Modelio install:

  1. The PNG export command (Modelio's diagram export API varies by version).
     The function `export_diagram_png()` documents three candidate code paths;
     pick whichever works in your Modelio 5.x and delete the others.
  2. Which "project" to load. The script assumes a single fresh project per
     run (cleaner reproducibility) but a shared project may be faster.

Usage:
    1. Open Modelio.
    2. Start ScriptServer on port 9999 (the `modelio` Claude skill handles
       this; or open the script panel and run the ScriptServer macro).
    3. From the repository root:
            python tools/render_diagrams.py
       Add  --only config-helpers/claude_opus_4_5/scenario_07
       to render a single cell.

Notes:
    - Each generated.py must run in a fresh Modelio package; we create
      packages named  ${approach}__${llm}__scenario_${NN}.
    - On failure, `diagram_render_error.txt` is written next to the script
      and the loop continues.
"""

from __future__ import annotations

import argparse
import socket
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RUNS_DIR = REPO_ROOT / "evaluation" / "runs"
SCRIPTSERVER_HOST = "127.0.0.1"
SCRIPTSERVER_PORT = 9999


def send_to_modelio(jython_source: str, timeout: float = 120.0) -> str:
    """Send a Jython snippet to the running Modelio ScriptServer and return stdout."""
    with socket.create_connection((SCRIPTSERVER_HOST, SCRIPTSERVER_PORT), timeout=timeout) as s:
        s.sendall(jython_source.encode("utf-8"))
        s.shutdown(socket.SHUT_WR)
        chunks = []
        while True:
            chunk = s.recv(65536)
            if not chunk:
                break
            chunks.append(chunk)
        return b"".join(chunks).decode("utf-8", errors="replace")


def export_diagram_png(diagram_name: str, out_path: Path) -> str:
    r"""
    Return a Jython snippet that exports `diagram_name` to `out_path` as PNG.

    TODO (authors): three candidate APIs, pick what works for your Modelio:

      A. Modelio's `org.modelio.api.modelio.diagram.IDiagramService`:
           svc = Modelio.getInstance().getDiagramService()
           svc.exportToImage(diagram, java.io.File(out), "png", 1.0)

      B. via the diagram editor:
           editor = diagramSrv.openDiagram(diagram)
           editor.exportToImage(java.io.File(out), "png")

      C. headless screenshot via SWT — fragile, not recommended.
    """
    return (
        "from java.io import File\n"
        "from org.modelio.api.modelio import Modelio\n"
        f"out = File(r'{out_path.as_posix()}')\n"
        f"# TODO: locate diagram named {diagram_name!r} and call exportToImage\n"
        "print('TODO: PNG export not yet wired')\n"
    )


def run_one(generated_py: Path) -> None:
    diagram_dir = generated_py.parent
    png_path = diagram_dir / "diagram.png"
    error_path = diagram_dir / "diagram_render_error.txt"
    if error_path.exists():
        error_path.unlink()

    script_body = generated_py.read_text(encoding="utf-8")

    try:
        execution_output = send_to_modelio(script_body)
        (diagram_dir / "execution_output.txt").write_text(execution_output, encoding="utf-8")
        # Best-effort: derive a diagram name from the run folder.
        diagram_name = generated_py.parent.name
        export_snippet = export_diagram_png(diagram_name, png_path)
        send_to_modelio(export_snippet)
    except Exception as exc:
        error_path.write_text(f"{type(exc).__name__}: {exc}\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--only", help="Render only this relative path, e.g. config-helpers/claude_opus_4_5/scenario_07")
    args = parser.parse_args()

    if args.only:
        targets = [RUNS_DIR / args.only / "generated.py"]
    else:
        targets = sorted(RUNS_DIR.glob("*/*/scenario_*/generated.py"))

    for target in targets:
        if not target.exists():
            print(f"[SKIP] missing: {target}")
            continue
        print(f"[RUN ] {target.relative_to(RUNS_DIR)}")
        run_one(target)


if __name__ == "__main__":
    main()
