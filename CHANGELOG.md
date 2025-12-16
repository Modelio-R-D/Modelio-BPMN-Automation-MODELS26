# Changelog

All notable changes to this project will be documented in this file.

## [v3.1] - December 2025

### Improved
- **Data object positioning**: Data objects now positioned below their source task (determined from data associations)
- **Y-offset support in layout**: Layout entries can now use `(column, y_offset)` tuple format for vertical stacking
  - `"Element": 5` - column 5, default Y position
  - `"Element": (5, 70)` - column 5, 70px below default position
- **Default config values**: Updated `DATA_OFFSET_X=90` (near task right edge), `DATA_OFFSET_Y=10` (small gap below task)

### Documentation
- **Y-offset rules clarified**: Positive y_offset moves elements DOWN within lane
- **Complete element type reference**: All 30+ element types documented with descriptions
- **Sequential vs parallel guidance**: Clear rules for when to use y_offset (parallel branches only)

---

## [v3.0] - December 2025

### Major Features
- **BPMN Export/Import**: New `BPMN_Export.py` macro to export existing diagrams to Python configuration
  - Captures all elements with exact positions and sizes
  - Uses lane-relative Y coordinates for proper positioning
  - Supports diagram cloning and migration between projects

- **Lane-Relative Positioning**: New positioning mode for exact diagram recreation
  - Elements format: `("Name", TYPE, "Lane", x, y_offset, width, height)`
  - `y_offset` is relative to lane top, not absolute Y coordinate
  - Handles Modelio's dynamic lane resizing automatically

- **New Element Types**:
  - Tasks: `SCRIPT_TASK`, `BUSINESS_RULE_TASK`, `SEND_TASK`, `RECEIVE_TASK`, generic `TASK`
  - Gateways: `INCLUSIVE_GW`, `COMPLEX_GW`, `EVENT_BASED_GW`
  - Events: `SIGNAL_START`, `CONDITIONAL_START`, `SIGNAL_END`, `TERMINATE_END`, `ERROR_END`
  - Intermediate Events: `INTERMEDIATE_CATCH`, `INTERMEDIATE_THROW`, `MESSAGE_CATCH`, `MESSAGE_THROW`, `TIMER_CATCH`, `SIGNAL_CATCH`, `SIGNAL_THROW`

### Changed
- **Backward Compatible**: Column-based positioning still works (3-tuple elements format)
- **Dynamic Imports**: Gracefully handles missing element types in older Modelio versions

### Files
- `BPMN_Helpers.py` - Enhanced helper library with new positioning and element types
- `BPMN_Export.py` - New export macro for diagram extraction

---

## [v2.5] - December 2025

### Documentation
- **Clarified BPMN data association rules**: Events CAN have data associations, Gateways CANNOT
  - Start Events: Output associations only (Start -> Data)
  - End Events: Input associations only (Data -> End)
  - Gateways: NEVER allowed - causes E205 orphan error
- Added detailed table and examples showing valid/invalid data associations

---

## [v2.4] - December 2025

### Changed
- **Data objects simplified**: Removed `position` parameter - data objects are now always placed below the lane center
  - Format changed from `(name, lane, column, "above|below")` to `(name, lane, column)`
  - Simplifies configuration and provides consistent visual layout

---

## [v2.3] - December 2025

### Changed
- **Data associations simplified**: Removed `direction` parameter - now auto-detected based on element types
  - Format changed from `(source, target, "input|output")` to `(source, target)`
  - Direction is automatically determined: Task→DataObject or DataObject→Task

---

## [v2.2] - December 2025

### Fixed
- **Data Association semantics**: Corrected `StartingActivity`/`EndingActivity` and `SourceRef`/`TargetRef` settings for proper BPMN compliance
  - `output`: Sets `StartingActivity = Task`, `TargetRef = DataObject`
  - `input`: Sets `EndingActivity = Task`, `SourceRef = DataObject`

### Changed
- **Lane-by-lane positioning**: Data objects are now positioned lane-by-lane (top to bottom) to handle Modelio's automatic lane expansion when data objects extend beyond boundaries

---

## [v2.1] - December 2025

### Added
- **Data Objects**: New `DATA_OBJECT` element type for representing documents and data in processes
- **Data Associations**: Connect tasks to data objects
- `data_objects` configuration section: `(name, lane, column)`
- `data_associations` configuration section: `(source, target)`
- New configuration options:
  - `DATA_WIDTH` (default: 40) - Width of data objects
  - `DATA_HEIGHT` (default: 50) - Height of data objects
  - `DATA_OFFSET_X` (default: 20) - X offset from column center
  - `DATA_OFFSET_Y` (default: 80) - Y offset from lane center

### Documentation
- Updated `CLAUDE_INSTRUCTIONS.md` to v2.1 with data object examples
- Updated `API_REFERENCE.md` with complete data object/association documentation

---

## [v2.0] - December 2025

