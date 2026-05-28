# -*- coding: utf-8 -*-
#
# render_all.py - Modelio macro
# =============================
#
# For every LLM-generated script under
#   evaluation/runs/<approach>/<llm>/scenario_<NN>/generated.py
# this macro creates a fresh sub-package, executes the generated script
# inside that sub-package, and saves a PNG of the resulting BPMN diagram
# as evaluation/runs/.../diagram_generated.png. It is the portable reproduction
# path for the renders committed to the artifact.
#
# This macro uses only standard Modelio APIs (transactions, the
# DiagramService, saveInFile). No additional Modelio modules are
# required.
#
# INSTALL
# -------
#   Copy this file to your Modelio macros folder:
#     Windows: C:\<Modelio install>\.modelio\5.4\macros\render_all.py
#     Linux:   ~/.modelio/5.4/macros/render_all.py
#     macOS:   ~/.modelio/5.4/macros/render_all.py
#   (Replace 5.4 with your Modelio version.)
#
# CONFIGURE
# ---------
#   Edit REPO_ROOT below to point at your local clone of
#   Modelio-BPMN-Automation-MODELS26.
#
# RUN
# ---
#   1. Open Modelio with a project that contains a top-level package
#      named MODELS26 (create it if missing).
#   2. Right-click the MODELS26 package -> Macros -> render_all.
#   3. The macro prints progress; PNGs appear next to each generated.py.
#
# OPTIONS
# -------
#   ONLY_APPROACH / ONLY_LLM / ONLY_SCENARIO let you restrict the run.
#   Leave them as None to render everything.
#
# Applicable on: Package
#

import os
import re

from org.modelio.metamodel.uml.statik import Package
from org.modelio.metamodel.diagrams import AbstractDiagram

# ============================================================================
# CONFIGURATION
# ============================================================================

# Absolute path to your local clone of Modelio-BPMN-Automation-MODELS26.
REPO_ROOT = r"C:/_code/Modelio-BPMN-Automation-MODELS26"

# Set to a string to restrict; leave as None for "render everything".
ONLY_APPROACH = None        # e.g. "config-helpers" or "no-helper"
ONLY_LLM      = None        # e.g. "claude_opus_4_5", "gpt_5_2", "glm5"
ONLY_SCENARIO = None        # e.g. "scenario_07"

PNG_RESOLUTION = 10         # second argument to dh.saveInFile

# ============================================================================
# HELPERS
# ============================================================================

EXECFILE_PAT = re.compile(
    r'execfile\(\s*[\'"]([^\'"]*BPMN_Helpers\.py)[\'"]\s*\)'
)


def _patch_helper_path(script_text):
    """Rewrite the captured execfile() path to point at the in-repo helper."""
    repo_helper = REPO_ROOT.replace("\\", "/") + "/approaches/config-helpers/BPMN_Helpers.py"
    return EXECFILE_PAT.sub('execfile("' + repo_helper + '")', script_text)


def _safe_pkg_name(approach, llm, scenario):
    raw = approach + "__" + llm + "__" + scenario
    return re.sub(r"[^A-Za-z0-9_]", "_", raw)


class _SelShim(object):
    """selectedElements stand-in for captured macros that read .size / .get(i)."""
    def __init__(self, items):
        self._items = items
        self.size = len(items)

    def get(self, i):
        return self._items[i]


def _find_models26():
    factory = modelingSession.getModel()
    for root in factory.getModelRoots():
        if root.getMClass().getName() == 'Project':
            for child in root.getCompositionChildren():
                if child.getName() == 'MODELS26' and isinstance(child, Package):
                    return child
    return None


def _get_or_create_subpkg(parent, name):
    for elem in parent.getOwnedElement():
        if elem.getName() == name and isinstance(elem, Package):
            return elem, False
    tx = modelingSession.createTransaction("RenderSetup_" + name)
    try:
        sub = modelingSession.getModel().createPackage(name, parent)
        tx.commit()
        return sub, True
    except:
        tx.rollback()
        raise


def _snapshot_diagrams():
    snap = set()
    for d in modelingSession.findByClass(AbstractDiagram):
        snap.add(d)
    return snap


