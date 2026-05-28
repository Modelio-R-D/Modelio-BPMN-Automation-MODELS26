# LM Studio + Qwen Configuration for Modelio BPMN Scripts
Complete Guide v5.0 (no regex + guards fix)

---

## Part 1: LM Studio Settings
- Model: Qwen2.5-Coder-14B-Instruct (Q4_K_M)
- Context Length: 8192
- Temperature: 0.2
- Top P: 0.9
- Max Tokens: 8192
- Repeat Penalty: 1.1

---

## Part 2: System Prompt
Paste into LM Studio's System Prompt field:

```
You are an expert Jython developer for Modelio BPMN macros.

RULES - NEVER VIOLATE:

1. PYTHON 2 SYNTAX: print "text" (NOT print())

2. ASCII ONLY - no unicode

3. CODE ORDER:
   - Imports first
   - Configuration second
   - Helper functions third
   - createMyProcess() function fourth
   - Entry point LAST

4. Every element needs addToLane()

5. Flow names in flowDefs must match elementRefs keys EXACTLY

6. Copy ALL helper functions exactly - never modify parseBounds()

7. For gateway guards: use label in createSequenceFlow AND try setConditionExpression

8. Generate COMPLETE scripts - never truncate
```

---

## Part 3: Template (paste at start of every chat)

