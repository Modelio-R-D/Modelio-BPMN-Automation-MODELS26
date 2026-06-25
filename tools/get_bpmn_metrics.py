# ============================================================================
# BPMN Metrics Inspector - Modelio Macro
# ============================================================================
# Usage:
#   1. In Modelio, select a BpmnProcess (or its parent Package) in the explorer
#   2. Go to Tools > Macros > Run Macro (or assign to a toolbar/shortcut)
#   3. Metrics will be printed in the Script console
# ============================================================================

from org.modelio.metamodel.bpmn.processCollaboration import BpmnProcess
from org.modelio.metamodel.bpmn.gateways import BpmnGateway
from org.modelio.metamodel.bpmn.flows import BpmnSequenceFlow
from org.modelio.metamodel.uml.statik import Package


def get_bpmn_metrics(process):
    """Extract and print metrics from a BpmnProcess element."""
    lane_set = process.getLaneSet()
    lanes = list(lane_set.getLane()) if lane_set else []

    flow_elements = list(process.getFlowElement())
    gateways       = []
    seq_flows      = []
    data_objects   = []
    data_assocs    = []
    other_elements = []

    for fe in flow_elements:
        class_name = fe.getMClass().getName()
        if isinstance(fe, BpmnGateway):
            gateways.append(fe)
        elif isinstance(fe, BpmnSequenceFlow):
            seq_flows.append(fe)
        elif 'DataObject' in class_name or 'DataStore' in class_name:
            data_objects.append(fe)
        else:
            other_elements.append(fe)

    for fe in flow_elements:
        class_name = fe.getMClass().getName()
        if 'Task' in class_name or 'SubProcess' in class_name:
            data_assocs += list(fe.getDataInputAssociation()) + list(fe.getDataOutputAssociation())

    total_elements = len(gateways) + len(other_elements) + len(data_objects)

    print "BPMN_METRICS:lanes=%d,elements=%d,gateways=%d,flows=%d,data=%d,data_assoc=%d" % (
        len(lanes), total_elements, len(gateways),
        len(seq_flows), len(data_objects), len(data_assocs)
    )


# ============================================================================
# ENTRY POINT
# ============================================================================
# selectedElements is populated by the Modelio UI when user selects something.

if selectedElements is None or selectedElements.size() == 0:
    print "ERROR: Nothing selected. Please select a BpmnProcess or a Package containing one."
else:
    element = selectedElements.get(0)

    if isinstance(element, BpmnProcess):
        # Direct selection of a process
        get_bpmn_metrics(element)

    elif isinstance(element, Package):
        # Package selected — find all BpmnProcesses inside it
        processes = [b for b in element.getOwnedBehavior() if isinstance(b, BpmnProcess)]
        if not processes:
            print "ERROR: No BpmnProcess found in package:", element.getName()
        else:
            print "Found", len(processes), "process(es) in package:", element.getName()
            for proc in processes:
                get_bpmn_metrics(proc)

    else:
        print "ERROR: Selected element is neither a BpmnProcess nor a Package."
        print "Selected:", element.getMClass().getName(), "-", element.getName()
