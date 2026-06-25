"""
bpmn_to_complexity.py
=====================
Reads a JSONL file where each record contains an 'output' field with a
BPMN XML string, extracts structural complexity metrics, classifies the
process, and writes an enriched JSONL.

Two new attributes are added to each record:

    "complexity_metrics": {
        "lanes":        <int>,   # number of <lane> elements (1 if no swimlanes)
        "elements":     <int>,   # tasks + gateways + events
        "gateways":     <int>,   # gateway nodes only
        "flows":        <int>,   # sequence flows
        "data_objects": <int>,   # dataObject / dataObjectReference elements
        "data_assoc":   <int>    # dataInputAssociation + dataOutputAssociation
    }
    "complexity": "Simple" | "Medium" | "Complex"


Usage
-----
    python bpmn_to_complexity.py                     # runs built-in example
    python bpmn_to_complexity.py input.jsonl
    python bpmn_to_complexity.py input.jsonl -o output.jsonl
    python bpmn_to_complexity.py input.jsonl -n 5
    python bpmn_to_complexity.py input.jsonl -i 2

Reuses parse_bpmn() from bpmn_to_modelio.py (must be in same folder).
"""

import json
import sys
import os
import argparse
import xml.etree.ElementTree as ET

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS_DIR)
from bpmn_to_config import parse_bpmn  # noqa: E402


# ---------------------------------------------------------------------------
# 1.  METRICS EXTRACTOR
# ---------------------------------------------------------------------------

BPMN_NS = 'http://www.omg.org/spec/BPMN/20100524/MODEL'
NS = {'b': BPMN_NS}

_TASK_TAGS  = {'task', 'userTask', 'serviceTask', 'sendTask', 'receiveTask',
               'manualTask', 'scriptTask', 'businessRuleTask',
               'callActivity', 'subProcess'}
_GW_TAGS    = {'exclusiveGateway', 'parallelGateway', 'inclusiveGateway',
               'eventBasedGateway', 'complexGateway'}
_EVT_TAGS   = {'startEvent', 'endEvent', 'intermediateCatchEvent',
               'intermediateThrowEvent', 'boundaryEvent'}
_DATA_TAGS  = {'dataObject', 'dataObjectReference',
               'dataStore',  'dataStoreReference'}
_ASSOC_TAGS = {'dataInputAssociation', 'dataOutputAssociation'}


def _local(tag):
    return tag.split('}')[-1] if '}' in tag else tag


def extract_metrics(xml_text):
    """
    Parse a BPMN XML string and return a metrics dict.

    Returns
    -------
    dict with keys: lanes, elements, gateways, flows, data_objects, data_assoc
    """
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        raise ValueError(f"Invalid BPMN XML: {e}")

    # Collect all <process> elements (handles both single-process and collaboration BPMNs)
    if _local(root.tag) == 'process':
        procs = [root]
    else:
        procs = [e for e in root.iter() if _local(e.tag) == 'process']
    if not procs:
        raise ValueError("No <process> element found")

    tasks      = 0
    gateways   = 0
    events     = 0
    data_obj   = 0
    data_assoc = 0
    flows      = 0

    for proc in procs:
        for elem in proc:
            local = _local(elem.tag)

            if local in _TASK_TAGS:
                tasks += 1
            elif local in _GW_TAGS:
                gateways += 1
            elif local in _EVT_TAGS:
                events += 1
            elif local in _DATA_TAGS:
                data_obj += 1
            elif local == 'sequenceFlow':
                flows += 1

        # Data associations are nested inside task elements
        for elem in proc.iter():
            if _local(elem.tag) in _ASSOC_TAGS:
                data_assoc += 1

    # Lanes — aggregate across all processes
    lanes_list = []
    for proc in procs:
        lanes_list.extend(proc.findall('.//b:lane', NS) or proc.findall('.//lane'))
    lane_count = len(lanes_list) if lanes_list else 1

    elements = tasks + gateways + events

    return {
        'lanes':        lane_count,
        'elements':     elements,
        'gateways':     gateways,
        'flows':        flows,
        'data_objects': data_obj,
        'data_assoc':   data_assoc,
    }


# ---------------------------------------------------------------------------
# 2.  COMPLEXITY CLASSIFIER
# ---------------------------------------------------------------------------

def classify_complexity(elements, lanes, gateways, data_objects):
    """
    Classify a BPMN process as Simple / Medium / Complex.

    Simple  : small self-contained process, single lane, at most 1 gateway,
              no data objects.
    Medium  : moderate size, up to 3 lanes, up to 2 gateways.
    Complex : everything else.
    """
    if (
        3 <= elements <= 6
        and lanes == 1
        and gateways <= 1
        and data_objects == 0
    ):
        return "Simple"
    elif (
        7 <= elements <= 12
        and 1 <= lanes <= 3
        and 1 <= gateways <= 2
    ):
        return "Medium"
    else:
        return "Complex"


# ---------------------------------------------------------------------------
# 3.  PER-RECORD ANALYSIS
# ---------------------------------------------------------------------------

def analyse_record(json_obj):
    """Enrich a JSONL record with complexity_metrics and complexity."""
    xml_text = json_obj['output']
    metrics  = extract_metrics(xml_text)
    label    = classify_complexity(
        elements=metrics['elements'],
        lanes=metrics['lanes'],
        gateways=metrics['gateways'],
        data_objects=metrics['data_objects'],
    )
    obj = dict(json_obj)
    obj['complexity_metrics'] = metrics
    obj['complexity']         = label
    return obj


