# Project 13: requirements and black box acceptance review

Review date: 15 November 2026 (India). Application: ProcessScope.

## 1. Scope and verdict

The report structurally matches the assignment and describes functionality aligned with Project 13. Submission readiness is conditional: real team/repository evidence is missing and live OS behavior must be demonstrated on the presentation machine. A description of a feature is not evidence that the feature passed a test.

The assignment PDF was read in full (10 pages). Pages 1-4 provide the general instructions, report format and evaluation; page 6 contains Project 13. The other project statements are alternative assignments. The filename's `31` does not change the user's assigned Project 13. AI anomaly detection and forecasting are optional additions here.

The PDF is a requirements source for this review. Its embedded example AI prompt is assignment content, not a separate request to generate an implementation. This review adds verification and documentation; it does not rewrite the student's application.

## 2. Required behavior and traceability

| ID | Project 13 requirement (PDF page 6) | Acceptance condition | Evidence and limits |
| --- | --- | --- | --- |
| R1 | Graphical dashboard | Open the dashboard; see readable resource metrics and navigate views without errors. | BB01 exercises rendered Streamlit UI. Browser appearance remains a manual check. |
| R2 | Real-time information | While active, subsequent samples update displayed data; pause keeps the last reading; resume updates again. | BB15 verifies updates on explicit AppTest reruns with controlled inputs. M01 must verify browser timer scheduling and live OS sampling. |
| R3 | Process states | Process table shows PID, name and the state provided by the OS; transitions and exits appear on later readings. | BB02 checks displayed state; BB07 checks empty input. M02/M05 cover actual transitions. |
| R4 | CPU usage | Show system and per-process CPU; handle initial unavailable readings and multicore values above 100%. | BB01/02/06 check displayed values. M03 checks measurement accuracy against a native OS tool. |
| R5 | Memory consumption | Show system memory and per-process percent and resident memory with clear units. | BB01/02 check percent and MiB conversion. M04 checks live accuracy. |
| R6 | Administrators can manage processes efficiently | Select a target, request a management action, see the outcome, and observe actual OS state changes. | BB12/13/14 check confirmation/dispatch and visible denial. Existing lifecycle test and M05 cover actual OS effects. |
| R7 | Identify potential issues promptly | Show pressure/state warnings on a fresh sample and identify a process to investigate where appropriate. | BB08/09/10/11 verify warning boundaries, visibility and advice. M06 measures live detection delay. |

The assignment does not specify numeric thresholds, a fixed refresh deadline, exact management actions, remote administration, authentication, ML or a black box test section. The report's 2-second default, 90% CPU/85% memory warnings, suspend/resume/terminate workflow, confirmation rules, search/filter thresholds and local-account restriction are application-level commitments. Tests below verify those commitments without treating them as extra faculty requirements. Clarify with faculty if managing processes owned by other accounts is expected: this application explicitly blocks that even when launched by an elevated account.

## 3. General guideline compliance

| Requirement | Finding | Remaining action |
| --- | --- | --- |
| One integrated group project; at most 3 members on different modules | Three integrated modules are described. Member assignments are placeholders. | Fill actual names, registration numbers and responsibilities; do not invent members. |
| Report sections 1-8 | Overview, module breakdown, functionalities, technology, flow diagram, GitHub tracking, conclusion/future scope and references are present. | Keep these sections when exporting the final report. |
| Appendix A: detailed AI elaboration/breakdown | Goals, modules, examples, technologies and execution plan are present. | Team should review the explanation against its own work. |
| Appendix B: assigned problem statement | Correct Project 13 title and description are present. | Retain the exact assigned statement. |
| Appendix C: complete solution/code | Generated report contains the current source appendix. | Rebuild after changes; verify appendix and code agree. |
| GitHub repository and at least 7 revisions with clear messages | Repository and commit table remain placeholders; no `.git` directory exists in the supplied project folder. Numbered documentation does not establish commits. | Supply the actual repository URL, 7 or more genuine revisions and dated evidence. |
| Feature branches; merge to main after testing | Not verifiable from this archive. | Provide real branches/merge history and test evidence. |
| Individual online UMS upload before deadline | Cannot be established from project files. No exact deadline appears in the PDF. | Each student uploads the complete integrated report by the faculty's actual deadline. |
| Presentation and viva | Preparation required; not verifiable from source. | Explain the implementation, challenges and test evidence. Evaluation is 15 marks AI evaluation plus 15 presentation/viva. |
| Student-written implementation; no copied peer/internet/AI code | Authorship cannot be certified by functional tests or an archive. The PDF explicitly permits AI explanation in Appendix A while requiring students to write their implementation. | Retain truthful attribution and be able to explain personal contributions. |

No marks or unconditional compliance certificate can be inferred from passing automated tests.

## 4. Black box test design

