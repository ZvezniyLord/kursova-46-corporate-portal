# WBS / Calendar source table

This is an initial work-package register, not an approved calendar. Detailed task dates, durations, predecessors, roles, rates and EVM values are generated as an explicitly synthetic educational scenario in `build/build_dataset.py` and the CSV outputs below; they are not enterprise facts or an approved baseline. No `.mpp` is represented here.

| WBS | Work package | Requirement | Output | Depends on | Owner role | Duration/calendar |
|---|---|---|---|---|---|---|
| 1.1 | Charter, scope, SMART | REQ-009 | Charter | — | AG5 | OPEN |
| 1.2 | Stakeholders, requirements, AC | REQ-001…010 | Registers/traceability | 1.1 | AG5 | OPEN |
| 1.3 | Method, RACI and communication | — | Governance plan | 1.1 | AG5 | OPEN |
| 2.1 | Dashboard | REQ-002 | Prototype screen | 1.2 | O3 | OPEN |
| 2.2 | Announcements | REQ-003 | Prototype screen | 1.2 | O3 | OPEN |
| 2.3 | Document search | REQ-004 | Prototype screen | 1.2 | O3 | OPEN |
| 2.4 | Directory | REQ-005 | Prototype screen | 1.2 | O3 | OPEN |
| 2.5 | Role concept and limitations | REQ-006,008 | UI/notes | 1.2 | O3 | OPEN |
| 3.1 | Accessibility and smoke tests | REQ-007 | Verification log | 2.1…2.5 | O4/O3 | OPEN |
| 3.2 | Risk/privacy/change controls | REQ-008 | Controls | 1.2 | AG5/O4 | OPEN |
| 3.3 | UAT test cases | — | UAT plan | 1.2, 2.1…2.5 | O4 | OPEN |
| 4.1 | Schedule/resources/cost/Baseline | REQ-009 | Native MPP only if verified | 1.1…1.3 | O1 | OPEN |
| 4.2 | Backlog/Sprint planning | REQ-010 | Jira only if verified; else CSV proposal | 1.2 | O2 | OPEN |
| 4.3 | Educational EVM model | — | Reproducible PV/EV/AC table | 4.1 | O1 | OPEN |
| 5.1 | Literature source verification | — | Source matrix | 1.1 | AG5 | OPEN |
| 5.2 | Coursework manuscript | — | Editable DOCX | All evidence | AG5 | OPEN |
| 5.3 | DOCX/PDF quality review | — | Quality report | 5.2 | AG5 | OPEN |
