# S1 - Document Approval - GPT-5.2 Thinking
# Paste generated script here

# -*- coding: utf-8 -*-
# Modelio Jython macro: Create a simple BPMN document approval process diagram (1 lane, linear flow)

from org.modelio.api.modelio import Modelio
from java.awt import Rectangle
import traceback

# -----------------------------------------------------------------------------
# Helpers (robust across minor API variations)
# -----------------------------------------------------------------------------

def _invoke_first(obj, names, *args):
    for n in names:
        try:
            m = getattr(obj, n)
        except:
            m = None
        if m:
            try:
                m(*args)
                return True
            except:
                pass
    return False

def _add_to(owner, getter_names, child):
    for n in getter_names:
        g = getattr(owner, n, None)
        if g:
            try:
                coll = g()
                try:
                    coll.add(child)
                except:
                    # Some lists might behave like Python lists (rare)
                    coll.append(child)
                return True
            except:
                pass
    return False

def _create(model, method_names):
    for n in method_names:
        m = getattr(model, n, None)
        if m:
            try:
                return m()
            except:
                pass
    raise Exception("Cannot create element with any of: %s" % (method_names,))

def _set_name(el, name):
    _invoke_first(el, ["setName"], name)

def _set_bounds(g, x, y, w, h):
    rect = Rectangle(x, y, w, h)
    if _invoke_first(g, ["setBounds"], rect):
        return
    # fallback: some APIs accept (x,y,w,h)
    if _invoke_first(g, ["setBounds"], x, y, w, h):
        return
    # fallback: location + size
    _invoke_first(g, ["setLocation"], x, y)
    _invoke_first(g, ["setSize"], w, h)

def _attach_as_owned(root_pkg, element):
    # Try common ownership relations (Behavior vs. ModelTree vs. generic)
    if _add_to(root_pkg, ["getOwnedElement"], element):
        return True
    if _add_to(root_pkg, ["getOwnedBehavior"], element):
        return True
    if _add_to(root_pkg, ["getOwnedOperation"], element):
        return True
    if _add_to(root_pkg, ["getOwned"], element):
        return True
    return False

def _set_container(flow_element, process):
    # Prefer container setter, else add to process.getFlowElement()
    if _invoke_first(flow_element, ["setContainer"], process):
        return True
    return _add_to(process, ["getFlowElement"], flow_element)

def _add_to_lane(lane, flow_element):
    # Prefer lane reference list, else element.getLane().add(lane)
    if _add_to(lane, ["getFlowElementRef"], flow_element):
        return True
    # fallback: set element lane ref (if available)
    return _add_to(flow_element, ["getLane", "getPartitionedLaneRefs"], lane)

def _set_sequence_end(flow, src, dst):
    ok1 = _invoke_first(flow, ["setSourceRef", "setSource", "setFromRef", "setFrom"], src)
    ok2 = _invoke_first(flow, ["setTargetRef", "setTarget", "setToRef", "setTo"], dst)
    if not (ok1 and ok2):
        # Some implementations use different naming; try the inverse getters as last resort
        ok1 = ok1 or _invoke_first(flow, ["setFromElement", "setSourceElement"], src)
        ok2 = ok2 or _invoke_first(flow, ["setToElement", "setTargetElement"], dst)
    return ok1 and ok2

def _get_root_package(model):
    # Works in standard Modelio projects
    roots = model.getModelRoots()
    for r in roots:
        try:
            # Project metaclass
            if r.getMClass().getName() == "Project":
                return r.getModel()
        except:
            pass
    # Fallback: first root that has getOwnedElement()
    for r in roots:
        try:
            if hasattr(r, "getOwnedElement"):
                return r
        except:
            pass
    raise Exception("Cannot find a root package (Project.getModel())")

def _create_process_design_diagram(model, owner, origin_process, name):
    diag = None
    m = getattr(model, "createBpmnProcessDesignDiagram", None)
    if m:
        # Try common overloads (Jython will pick the matching Java signature)
        for args in [
            (name, owner, origin_process),
            (name, origin_process, owner),
            (name, origin_process),
            (name, owner),
            tuple(),
        ]:
            try:
                diag = m(*args)
                break
            except:
                pass

    if diag is None:
        raise Exception("IUmlModel.createBpmnProcessDesignDiagram(...) is not available in this environment.")

    # Ensure name + origin/context is set
    _set_name(diag, name)
    _invoke_first(diag, ["setOrigin", "setRepresented", "setContext"], origin_process)

    # Ensure diagram is owned somewhere (prefer process products, then owner products)
    if not _add_to(origin_process, ["getProduct"], diag):
        _add_to(owner, ["getProduct"], diag)
        _add_to(owner, ["getOwnedElement"], diag)

    return diag

def _get_diagram_handle(diagram_service, diagram):
    # Typical API: diagramService.getDiagramHandle(AbstractDiagram)
    for meth in ["getDiagramHandle", "openDiagramHandle", "getHandle"]:
        m = getattr(diagram_service, meth, None)
        if m:
            try:
                return m(diagram)
            except:
                pass
    raise Exception("Cannot obtain a diagram handle (IDiagramHandle) from diagram service.")

def _unmask(diagram_handle, element, x, y, parent_graphic=None):
    # Some APIs support unmask(element, parent, x, y). If not, fallback to unmask(element, x, y).
    if parent_graphic is not None:
        try:
            return diagram_handle.unmask(element, parent_graphic, x, y)
        except:
            pass
    return diagram_handle.unmask(element, x, y)

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

modelio = Modelio.getInstance()
session = modelio.getModelingSession()
model = session.getModel()
services = modelio.getModelioServices()
diagram_service = services.getDiagramService()