Test oracle: the assignment's required behavior plus the report's stated user-facing behavior. Techniques: equivalence partitioning (valid/invalid search and confirmations), boundary value analysis (usage thresholds), state transitions (setup, pause, resume, review, cancel, confirm), and decision combinations (warnings across views).

`tests/test_black_box_requirements.py` drives the real dashboard through public Streamlit AppTest widgets and checks displayed metrics, tables and messages. It does not call application helper functions. OS collection and process-action adapters are substituted with controlled inputs so cases are repeatable and no existing user process receives signals. This is interface-level acceptance testing with substituted dependencies, not a fully live end-to-end black box run. The existing backend/unit tests are supporting evidence and are not relabeled as black box tests.

Preconditions: install `requirements.txt`; use session-only history; standard fixtures provide PID 300 (Alpha-worker: 19.9% CPU, 4.9% memory, 1 MiB RSS), PID 301 (Beta-worker: 20% CPU, 5% memory, 2 MiB RSS), and PID 302 (Gamma-worker: 145% CPU, 6% memory, 3 MiB RSS). Baseline system CPU is 20%, RAM is 30%.

| Case | Requirements | Inputs / user steps | Expected observable result |
| --- | --- | --- | --- |
| BB01 | R1, R4, R5 | Complete the welcome guide with session-only history; open all 4 views. | CPU 20.0%, RAM 30.0%, default interval 2 seconds; controls off; no UI exception. |
| BB02 | R3, R4, R5 | Supply a stopped Alpha-worker; open Processes. | PID/name/state preserved; 19.9% CPU, 4.9% memory and 1 MiB RSS; Gamma's 145% CPU preserved. |
| BB03 | R1 (report extension) | Search `ALPHA`, `301`, then `no-such-process`. | Case-insensitive name match returns 300; PID match returns 301; no-match message without crash. |
| BB04 | R4, R5 (report extension) | Apply high CPU and high memory filters. | Exclude 19.9%/4.9%; include exact 20%/5% boundaries and higher values. |
| BB05 | R1 (report extension) | Sort by CPU, Memory, Name, PID. | Usage sorts descending; name/PID ascending with correct row identity. |
| BB06 | R4 | Supply unavailable system/process CPU and unavailable disk I/O. | System says Warming up; process CPU and I/O remain missing, not invented zero readings; no crash. |
| BB07 | R1, R3 | Supply zero visible processes. | Process count 0; explicit empty-result message; no selectable process or crash. |
| BB08 | R7 | Supply CPU 89.9%, 90.0%, 90.1% independently. | No pressure warning below 90%; warning and High status at/above 90%. |
| BB09 | R7 | Supply RAM 84.9%, 85.0%, 85.1% independently. | No pressure warning below 85%; warning and High status at/above 85%. |
| BB10 | R7 | Supply CPU 90% and one zombie; open all views. | Pressure warning and count of one zombie on every view. |
| BB11 | R7 | Supply CPU 95%, RAM 87%; open Analysis. | Advice names Gamma-worker PID 302 as largest CPU/memory consumer; no automatic process action. |
| BB12 | R6 | For each of Suspend, Resume, Terminate: enable, select 300, review, type 300, confirm, rerun. | No request before confirmation; exactly one matching request after confirmation; visible result; rerun does not duplicate request. |
| BB13 | R6 | Review Terminate; submit blank, 301, abc, -1; then Cancel. | Every invalid confirmation shows mismatch; no request; Cancel removes confirmation. |
| BB14 | R6 | Confirm a request whose OS adapter reports access denied. | Visible denial reason and no UI exception. This does not prove real OS permission enforcement. |
| BB15 | R2 | Set 1-second interval and apply; supply 42% CPU, wait >1 second and rerun; pause; supply 55%, wait/rerun; resume. | 42% appears after refresh; remains 42% while paused with Paused indicator; resume displays 55%. |

The fixed-target, disable-controls, PID reuse, protected-process and ownership cases already in `test_dashboard.py` and `test_process_control.py` supplement this matrix. Their action mocks prove dispatch/protection logic under test inputs, not actual process execution effects.

## 5. Live machine acceptance cases (not yet executed)

Use only a disposable worker created for the test. Record OS, account, Python/package versions, observed result, screenshot/log and time for each case. Keep pending cases marked NOT RUN until evidence exists.

