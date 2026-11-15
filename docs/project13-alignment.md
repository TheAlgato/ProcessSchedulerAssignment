# Project 13 alignment review

ProcessScope now targets CSE316 CA3 project 13, Real-Time Process Monitoring Dashboard. The supplied application already collected live OS readings but was titled as an AI performance analyzer and had no process-management controls. The revision adds that missing function and keeps existing analysis as additional scope.

## Requirements and changes

| Guideline requirement | Supplied project | Revised project and evidence |
| --- | --- | --- |
| Graphical dashboard | Streamlit dashboard already present. | Retained the existing dashboard and aligned its page and workspace titles with the assigned project. |
| Real-time process states | Actual psutil status, PID, name, and other readings. | Retained actual OS states and PID plus creation-time identity. The default refresh is now two seconds, selectable from one to sixty seconds. |
| CPU usage | Process and system CPU counters and charts already present. | Retained interval-based measurements, per-core diagnostics, and CPU search, sorting, and filters. |
| Memory consumption | Resident memory, memory percentage, and system charts already present. | Retained the process table, system memory display, and process memory trends. |
| Administrators can manage processes | Read-only. No action controls. | Added Suspend, Resume, and Terminate under Processes, an explicit enable switch, fixed-target review, typed-PID confirmation, cancellation, OS identity and permission checks, and a downloadable session action log. |
| Identify potential issues promptly | Recommendations and anomaly analysis already present. | Retained analysis and added warnings across all views for CPU at 90%, memory at 85%, and visible zombie processes. |
| Up to three students working on different modules | Technical stages documented, but team identities unavailable. | Defined three integrated team modules in the README and report. Actual names still need to be filled in. |
| Required report sections and appendices | No report matching the specified format. | Added `docs/report-body.md` and a report builder. `PROJECT_REPORT.md` includes the eight sections, flow diagram, AI-assisted breakdown, exact problem statement, and current source-code appendix. |
| GitHub, seven revisions, feature branches, tested merges | ZIP contains no Git history or verifiable repository link. | Added instructions and fields for real evidence. This requirement remains unverified until the team supplies its actual repository history. |
| Individual UMS submission, presentation, and viva | Not verifiable from source files. | Included the remaining submission tasks in the report and checklist below. |

## Verification completed

Command: `python -m unittest discover -s tests -v`.

Result on 13 November 2026: 36 tests discovered, 35 passed, one skipped. The original 23 tests passed. New coverage checks action dispatch, stale identity, protected targets, ownership, OS errors, onboarding, all four workspace views, disabled controls, wrong confirmation, cancellation, fixed-target confirmation, error logging, and visible warnings.

Dashboard interaction tests use fixed readings and mocked process-control calls. They verify application behavior without acting on existing programs. The real disposable-process test was skipped because this execution environment blocks macOS process enumeration with `Operation not permitted`. Real process enumeration and actions must still be verified on the team's local machine. The backend retains its protections when inspection is denied.

The local Streamlit server started successfully. Browser automation is disabled in this session, so visual layout was not reviewed in a browser. The automated dashboard tests rendered the app through Streamlit AppTest without application exceptions. The mechanical UI check reported no findings. Windows and Linux were not exercised on those operating systems.

`requirements-tested.txt` records the exact versions used for the checks. Install normal project dependencies through the supplied launcher or `requirements.txt`. The frozen file records this macOS Python 3.12 verification environment and may need platform-appropriate resolution elsewhere.

## Run and demonstrate the revised project

1. Extract the entire project folder. Keep the files together.
2. Use `Start Windows.bat`, `Start macOS.command`, or `python3 setup.py` from that folder. Python 3.10 or newer is required.
3. Complete the guide and choose session-only history for an initial demonstration.
4. Open Processes. Verify that the PID, state, CPU, and resident-memory readings correspond to the local machine. Allow at least two samples for CPU readings.
5. Start a disposable worker from a separate terminal, for example `python -c "import os,time; print(os.getpid(), flush=True); time.sleep(300)"`. Record its printed PID. Use the correct Python command for your computer.
6. Enable process controls, select only that worker PID, choose Suspend, review it, type its PID, and confirm. Check for a stopped state in a later reading. Resume it and verify that it continues. Finally terminate that same disposable worker and verify that it exits. Never use an application containing unsaved work for this demonstration.
7. Review Analysis and Diagnostics. Export a process snapshot or history and the session action log. Do not claim a warning or model result was measured unless it actually appeared during your run.
8. Run the test suite on the presentation machine. The disposable lifecycle test should run on an unrestricted POSIX environment. It is explicitly skipped on Windows; verify the actions there manually.

## Before submission

- Fill in team names, registration numbers, section, faculty, repository name, URL, and actual submission date in `docs/report-body.md`.
- Add at least seven genuine GitHub revisions and evidence of tested feature-branch merges. Existing numbered documentation files are not commits.
- Record local verification results and actual screenshots. Include the platform and package versions.
- Regenerate the report with `python tools/build_project_report.py` after every source change. Review the generated `PROJECT_REPORT.md`, then export it to the format accepted by the instructor.
- Review the guidelines' distinction between permitted AI-generated explanation and the requirement for student-written code. Discuss acceptable use of this assisted revision with the instructor and ensure every team member can explain their implementation.
- Each member submits the complete integrated report individually on UMS by the actual deadline and prepares for the presentation and viva.

## Source

The supplied `A1358141926_31_2026_CSE316 CA3 Project.pdf`, pages 1-3 for submission, report, team, and GitHub requirements, and page 6 for project 13. The assignment number in the PDF's filename does not change the problem number assigned by the user.