t = session.createTransaction("Create BPMN document approval process")
try:
    # Owner (root package)
    root_pkg = _get_root_package(model)

    # 1) Create a new BpmnProcess
    bpmn_process = _create(model, ["createBpmnProcess"])
    _set_name(bpmn_process, "Document Approval Process")
    if not _attach_as_owned(root_pkg, bpmn_process):
        raise Exception("Failed to attach BpmnProcess to the model root package.")

    # 2) Create BpmnLanes for each role (single lane: Reviewer)
    lane_set = None
    if hasattr(model, "createBpmnLaneSet"):
        lane_set = _create(model, ["createBpmnLaneSet"])
        _set_name(lane_set, "LaneSet")

        # Attach lane set to process (try both directions)
        if not _invoke_first(bpmn_process, ["setLaneSet"], lane_set):
            # Some metamodels use getLaneSe


# Modelio output:

org.python.antlr.ParseException: org.python.antlr.ParseException: encoding declaration in Unicode string
org.python.antlr.ParseException: encoding declaration in Unicode string
	at org.python.core.ParserFacade.prepBufReader(ParserFacade.java:281)
	at org.python.core.ParserFacade.parseExpressionOrModule(ParserFacade.java:123)
	at org.python.util.PythonInterpreter.compile(PythonInterpreter.java:321)
	at org.python.util.PythonInterpreter.compile(PythonInterpreter.java:317)
	at org.python.util.PythonInterpreter.compile(PythonInterpreter.java:309)
	at org.python.jsr223.PyScriptEngine.compileScript(PyScriptEngine.java:87)
	at org.python.jsr223.PyScriptEngine.eval(PyScriptEngine.java:31)
	at java.scripting/javax.script.AbstractScriptEngine.eval(AbstractScriptEngine.java:264)
	at org.modelio.platform.script.engine.core.engine.PythonRunner$ClassLoaderScriptEngine.eval(PythonRunner.java:303)
	at org.modelio.platform.script.engine.core.engine.PythonRunner.evalScript(PythonRunner.java:191)
	at org.modelio.platform.script.engine.core.engine.PythonRunner.runScript(PythonRunner.java:123)
	at org.modelio.platform.script.engine.core.engine.TransactionScriptRunner.runScript(TransactionScriptRunner.java:71)
	at org.modelio.script.handlers.EvalScriptHandler.execute(EvalScriptHandler.java:50)
	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.base/java.lang.reflect.Method.invoke(Method.java:566)
	at org.eclipse.e4.core.internal.di.MethodRequestor.execute(MethodRequestor.java:58)
	at org.eclipse.e4.core.internal.di.InjectorImpl.invokeUsingClass(InjectorImpl.java:319)
	at org.eclipse.e4.core.internal.di.InjectorImpl.invoke(InjectorImpl.java:253)
	at org.eclipse.e4.core.contexts.ContextInjectionFactory.invoke(ContextInjectionFactory.java:173)
	at org.eclipse.e4.core.commands.internal.HandlerServiceHandler.execute(HandlerServiceHandler.java:156)
	at org.eclipse.core.commands.Command.executeWithChecks(Command.java:488)
	at org.eclipse.core.commands.ParameterizedCommand.executeWithChecks(ParameterizedCommand.java:487)
	at org.eclipse.e4.core.commands.internal.HandlerServiceImpl.executeHandler(HandlerServiceImpl.java:213)
	at org.eclipse.e4.ui.workbench.renderers.swt.HandledContributionItem.executeItem(HandledContributionItem.java:438)
	at org.eclipse.e4.ui.workbench.renderers.swt.AbstractContributionItem.handleWidgetSelection(AbstractContributionItem.java:449)
	at org.eclipse.e4.ui.workbench.renderers.swt.AbstractContributionItem.lambda$2(AbstractContributionItem.java:475)
	at org.eclipse.swt.widgets.EventTable.sendEvent(EventTable.java:89)
	at org.eclipse.swt.widgets.Display.sendEvent(Display.java:4251)
	at org.eclipse.swt.widgets.Widget.sendEvent(Widget.java:1066)
	at org.eclipse.swt.widgets.Display.runDeferredEvents(Display.java:4068)
	at org.eclipse.swt.widgets.Display.readAndDispatch(Display.java:3645)
	at org.eclipse.e4.ui.internal.workbench.swt.PartRenderingEngine$5.run(PartRenderingEngine.java:1157)
	at org.eclipse.core.databinding.observable.Realm.runWithDefault(Realm.java:338)
	at org.eclipse.e4.ui.internal.workbench.swt.PartRenderingEngine.run(PartRenderingEngine.java:1046)
	at org.eclipse.e4.ui.internal.workbench.E4Workbench.createAndRunUI(E4Workbench.java:155)
	at org.eclipse.e4.ui.internal.workbench.swt.E4Application.start(E4Application.java:166)
	at org.eclipse.equinox.internal.app.EclipseAppHandle.run(EclipseAppHandle.java:203)
	at org.eclipse.core.runtime.internal.adaptor.EclipseAppLauncher.runApplication(EclipseAppLauncher.java:134)
	at org.eclipse.core.runtime.internal.adaptor.EclipseAppLauncher.start(EclipseAppLauncher.java:104)
	at org.eclipse.core.runtime.adaptor.EclipseStarter.run(EclipseStarter.java:401)
	at org.eclipse.core.runtime.adaptor.EclipseStarter.run(EclipseStarter.java:255)
	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.base/java.lang.reflect.Method.invoke(Method.java:566)
	at org.eclipse.equinox.launcher.Main.invokeFramework(Main.java:653)
	at org.eclipse.equinox.launcher.Main.basicRun(Main.java:590)
	at org.eclipse.equinox.launcher.Main.run(Main.java:1461)
org.python.antlr.ParseException: org.python.antlr.ParseException: encoding declaration in Unicode string