| Case | Steps and test input | Expected result / acceptance criterion | Status |
| --- | --- | --- | --- |
| M01 - Browser refresh | Start the dashboard normally, default 2-second interval. Observe timestamps through at least 3 updates without clicking. Pause, wait 2 intervals, resume. Repeat at 1 and 60 seconds using Apply settings. | Timestamps/data update automatically while active, remain fixed while paused, resume afterward. Record actual cadence; no hard deadline was set by faculty. | NOT RUN |
| M02 - Real process identity | Launch a temporary sleeping worker and record its PID. Search it and compare with Activity Monitor/Task Manager/ps. Allow at least two samples. | Correct PID, name and OS state. After exit it disappears on a subsequent sample without crash. State names can differ between platforms. | NOT RUN |
| M03 - Live CPU | Observe idle worker, then run a disposable CPU workload on one core. Compare similar sample windows with a native monitor. | CPU rises/falls with workload; account for per-process one-core=100% versus system-wide scaling. Record tolerance before comparison; suggested approximate tolerance is 10 percentage points for matched windows, not a faculty requirement. | NOT RUN |
| M04 - Live memory | Observe a disposable worker before/after allocating a bounded buffer, for example 32 MiB if available. Compare RSS with native monitor. | Reported resident memory increases and has correct units. Record values; allocators/OS accounting need not equal buffer size exactly. | NOT RUN |
| M05 - Actual management | Select only the temporary worker; confirm Suspend, verify stopped state independently; confirm Resume, verify it runs; confirm Terminate, verify actual exit. | Correct process receives each action. A Request sent message alone is insufficient proof of exit. Record the PID and each OS observation. | NOT RUN |
| M06 - Prompt issue detection | Observe a safe, naturally occurring threshold breach or use a controlled demonstration environment; record sample time and displayed warning time. Let pressure clear. | Warning appears on the first displayed sample satisfying 90% CPU/85% RAM; clears on a later below-threshold sample. Do not fill host RAM merely to trigger an alert. | NOT RUN |
| M07 - Exit during confirmation | Review an action for the temporary worker; end it externally before confirmation; then confirm. | Clear exited/stale target failure, no other process affected, dashboard remains usable. | NOT RUN |
| M08 - Downloads and persistence | Download filtered process CSV, history CSV, diagnostics JSON, action log; open/parse each. Separately choose local history, collect, restart with local history. | Files contain the displayed scope and correct values; saved history survives restart. Session-only choice leaves prior saved files unchanged. | NOT RUN |
| M09 - Platform and permissions | Repeat M01-M05 on every claimed deployment OS. On a suitable test machine attempt a denied/protected target through the normal UI. | Supported operations work with current account permissions; denied requests show clear failure; no elevation or unintended target action. | NOT RUN |
| M10 - Visual usability | Open in the intended browser at desktop and small window sizes; try light mode, sidebar and all views. | Labels, controls and confirmation text remain readable and reachable; no overlap/clipping. AppTest is not pixel-level browser verification. | NOT RUN |

## 6. Reproduce and record results

From the project directory:

```sh
python -m unittest discover -s tests -p test_black_box_requirements.py -v
python -m unittest discover -s tests -v
python tools/build_project_report.py
```

The execution record and exact resolved packages for this review are saved under `docs/verification/`. Earlier claims in the alignment document dated 13 November describe a different environment and must not be treated as today's results.

### Actual results: 15 November 2026

Environment: macOS 26.6.2 arm64, Python 3.13.3. Dependencies were installed from the supplied `requirements.txt` into an isolated temporary environment. Resolved versions are preserved in [the package record](verification/2026-11-15-packages.txt); the earlier `requirements-tested.txt` was preserved.

| Run | Actual outcome | Evidence |
| --- | --- | --- |
| BB01-BB15, including threshold and action subcases | All 15 test methods passed; no acceptance failure found in the exercised controlled-input behavior. | [Full test log](verification/2026-11-15-unittest.log), methods prefixed `test_BB`. |
| Full suite under sandbox | 51 tests discovered: 50 passed, 1 skipped, 0 failures/errors; 9.954 seconds. Skip reason: OS process inspection was denied by the sandbox. | [Full test log](verification/2026-11-15-unittest.log). |
| Process-control suite outside sandbox | 7 of 7 passed, including actual suspend, observed stopped state, resume, and terminate of the child created by the lifecycle test. No existing user program was targeted. | [Local process-control log](verification/2026-11-15-process-control-local.log). |

The successful local lifecycle run resolves the sandbox skip for that backend test on this macOS machine. It does not complete M05's browser-to-OS interaction demonstration. M01-M10 remain pending manual acceptance; none is labeled passed. Windows/Linux remain untested.

The log contains Streamlit warnings about `use_container_width` deprecation and bare-mode script context. These did not fail the test run; future library compatibility and browser layout are separate from these acceptance results. No production application behavior was changed during this review.

## 7. Submission actions

1. Complete actual team, section, faculty, date and repository details in `docs/report-body.md`.
2. Replace all seven commit placeholders with genuine GitHub revision and tested-merge evidence.
3. Complete the live acceptance cases above and attach actual observations/screenshots. Do not mark planned tests as passed.
4. Rebuild `PROJECT_REPORT.md`, including its complete current code appendix, and inspect the final export.
5. Submit individually on UMS by the actual announced deadline and prepare to explain the required monitoring/management workflow in the viva.