def _list_runs():
    """Yield (approach, llm, scenario, script_path) for every generated.py."""
    runs_root = os.path.join(REPO_ROOT, "evaluation", "runs")
    if not os.path.isdir(runs_root):
        raise Exception("REPO_ROOT does not contain evaluation/runs/: " + runs_root)

    for approach in sorted(os.listdir(runs_root)):
        if ONLY_APPROACH is not None and approach != ONLY_APPROACH:
            continue
        adir = os.path.join(runs_root, approach)
        if not os.path.isdir(adir):
            continue
        for llm in sorted(os.listdir(adir)):
            if ONLY_LLM is not None and llm != ONLY_LLM:
                continue
            ldir = os.path.join(adir, llm)
            if not os.path.isdir(ldir):
                continue
            for scenario in sorted(os.listdir(ldir)):
                if ONLY_SCENARIO is not None and scenario != ONLY_SCENARIO:
                    continue
                sdir = os.path.join(ldir, scenario)
                gen_py = os.path.join(sdir, "generated.py")
                if os.path.isfile(gen_py):
                    yield (approach, llm, scenario, gen_py)


# ============================================================================
# PER-RUN EXECUTION
# ============================================================================

def _render_one(approach, llm, scenario, script_path, models26):
    out_dir = os.path.dirname(script_path)
    out_png = os.path.join(out_dir, "diagram_generated.png").replace("\\", "/")
    err_path = os.path.join(out_dir, "diagram_render_error.txt")
    if os.path.isfile(err_path):
        try:
            os.remove(err_path)
        except:
            pass

    pkgname = _safe_pkg_name(approach, llm, scenario)
    subpkg, _ = _get_or_create_subpkg(models26, pkgname)

    f = open(script_path, "r")
    try:
        raw = f.read()
    finally:
        f.close()
    script = _patch_helper_path(raw)

    # Snapshot existing diagrams, inject selectedElements shim, exec captured script.
    before = _snapshot_diagrams()

    # The captured macros expect a module-global `selectedElements` with .size/.get.
    # Stash the GUI's selection, swap in our shim, restore on the way out.
    global selectedElements
    try:
        _saved_sel = selectedElements
    except NameError:
        _saved_sel = None

    selectedElements = _SelShim([subpkg])

    tx = modelingSession.createTransaction("Render_" + pkgname)
    try:
        exec(script) in globals()
        tx.commit()
    except Exception, ex:
        tx.rollback()
        msg = "RUN ERROR: " + type(ex).__name__ + ": " + str(ex)
        ef = open(err_path, "w")
        try:
            ef.write(msg + "\n")
        finally:
            ef.close()
        if _saved_sel is not None:
            selectedElements = _saved_sel
        return False, msg

    if _saved_sel is not None:
        selectedElements = _saved_sel

    # Find any newly created diagram and export it.
    diagramService = Modelio.getInstance().getDiagramService()
    new_diagrams = []
    for d in modelingSession.findByClass(AbstractDiagram):
        if d not in before:
            new_diagrams.append(d)

    if not new_diagrams:
        msg = "NO_DIAGRAM_PRODUCED"
        ef = open(err_path, "w")
        try:
            ef.write(msg + "\n")
        finally:
            ef.close()
        return False, msg

    target = new_diagrams[0]
    dh = diagramService.getDiagramHandle(target)
    try:
        dh.saveInFile("PNG", out_png, PNG_RESOLUTION)
    finally:
        dh.close()
    return True, "ok -> " + target.getName()


# ============================================================================
# MAIN
# ============================================================================

def main():
    models26 = _find_models26()
    if models26 is None:
        print "ERROR: no top-level package named 'MODELS26' under any Project root."
        print "       Create it in Modelio, then re-run this macro."
        return

    ok = 0
    fail = 0
    runs = list(_list_runs())
    print "Rendering " + str(len(runs)) + " runs..."
    i = 0
    for (approach, llm, scenario, script_path) in runs:
        i = i + 1
        rel = approach + "/" + llm + "/" + scenario
        success, msg = _render_one(approach, llm, scenario, script_path, models26)
        tag = "OK  " if success else "FAIL"
        print "[" + str(i).rjust(3) + "/" + str(len(runs)) + "] " + tag + " " + rel + "  (" + msg + ")"
        if success:
            ok = ok + 1
        else:
            fail = fail + 1

    print ""
    print "=== " + str(ok) + "/" + str(len(runs)) + " succeeded, " + str(fail) + " failed ==="


main()
