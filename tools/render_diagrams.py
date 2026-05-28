"""
render_diagrams.py
==================

Internal automation driver used by the authors to produce the
`diagram_generated.png` files committed under `evaluation/runs/`. It depends on a
project-internal Modelio remote-execution channel and is not part of the
public reproduction path.

**Reviewers reproducing the artifact should use the Modelio macro at
`tools/macros/render_all.py` instead.** That macro runs entirely inside
a stock Modelio installation and produces the same per-run PNGs without
any external Python driver. See `tools/README.md` for both paths.

Authors' usage (from repo root):

    python tools/render_diagrams.py --check
    python tools/render_diagrams.py --only config-helpers/claude_opus_4_5/scenario_01
    python tools/render_diagrams.py --approach config-helpers --llm claude_opus_4_5
    python tools/render_diagrams.py                     # everything

The driver wraps each captured `generated.py` so that:

1.  The hardcoded `execfile("C:/Users/lchlih/.modelio/...")` line — left
    over from the original experiment author's macros folder — is
    rewritten to point at the in-repo `BPMN_Helpers.py`.
2.  The `selectedElements` global the captured macro expects is shimmed
    to return a fresh per-run sub-package under the MODELS26 UML
    package.
"""

from __future__ import annotations

import argparse
import re
import socket
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RUNS_DIR = REPO_ROOT / "evaluation" / "runs"
HELPER_PY = REPO_ROOT / "approaches" / "config-helpers" / "BPMN_Helpers.py"

SCRIPTSERVER_HOST = "127.0.0.1"
SCRIPTSERVER_PORT = 9999
END_MARKER = "---END---"
DEFAULT_TIMEOUT = 300.0  # seconds


# ---------------------------------------------------------------------------
# Modelio remote-execution client (END_MARKER framing).
# Configuration is project-internal; see authors' notes for setup.
# ---------------------------------------------------------------------------

def send_to_modelio(jython_source: str, timeout: float = DEFAULT_TIMEOUT) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        s.connect((SCRIPTSERVER_HOST, SCRIPTSERVER_PORT))
        payload = jython_source + "\n" + END_MARKER + "\n"
        s.sendall(payload.encode("utf-8"))
        buf = ""
        while True:
            chunk = s.recv(8192)
            if not chunk:
                break
            buf += chunk.decode("utf-8", errors="replace")
            if END_MARKER in buf:
                return buf.split(END_MARKER, 1)[0]
        return buf


# ---------------------------------------------------------------------------
# Wrapper assembly
# ---------------------------------------------------------------------------

EXECFILE_RE = re.compile(
    r'execfile\(\s*[\'"]([^\'"]*BPMN_Helpers\.py)[\'"]\s*\)'
)


def patch_helper_execfile(script: str) -> str:
    """Rewrite the captured execfile() path to point at the in-repo helper."""
    repo_helper = HELPER_PY.as_posix()
    return EXECFILE_RE.sub(f'execfile("{repo_helper}")', script)


def safe_pkg_name(approach: str, llm: str, scenario: str) -> str:
    raw = f"{approach}__{llm}__{scenario}"
    return re.sub(r"[^A-Za-z0-9_]", "_", raw)