# ---------------------------------------------------------------------------
# 4.  JSONL PIPELINE
# ---------------------------------------------------------------------------

def process_jsonl(input_path, output_path=None, limit=None, index=None):
    if output_path is None:
        base, _ = os.path.splitext(input_path)
        output_path = base + '_complexity.jsonl'

    written = 0
    with open(input_path, encoding='utf-8') as fh, open(output_path, 'w', encoding='utf-8') as out_fh:
        for i, raw_line in enumerate(fh):
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            if index is not None and i != index:
                continue
            if limit is not None and i >= limit:
                break

            try:
                obj = json.loads(raw_line)
            except json.JSONDecodeError as e:
                print(f"WARNING: skipping line {i}: {e}", file=sys.stderr)
                continue

            try:
                obj = analyse_record(obj)
            except Exception as e:
                print(f"WARNING: error on line {i} ({e})", file=sys.stderr)
                obj['complexity_metrics'] = None
                obj['complexity']         = None

            out_fh.write(json.dumps(obj, ensure_ascii=False) + '\n')
            written += 1

    print(f"Done: {written} records written to {output_path}")


# ---------------------------------------------------------------------------
# 5.  BUILT-IN EXAMPLE
# ---------------------------------------------------------------------------

def _run_example():
    # Sample from the dataset — budget process with data objects
    example_xml = """<?xml version="1.0" ?>
<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL">
  <process id="Process_1" name="Budget Approval">
    <laneSet id="LaneSet_1">
      <lane id="Lane_1" name="Department">
        <flowNodeRef>Task_1</flowNodeRef>
        <flowNodeRef>Task_2</flowNodeRef>
        <flowNodeRef>Task_3</flowNodeRef>
        <flowNodeRef>StartEvent_1</flowNodeRef>
      </lane>
      <lane id="Lane_2" name="Finance">
        <flowNodeRef>Task_4</flowNodeRef>
        <flowNodeRef>Task_5</flowNodeRef>
        <flowNodeRef>ExclusiveGateway_1</flowNodeRef>
        <flowNodeRef>EndEvent_1</flowNodeRef>
      </lane>
    </laneSet>
    <startEvent id="StartEvent_1" name="Start"/>
    <task id="Task_1" name="Outline objectives"/>
    <task id="Task_2" name="Draft plan"/>
    <task id="Task_3" name="Adjust plan"/>
    <task id="Task_4" name="Review feasibility"/>
    <task id="Task_5" name="Allocate budget"/>
    <exclusiveGateway id="ExclusiveGateway_1" name="Approved?"/>
    <endEvent id="EndEvent_1" name="End"/>
    <dataObject id="DataObject_1" name="Budget Plan"/>
    <dataObject id="DataObject_2" name="Approval Record"/>
    <sequenceFlow id="SF_1" sourceRef="StartEvent_1" targetRef="Task_1"/>
    <sequenceFlow id="SF_2" sourceRef="Task_1"       targetRef="Task_2"/>
    <sequenceFlow id="SF_3" sourceRef="Task_2"       targetRef="Task_4"/>
    <sequenceFlow id="SF_4" sourceRef="Task_4"       targetRef="ExclusiveGateway_1"/>
    <sequenceFlow id="SF_5" sourceRef="ExclusiveGateway_1" targetRef="Task_5" name="approved"/>
    <sequenceFlow id="SF_6" sourceRef="ExclusiveGateway_1" targetRef="Task_3" name="rejected"/>
    <sequenceFlow id="SF_7" sourceRef="Task_3"       targetRef="Task_4"/>
    <sequenceFlow id="SF_8" sourceRef="Task_5"       targetRef="EndEvent_1"/>
  </process>
</definitions>"""

    print("=" * 60)
    print("EXAMPLE: extract_metrics() + classify_complexity()")
    print("=" * 60)

    metrics = extract_metrics(example_xml)
    print("\nMetrics extracted from BPMN XML:")
    for k, v in metrics.items():
        print(f"  {k:>15}: {v}")

    label = classify_complexity(
        elements=metrics['elements'],
        lanes=metrics['lanes'],
        gateways=metrics['gateways'],
        data_objects=metrics['data_objects'],
    )
    print(f"\n  {'complexity':>15}: {label}")
    print()
    print("Note: data_objects=2 is correctly detected (unlike DOT format)")
    print("      lanes=2 is correctly detected from <lane> elements")


# ---------------------------------------------------------------------------
# 6.  CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Extract BPMN complexity metrics from BPMN XML in a JSONL file.')
    parser.add_argument('input', nargs='?',
                        help='Path to input .jsonl file. '
                             'If omitted, runs the built-in example.')
    parser.add_argument('-o', '--output',
                        help='Path for output .jsonl (default: <input>_complexity.jsonl)')
    parser.add_argument('-n', '--limit', type=int,
                        help='Only process the first N records')
    parser.add_argument('-i', '--index', type=int,
                        help='Only process the record at this 0-based index')
    args = parser.parse_args()

    if args.input is None:
        _run_example()
    else:
        process_jsonl(
            input_path=args.input,
            output_path=args.output,
            limit=args.limit,
            index=args.index,
        )


if __name__ == '__main__':
    main()