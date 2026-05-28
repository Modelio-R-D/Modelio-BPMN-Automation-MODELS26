# Scenario 49

**Complexity:** Complex

## Natural-language description

A customer brings in a defective computer and the CRS checks the defect and hands out a repair cost calculation back.
If the customer decides that the costs are acceptable, the process continues, otherwise she takes her computer home unrepaired.
The ongoing repair consists of two activities, which are executed, in an arbitrary order.
The first activity is to check and repair the hardware, whereas the second activity checks and configures the software.
After each of these activities, the proper system functionality is tested.
If an error is detected another arbitrary repair activity is executed, otherwise the repair is finished.

## Ground-truth structural metrics

- lanes: 1
- elements: 18
- gateways: 6
- flows: 20
- data_objects: 0
- data_assoc: 0