WRAPPER_TEMPLATE = r'''# === render wrapper ===
from org.modelio.metamodel.uml.statik import Package
from org.modelio.metamodel.diagrams import AbstractDiagram

_factory = modelingSession.getModel()
_models26 = None
for _root in _factory.getModelRoots():
    if _root.getMClass().getName() == 'Project':
        for _child in _root.getCompositionChildren():
            if _child.getName() == 'MODELS26' and isinstance(_child, Package):
                _models26 = _child
                break

if _models26 is None:
    raise Exception("MODELS26 package not found under any Project root")

# Reuse existing sub-package if present (so re-renders are idempotent), else create.
_pkgname = "__PKG_NAME__"
_subpkg = None
for _e in _models26.getOwnedElement():
    if _e.getName() == _pkgname and isinstance(_e, Package):
        _subpkg = _e
        break
if _subpkg is None:
    _tx = modelingSession.createTransaction("RenderSetup_" + _pkgname)
    try:
        _subpkg = _factory.createPackage(_pkgname, _models26)
        _tx.commit()
    except:
        _tx.rollback()
        raise

# Diagrams already in the model before we run the captured script:
_before = set()
for _d in modelingSession.findByClass(AbstractDiagram):
    _before.add(_d)

# Shim selectedElements for the captured macro.
class _SelShim(object):
    def __init__(self, items):
        self._items = items
        self.size = len(items)
    def get(self, i):
        return self._items[i]
selectedElements = _SelShim([_subpkg])

# Wrap the captured script in a transaction (the GUI macro runner does this
# automatically; remote-execution invocations do not).
_tx_body = modelingSession.createTransaction("Render_" + _pkgname)
try:
    # --- captured generated.py begins ---
    __SCRIPT_BODY__
    # --- captured generated.py ends ---
    _tx_body.commit()
except:
    _tx_body.rollback()
    raise

# Find diagrams newly created during execution.
_new = []
for _d in modelingSession.findByClass(AbstractDiagram):
    if _d not in _before:
        _new.append(_d)

print "FOUND_DIAGRAMS:" + str(len(_new))

# Export the first BPMN-style diagram to the requested path.
_out_path = r"__OUT_PATH__"
_diagramService = Modelio.getInstance().getDiagramService()
_exported = 0
for _d in _new:
    if _exported >= 1:
        break
    try:
        _dh = _diagramService.getDiagramHandle(_d)
        _dh.saveInFile("PNG", _out_path, 10)
        _dh.close()
        print "EXPORTED:" + _d.getName() + " -> " + _out_path
        _exported = _exported + 1
    except Exception, _ex:
        print "EXPORT_ERROR:" + _d.getName() + ":" + str(_ex)

if _exported == 0:
    print "NO_DIAGRAM_PRODUCED"
print "DONE"
'''


def build_wrapper(generated_py: Path, out_png: Path, pkg_suffix: str = "") -> str:
    parts = generated_py.relative_to(RUNS_DIR).parts  # approach, llm, scenario_NN, <script>.py
    approach, llm, scenario = parts[0], parts[1], parts[2]
    pkg = safe_pkg_name(approach, llm, scenario) + pkg_suffix

    raw = generated_py.read_text(encoding="utf-8")
    patched = patch_helper_execfile(raw)
    # The captured script is inlined inside a `try:` block — indent every line
    # 4 spaces. Blank lines stay blank.
    indented = "\n".join(("    " + line) if line else line for line in patched.splitlines())

    return (
        WRAPPER_TEMPLATE
        .replace("__PKG_NAME__", pkg)
        .replace("__OUT_PATH__", out_png.as_posix())
        .replace("__SCRIPT_BODY__", indented)
    )


# ---------------------------------------------------------------------------
# Per-run execution + batch
# ---------------------------------------------------------------------------

def render_one(generated_py: Path, dry_run: bool = False,
               *, out_name: str = "diagram_generated.png",
               log_name: str = "diagram_render.log",
               err_name: str = "diagram_render_error.txt",
               pkg_suffix: str = "") -> tuple[bool, str]:
    run_dir = generated_py.parent
    out_png = run_dir / out_name
    log_path = run_dir / log_name
    err_path = run_dir / err_name
    if err_path.exists():
        err_path.unlink()

    wrapper = build_wrapper(generated_py, out_png, pkg_suffix=pkg_suffix)

    if dry_run:
        print(wrapper)
        return True, "dry-run"

    t0 = time.time()
    try:
        output = send_to_modelio(wrapper)
    except Exception as exc:
        err_path.write_text(f"{type(exc).__name__}: {exc}\n", encoding="utf-8")
        return False, f"socket-error: {exc!r}"
    elapsed = time.time() - t0

    log_path.write_text(output, encoding="utf-8")

    ok = ("EXPORTED:" in output) and out_png.exists()
    if not ok:
        err_lines = [l for l in output.splitlines() if "Error" in l or "Traceback" in l or l.startswith("ERROR")]
        err_path.write_text(
            "Full Modelio remote-execution output below.\n"
            "---\n"
            + ("\n".join(err_lines) if err_lines else "(no error line matched)")
            + "\n---\n"
            + output,
            encoding="utf-8",
        )
        return False, f"no-png ({elapsed:.1f}s)"
    return True, f"ok ({elapsed:.1f}s)"