```python
# ============================================================================
# MODELIO BPMN TEMPLATE v5 - NO REGEX + GUARDS
# ============================================================================

from org.modelio.metamodel.bpmn.processCollaboration import BpmnProcess
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLane
from org.modelio.metamodel.bpmn.processCollaboration import BpmnLaneSet
from org.modelio.metamodel.bpmn.activities import BpmnUserTask
from org.modelio.metamodel.bpmn.activities import BpmnServiceTask
from org.modelio.metamodel.bpmn.activities import BpmnManualTask
from org.modelio.metamodel.bpmn.events import BpmnStartEvent
from org.modelio.metamodel.bpmn.events import BpmnEndEvent
from org.modelio.metamodel.bpmn.gateways import BpmnExclusiveGateway
from org.modelio.metamodel.bpmn.gateways import BpmnParallelGateway
from org.modelio.metamodel.bpmn.flows import BpmnSequenceFlow
from org.modelio.metamodel.uml.statik import Package
from org.eclipse.draw2d.geometry import Rectangle as Draw2DRectangle
import time

# ============================================================================
# CONFIGURATION
# ============================================================================
WAIT_TIME_MS = 50
MAX_ATTEMPTS = 3
SPACING = 120
START_X = 80

# ============================================================================
# HELPER FUNCTIONS - COPY EXACTLY
# ============================================================================

def createLane(laneSet, name):
    lane = modelingSession.getModel().createBpmnLane()
    lane.setName(name)
    lane.setLaneSet(laneSet)
    return lane

def addToLane(element, lane):
    try:
        lane.getFlowElementRef().add(element)
    except:
        pass

def createStartEvent(process, name):
    event = modelingSession.getModel().createBpmnStartEvent()
    event.setName(name)
    event.setContainer(process)
    return event

def createEndEvent(process, name):
    event = modelingSession.getModel().createBpmnEndEvent()
    event.setName(name)
    event.setContainer(process)
    return event

def createUserTask(process, name):
    task = modelingSession.getModel().createBpmnUserTask()
    task.setName(name)
    task.setContainer(process)
    return task

def createServiceTask(process, name):
    task = modelingSession.getModel().createBpmnServiceTask()
    task.setName(name)
    task.setContainer(process)
    return task

def createManualTask(process, name):
    task = modelingSession.getModel().createBpmnManualTask()
    task.setName(name)
    task.setContainer(process)
    return task

def createExclusiveGateway(process, name):
    gateway = modelingSession.getModel().createBpmnExclusiveGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway

def createParallelGateway(process, name):
    gateway = modelingSession.getModel().createBpmnParallelGateway()
    gateway.setName(name)
    gateway.setContainer(process)
    return gateway

def createSequenceFlow(process, source, target, label=""):
    """Create flow with optional guard label."""
    flow = modelingSession.getModel().createBpmnSequenceFlow()
    flow.setName(label)
    flow.setSourceRef(source)
    flow.setTargetRef(target)
    flow.setContainer(process)
    # Also set condition expression for guard display
    if label:
        try:
            flow.setConditionExpression(label)
        except:
            pass
    return flow

# ============================================================================
# DIAGRAM UTILITIES - NO REGEX
# ============================================================================

def parseBounds(boundsStr):
    """Parse Rectangle(x, y, w, h) using string operations - NO REGEX."""
    try:
        startIdx = boundsStr.find("(")
        endIdx = boundsStr.rfind(")")
        if startIdx == -1 or endIdx == -1:
            return None
        inner = boundsStr[startIdx + 1:endIdx]
        parts = inner.split(",")
        if len(parts) == 4:
            return {
                "x": float(parts[0].strip()),
                "y": float(parts[1].strip()),
                "w": float(parts[2].strip()),
                "h": float(parts[3].strip())
            }
    except:
        pass
    return None

def getGraphics(diagramHandle, element):
    try:
        graphics = diagramHandle.getDiagramGraphics(element)
        if graphics is not None and graphics.size() > 0:
            return graphics.get(0)
    except:
        pass
    return None

def getBounds(diagramHandle, element):
    dg = getGraphics(diagramHandle, element)
    if dg:
        return parseBounds(str(dg.getBounds()))
    return None

def getLaneCenterY(diagramHandle, lane):
    bounds = getBounds(diagramHandle, lane)
    if bounds:
        return bounds["y"] + bounds["h"] / 2 - 23
    return None

def waitForElements(diagramHandle, elements):
    elementGraphics = {}
    attempt = 0
    while attempt < MAX_ATTEMPTS:
        attempt += 1
        for elem in elements:
            name = elem.getName()
            if name not in elementGraphics:
                dg = getGraphics(diagramHandle, elem)
                if dg:
                    elementGraphics[name] = dg
        if len(elementGraphics) == len(elements):
            print "  [Attempt " + str(attempt) + "] All elements ready"
            return elementGraphics, attempt
        time.sleep(WAIT_TIME_MS / 1000.0)
    print "  [Attempt " + str(attempt) + "] Timeout"
    return elementGraphics, attempt

def unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout):
    unmaskedCount = 0
    laneY = {}
    for laneName, lane in lanes.items():
        bounds = getBounds(diagramHandle, lane)
        if bounds:
            laneY[laneName] = int(bounds["y"] + bounds["h"] / 2)
    for elem in elements:
        name = elem.getName()
        if name not in elementGraphics:
            laneName = elementLayout.get(name, (0, ""))[1]
            targetY = laneY.get(laneName, 100)
            try:
                result = diagramHandle.unmask(elem, 100, targetY)
                if result and result.size() > 0:
                    elementGraphics[name] = result.get(0)
                    unmaskedCount += 1
            except:
                pass
    return unmaskedCount

# ============================================================================
# MAIN PROCESS FUNCTION
# ============================================================================

def createMyProcess(parentPackage):
    print "== PHASE 1: CREATE PROCESS & LANES =="
    
    process = modelingSession.getModel().createBpmnProcess()
    process.setName("MyProcess")
    process.setOwner(parentPackage)
    
    laneSet = modelingSession.getModel().createBpmnLaneSet()
    laneSet.setProcess(process)
    
    # Create lanes
    lane1 = createLane(laneSet, "Lane1")
    lane2 = createLane(laneSet, "Lane2")
    
    lanes = {
        "Lane1": lane1,
        "Lane2": lane2
    }
    
    print "== PHASE 2: CREATE ELEMENTS =="
    
    # Create elements - EVERY element needs addToLane()
    start = createStartEvent(process, "Start")
    addToLane(start, lane1)
    
    task1 = createUserTask(process, "Task 1")
    addToLane(task1, lane1)
    
    gateway = createExclusiveGateway(process, "Decision")
    addToLane(gateway, lane2)
    
    endYes = createEndEvent(process, "End Yes")
    addToLane(endYes, lane2)
    
    endNo = createEndEvent(process, "End No")
    addToLane(endNo, lane1)
    
    # Collect elements
    elements = [start, task1, gateway, endYes, endNo]
    
    # Element references - NAMES MUST MATCH EXACTLY
    elementRefs = {
        "Start": start,
        "Task 1": task1,
        "Decision": gateway,
        "End Yes": endYes,
        "End No": endNo,
    }
    
    # Layout: name -> (column, lane)
    elementLayout = {
        "Start": (0, "Lane1"),
        "Task 1": (1, "Lane1"),
        "Decision": (2, "Lane2"),
        "End Yes": (3, "Lane2"),
        "End No": (3, "Lane1"),
    }
    
    print "== PHASE 3: CREATE DIAGRAM =="
    
    diagram = modelingSession.getModel().createBpmnProcessDesignDiagram()
    diagram.setName("MyProcess Diagram")
    diagram.setOrigin(process)
    
    diagramService = Modelio.getInstance().getDiagramService()
    diagramHandle = diagramService.getDiagramHandle(diagram)
    diagramHandle.save()
    
    print "== PHASE 4: WAIT FOR ELEMENTS =="
    
    elementGraphics, attempts = waitForElements(diagramHandle, elements)
    
    if len(elementGraphics) < len(elements):
        unmaskMissingElements(diagramHandle, elements, elementGraphics, lanes, elementLayout)
        diagramHandle.save()
    
    print "== PHASE 5: REPOSITION ELEMENTS =="
    
    laneY = {}
    for laneName, lane in lanes.items():
        y = getLaneCenterY(diagramHandle, lane)
        if y:
            laneY[laneName] = y
    
    for elem in elements:
        name = elem.getName()
        if name in elementLayout and name in elementGraphics:
            col, laneName = elementLayout[name]
            dg = elementGraphics[name]
            bounds = getBounds(diagramHandle, elem)
            if bounds:
                targetX = START_X + SPACING * col
                targetY = laneY.get(laneName, 100)
                newBounds = Draw2DRectangle(int(targetX), int(targetY), int(bounds["w"]), int(bounds["h"]))
                dg.setBounds(newBounds)
                diagramHandle.save()
    
    print "== PHASE 6: CREATE FLOWS =="
    
    # FLOWS: (source, target, guard_label)
    # Guard labels appear on gateway exit arrows
    flowDefs = [
        ("Start", "Task 1", ""),
        ("Task 1", "Decision", ""),
        ("Decision", "End Yes", "Yes"),    # Guard: Yes
        ("Decision", "End No", "No"),      # Guard: No
    ]
    
    for srcName, tgtName, label in flowDefs:
        src = elementRefs.get(srcName)
        tgt = elementRefs.get(tgtName)
        if src and tgt:
            createSequenceFlow(process, src, tgt, label)
    
    diagramHandle.save()
    diagramHandle.close()
    
    print "== COMPLETE =="

# ============================================================================
# ENTRY POINT - MUST BE LAST
# ============================================================================

if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createMyProcess(element)
    else:
        print "ERROR: Select a Package."
else:
    print "ERROR: Select a Package first."


Now create a BPMN process for: [YOUR DESCRIPTION]

RULES:
1. Copy ALL helper functions exactly
2. parseBounds uses string parsing, NOT regex
3. flowDefs names must match elementRefs keys exactly
4. Gateway exit flows need labels: ("Gateway", "Target", "Yes")
5. Entry point must be LAST
6. Use Python 2: print "text"
```


---

## Part 4: Checklist
- [ ] parseBounds uses string find/split, NOT regex
- [ ] All print use: print "text"
- [ ] Entry point at VERY END
- [ ] Every element has addToLane()
- [ ] flowDefs names match elementRefs exactly
- [ ] Gateway flows have labels: ("Gateway", "EndYes", "Yes")
- [ ] createSequenceFlow sets both name AND conditionExpression

---

## Part 5: Common Errors

### Lanes in wrong position
- Cause: parseBounds was modified or uses regex
- Fix: use the string parsing version exactly

### Guards not showing
- Cause: createSequenceFlow missing setConditionExpression
- Fix: add:
```python
if label:
    try:
        flow.setConditionExpression(label)
    except:
        pass
```

### Flows not created
- Cause: flowDefs name doesn't match elementRefs
- Fix: ensure exact name match:
```python
# Element:
endYes = createEndEvent(process, "End Yes")

# elementRefs:
elementRefs = {"End Yes": endYes}  # Must match!

# flowDefs:
flowDefs = [("Decision", "End Yes", "Yes")]  # Must match!
```

### SyntaxError
- Cause: Python 3 syntax
- Fix: use print "text" not print()