### Added
- **Two-file architecture**: Separates reusable helper library from process configuration
- `BPMN_Helpers.py` - Standalone helper library to install once in Modelio macros folder
- `createBPMNFromConfig()` - Single function to create entire process from configuration dict
- Element type constants (`START`, `END`, `USER_TASK`, `SERVICE_TASK`, `MANUAL_TASK`, `EXCLUSIVE_GW`, `PARALLEL_GW`, `MESSAGE_START`, `MESSAGE_END`, `TIMER_START`)
- Configuration-based approach with `CONFIG` dictionary
- Support for Claude, ChatGPT, Gemini, and LM Studio/Qwen

### Changed
- AI now generates ~50-100 lines of configuration instead of 500+ lines of full scripts
- Faster generation, fewer syntax errors, easier debugging
- Process scripts use `execfile()` to load helper library

### Documentation
- Added `docs/QUICK_START.md` - Step-by-step setup guide
- Added `docs/API_REFERENCE.md` - Complete configuration reference
- Added `docs/APPROACHES.md` - Comparison of single-file vs two-file approaches

---

## Single-File Version History

The following versions used a single-file approach where all helper functions were included inline in each generated script.

## [v0.9.1] - December 2025

### Added
- Guards for gateway conditions (displayed on sequence flows)

## [v0.9.0] - December 2025

### Added
- Configurable task dimensions (`TASK_WIDTH`, `TASK_HEIGHT`)
- Tasks are resized to ensure text fits properly
- Increased default `SPACING` to 150 for better readability

### Changed
- Events and gateways keep their original dimensions
- Log output now shows element dimensions

## [v0.8.3] - December 2025

### Fixed
- **Critical fix**: Manual unmask now works correctly by placing elements at the Y position inside their lane
- Unmask at (0,0) was failing - must unmask inside the correct lane

### Added
- Lane Y position calculation for manual unmask
- Detailed unmask logging with lane name and Y position

## [v0.8.2] - December 2025

### Added
- Manual unmask fallback for elements not auto-unmasked
- Automatic retry for missing elements after wait timeout

## [v0.8.1] - December 2025

### Added
- Detailed attempt logging during wait phase
- Shows found/missing elements count per attempt
- Lists missing element names (truncated to 12 chars)

## [v0.8.0] - December 2025

### Added
- Discovery: Modelio auto-unmasks elements when diagram is created
- Wait mechanism to check for element availability
- No longer need to manually call unmask() for initial display

### Changed
- Removed explicit unmask calls for all elements
- Added polling loop to wait for elements

## [v0.7.0] - November 2025

### Added
- Detailed reposition logging
- Lane change detection with before/after comparison
- `*** LANE CHANGED ***` markers in output

## [v0.6.0] - November 2025

### Added
- Lane change detection during repositioning
- Comparison of lane bounds before and after each move

## [v0.5.0] - November 2025

### Fixed
- Read lane Y positions once before repositioning
- Use fixed Y values to avoid lane drift

## [v0.3.0] - November 2025

### Added
- Complete BPMN template with all helper functions
- Support for all common BPMN element types
- Message and Timer start/end events
- `createBPMNDiagram()` function with automatic layout

## [v0.2.0-single] - November 2025

### Added
- Initial template structure
- Basic BPMN element creation functions
- Lane and flow support

---

## Key Discoveries

### Data Association Semantics (v2.2+)

BPMN data associations have specific semantics (auto-detected based on element types):

| Direction | Arrow | BPMN Properties |
|-----------|-------|-----------------|
| Task → DataObject | Task produces data | `StartingActivity=Task`, `TargetRef=Data` |
| DataObject → Task | Task consumes data | `SourceRef=Data`, `EndingActivity=Task` |

Typical pattern for data flowing between tasks:
```
Task A --> Data Object --> Task B
```

### Lane Expansion with Data Objects (v2.2)

When data objects are positioned below tasks, they may extend beyond lane boundaries. Modelio auto-expands lanes to accommodate this, which shifts subsequent lanes down. Solution: position data objects lane-by-lane and re-read lane coordinates after each lane.

### Auto-Unmask Behavior (v0.8.0)

Modelio automatically unmasks elements when a diagram is created, but:
- Auto-unmask is **non-deterministic** - sometimes all elements appear, sometimes only partial
- Waiting **does not reliably help** - Modelio appears to freeze in some state
- Solution: Quick check (3 attempts, 50ms) then manual unmask fallback

### Lane-Aware Unmask (v0.8.3)

Manual unmask must be done at the correct Y position:

```python
# WRONG - will fail
diagramHandle.unmask(elem, 0, 0)

# CORRECT - inside the lane
diagramHandle.unmask(elem, 100, laneY[laneName])
```

### Two-File Benefits (v2.0)

| Metric | Single-File | Two-File |
|--------|-------------|----------|
| Lines per script | 500-700 | 50-150 |
| AI generation time | ~45 sec | ~15 sec |
| Syntax error rate | ~30% | ~0% |
| Bug fix effort | Edit every file | Edit once |