def iter_targets(args: argparse.Namespace) -> list[Path]:
    script_name = "ground_truth.py" if args.ground_truth else "generated.py"
    if args.only:
        return [RUNS_DIR / args.only / script_name]
    paths = sorted(RUNS_DIR.glob(f"*/*/scenario_*/{script_name}"))
    if args.approach:
        paths = [p for p in paths if p.parts[-4] == args.approach]
    if args.llm:
        paths = [p for p in paths if p.parts[-3] == args.llm]
    return paths


def check_modelio() -> bool:
    script = (
        "from org.modelio.metamodel.uml.statik import Package\n"
        "_found = False\n"
        "for _root in modelingSession.getModel().getModelRoots():\n"
        "    if _root.getMClass().getName() == 'Project':\n"
        "        for _child in _root.getCompositionChildren():\n"
        "            if _child.getName() == 'MODELS26' and isinstance(_child, Package):\n"
        "                _found = True\n"
        "print 'CHECK_OK' if _found else 'CHECK_FAIL_no_MODELS26'\n"
    )
    try:
        output = send_to_modelio(script, timeout=10.0)
    except Exception as exc:
        print(f"[CHECK] cannot reach Modelio at {SCRIPTSERVER_HOST}:{SCRIPTSERVER_PORT}: {exc}")
        return False
    print(output.strip())
    return "CHECK_OK" in output


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--only", help="relative path, e.g. config-helpers/claude_opus_4_5/scenario_07")
    p.add_argument("--approach", choices=["config-helpers", "no-helper"])
    p.add_argument("--llm", choices=["claude_opus_4_5", "gpt_5_2", "glm5"])
    p.add_argument("--dry-run", action="store_true",
                   help="Print the wrapper that would be sent; do not connect.")
    p.add_argument("--check", action="store_true",
                   help="Verify Modelio is reachable and MODELS26 exists, then exit.")
    p.add_argument("--ground-truth", action="store_true",
                   help="Render ground_truth.py instead of generated.py; "
                        "output filename becomes ground_truth.png, log/error files "
                        "become ground_truth_render.{log,error.txt}, and the per-run "
                        "Modelio sub-package gets a __GT suffix to avoid colliding "
                        "with the corresponding generated-side render.")
    args = p.parse_args()

    if args.check:
        sys.exit(0 if check_modelio() else 1)

    if args.ground_truth:
        out_name = "ground_truth.png"
        log_name = "ground_truth_render.log"
        err_name = "ground_truth_render_error.txt"
        pkg_suffix = "__GT"
    else:
        out_name = "diagram_generated.png"
        log_name = "diagram_render.log"
        err_name = "diagram_render_error.txt"
        pkg_suffix = ""

    targets = iter_targets(args)
    ok = 0
    fail = 0
    t0 = time.time()
    for i, t in enumerate(targets, 1):
        rel = t.relative_to(RUNS_DIR).parent
        if not t.exists():
            print(f"[{i:3d}/{len(targets):3d}] SKIP {rel} (missing)")
            continue
        success, msg = render_one(t, dry_run=args.dry_run,
                                  out_name=out_name, log_name=log_name,
                                  err_name=err_name, pkg_suffix=pkg_suffix)
        tag = "OK  " if success else "FAIL"
        print(f"[{i:3d}/{len(targets):3d}] {tag} {rel}  ({msg})")
        if success:
            ok += 1
        else:
            fail += 1
    print(f"\n=== {ok}/{len(targets)} succeeded, {fail} failed, {time.time() - t0:.1f}s total ===")
    sys.exit(0 if fail == 0 else 1)


if __name__ == "__main__":
    main()
