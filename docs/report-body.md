# Real-Time Process Monitoring Dashboard

CSE316 Operating Systems, CA3, Project 13  
Application: ProcessScope  
Institution: Lovely Professional University

Team members and registration numbers: [Enter actual details, maximum three students]  
Section and faculty: [Enter actual details]  
GitHub repository name and URL: [Enter the team's actual repository]  
Submission date: [Enter actual submission date]

## 1. Project overview

ProcessScope displays real-time operating-system process states, CPU utilization, and memory consumption in a graphical dashboard. Administrators can inspect processes and explicitly suspend, resume, or terminate processes owned by the account running the application. Warnings and recommendations help users investigate resource pressure and zombie processes.

The dashboard runs locally. Its monitoring module reads actual OS counters through psutil. It refreshes every two seconds by default, with selectable intervals from one to sixty seconds. A timestamp and paused indicator show the age of each displayed observation. This is periodic real-time monitoring, not a hard real-time system with guaranteed deadlines.

The required scope is monitoring, process management, and issue identification. Existing anomaly detection, resource forecasts, network diagnostics, disk metrics, and exports remain additional functionality. The app does not replace an operating-system administrator or automatically terminate workloads.

## 2. Module-wise breakdown

Assign one team member to each module and replace the entries below with actual responsibilities.

| Module | Responsibility and code | Assigned member |
| --- | --- | --- |
| Collection and process management | `modules/process_monitor.py`, `modules/system_monitor.py`, and `modules/process_control.py`. Read process and system counters, derive interval CPU and transfer rates, and apply confirmed OS process actions. | [Member 1] |
| Analysis and storage | `modules/anomaly_detector.py`, `modules/resource_predictor.py`, `modules/recommendation_engine.py`, `modules/process_history.py`, and `database/db_manager.py`. Maintain history, detect resource pressure and unusual profiles, and produce optional forecasts. | [Member 2] |
| Dashboard, visualization, and reporting | `dashboard.py`, `visualization/`, launchers, `tools/build_project_report.py`, and documentation. Present readings and controls, export results, and integrate and document the application. | [Member 3] |

The modules form one integrated application. Tests cover their observable behavior and their dashboard integration.

## 3. Functionalities

### Live monitoring

The process table includes PID, name, actual OS state, CPU percentage, memory percentage, resident memory in MiB, threads, age, and available disk I/O. CPU is computed from changes in cumulative user and system time divided by elapsed monotonic time. A process using multiple cores can exceed 100%. Newly observed processes need a second sample for CPU usage.

System readings include CPU utilization, memory usage and capacity, filesystem capacity, per-core CPU, swap, and supported network and disk transfer rates. Process identity consists of PID and creation time so that a reused PID does not inherit the previous process's trend.

Users can search by name or PID, filter high usage or unusual profiles, sort the table, inspect up to 120 recent process readings, and export CSV or JSON snapshots. Collection can be paused. History can remain in memory or be stored in SQLite.

### Process management

Controls start disabled. To act, enable controls, select a process, choose Suspend, Resume, or Terminate, and review the action. The confirmation retains the selected identity and action independently of subsequent live-table or selection changes. The user must type the displayed PID before sending the request. Cancel or a mismatched PID sends no request.

The control module rechecks PID and creation time, running state, ownership, and protected processes. It blocks PID 0/1, the dashboard and its ancestors, other accounts' processes, and exited or zombie targets. The operating system can still deny access, and the app reports the failure without attempting elevation. Suspending stops execution until resumed. On POSIX, Terminate sends a termination request. On Windows it forces the process to end. A sent request does not prove that the process exited, so users check the next reading.

The most recent 50 action outcomes stay in the browser session and can be downloaded as CSV. This session log is not a permanent or tamper-proof audit record.

### Issue identification and additional analysis

CPU usage at or above 90% and memory usage at or above 85% produce visible warnings on all workspace views. Visible zombie processes also produce a warning. Recommendations name the largest visible CPU or memory consumer when system pressure is high. Disk capacity at 90% and swap at 85% produce investigation advice in Overview and Analysis.

Isolation Forest detects unusual CPU and memory profiles relative to other processes in the same snapshot. It requires at least 20 usable processes. An unusual profile alone does not establish a fault.

The optional five-minute forecast uses historical pairs and compares a Random Forest model with a persistence baseline. Independent validation requires enough time-separated history. With insufficient evaluation history, the forecast identifies its baseline as unvalidated. Forecasts do not trigger process actions.

## 4. Technology used

Programming language: Python 3.10 or newer. The revised package was tested with Python 3.12.

Libraries and tools:

- psutil for operating-system counters and process-control APIs.
- Streamlit for the graphical dashboard, forms, session state, and periodic refresh.
- pandas and NumPy for tabular data and numerical operations.
- Plotly for resource charts.
- scikit-learn for optional anomaly detection and forecasting.
- SQLite through Python's standard library for local history.
- unittest, unittest.mock, and Streamlit AppTest for automated verification.
- Git and GitHub for revision tracking, to be maintained by the team.

`requirements.txt` defines installation requirements. `requirements-tested.txt` records the exact package versions used in this verification environment. Windows and Linux behavior still needs verification on those operating systems.

## 5. Flow diagram

```text
Start local dashboard
        |
Allow monitoring -> Choose history storage -> Open dashboard
        |
Read process and system counters from the operating system
        |
Compute interval CPU and I/O rates
        |
Save chosen history -> Evaluate pressure and optional analysis
        |
Display states, CPU, memory, warnings, charts, and timestamp
        |
        +---- Refresh interval elapsed? ---- Yes ---- Read next sample
        |
        +---- Process management enabled?
                         |
                    Select process
                         |
                    Review fixed target and action
                         |
                    Type matching PID and confirm
                         |
                    Recheck identity, ownership, and protections
                         |
                +--------+---------+
                |                  |
             Allowed          Blocked or exited
                |                  |
        Send OS action       Show failure reason
                |                  |
                +------ Log outcome ------+
                         |
                    Read next sample
```

Cancel and a mismatched confirmation never send a process-control request. OS permission errors are reported as failed outcomes.

## 6. Revision tracking on GitHub

Repository name: [Enter actual repository name]  
GitHub link: [Enter actual repository URL]

The supplied ZIP does not contain `.git` history. No commit count, repository ownership, or branch-merge history can be verified from that archive. The numbered files under `docs/` describe development stages and are not evidence of Git commits.

The guidelines require at least seven genuine revisions with clear commit messages, feature branches, testing, and merges into the main branch. Record actual work below. Do not invent commit hashes or rewrite dates to imply past development.

| Revision | Actual commit hash | Change and validation | Feature branch or merge |
| --- | --- | --- | --- |
| 1 | [Actual hash] | [Actual change and check] | [Actual branch] |
| 2 | [Actual hash] | [Actual change and check] | [Actual branch] |
| 3 | [Actual hash] | [Actual change and check] | [Actual branch] |
| 4 | [Actual hash] | [Actual change and check] | [Actual branch] |
| 5 | [Actual hash] | [Actual change and check] | [Actual branch] |
| 6 | [Actual hash] | [Actual change and check] | [Actual branch] |
| 7 | [Actual hash] | [Actual change and check] | [Actual branch] |

Run `python -m unittest discover -s tests -v` before merging a feature. Use `git log --oneline --all --graph` and actual GitHub commit and pull-request links as revision evidence. Each student uploads the complete integrated report individually on UMS and takes part in the presentation and viva.

## 7. Conclusion and future scope

The revised application implements project 13's required dashboard, live process and resource monitoring, explicit process management, and prompt issue identification. The primary alignment change is the addition of process controls to a previously read-only analyzer, together with project-specific naming and documentation.

The requirement-by-requirement review and black box acceptance matrix are recorded in `docs/black-box-testing.md` and included as supplemental Appendix D. On 15 November 2026, all 15 new interface acceptance tests passed. The full suite passed 50 of 51 tests, with the real-process lifecycle test skipped under sandbox restrictions. A separate local process-control run outside the sandbox passed all 7 tests, including the real disposable-process lifecycle; its evidence is in `docs/verification/2026-11-15-process-control-local.log`. Controlled-input dashboard tests do not prove live OS measurement accuracy or automatic browser refresh; the remaining live-machine acceptance cases in Appendix D must be completed on the presentation machine. The older `docs/project13-alignment.md` preserves the 13 November review.

Future work can include configurable alert thresholds, history retention limits, durable authenticated action auditing, and platform-specific validation. Remote administration would require a separate authentication and deployment design. The current localhost binding is part of the application's local-use scope.

Before submission, fill in the real team and repository details, add revision evidence, review the implementation with the team, capture actual local screenshots, and export the completed report to the format accepted by the instructor.

## 8. References

1. Lovely Professional University. CSE316 Operating Systems, Academic Task 3 project guidelines, supplied PDF `A1358141926_31_2026_CSE316 CA3 Project.pdf`. Submission and report requirements appear on pages 1-3. Project 13 appears on page 6.
2. psutil API reference. https://psutil.io/api/ . Process identity, counters, suspend, resume, terminate, and permissions.
3. Streamlit execution flow. https://docs.streamlit.io/develop/api-reference/execution-flow/st.fragment . Periodic dashboard fragments.
4. Streamlit application testing. https://docs.streamlit.io/develop/api-reference/app-testing . AppTest.
5. Python documentation, sqlite3. https://docs.python.org/3/library/sqlite3.html . Local database persistence.
6. scikit-learn documentation. https://scikit-learn.org/stable/ . Isolation Forest and Random Forest estimators.
7. Plotly Python documentation. https://plotly.com/python/ . Interactive resource charts.

## Appendix A. AI-generated project elaboration and breakdown

This appendix provides the AI-assisted project explanation requested by the guidelines. The team must review it against the implemented behavior and understand the implementation for the viva. The guidelines also require student-written implementation and prohibit copying AI-generated code. Confirm the acceptable use of this assisted revision with the instructor.

### Project goals, expected outcomes, and scope

Build a local graphical process monitor that answers three questions: what is running, which processes consume resources, and which process needs attention or a deliberate management action? The expected result is an integrated dashboard that updates real process states, CPU, and memory, handles unavailable readings, and confirms user-selected process actions. The required outcome does not depend on an AI forecast.

### Module functionalities and examples

The collection and management module measures actual process and system counters. For example, a worker consuming one full CPU core approaches 100% process CPU. If the user pauses that worker through Suspend, a subsequent observation can show a stopped state. Resume allows execution to continue. The identity check prevents a different process from receiving the action after PID reuse.

The analysis and storage module preserves chosen history, identifies pressure, and explains investigation steps. For example, system memory at 87% exceeds the 85% threshold and prompts a review of the largest visible memory consumer. Optional statistical analysis supplements these direct checks.

The dashboard module turns those results into searchable tables, charts, warnings, process inspection, and confirmed controls. For example, reviewing Suspend for PID 300 and later selecting PID 301 does not change the target of the pending confirmation. Exports support documentation and debugging.

### Technology recommendations

Use the existing Python, psutil, Streamlit, and SQLite implementation for the required local monitoring workflow. Retain pandas and Plotly for presentation. Treat scikit-learn analysis as additional functionality, because the assigned problem requires process monitoring and management rather than machine-learning predictions.

### Execution plan

1. Assign actual team members to the three integrated modules and create the GitHub repository.
2. Verify process states, CPU baselines, memory values, and permission behavior on the intended machine.
3. Integrate collection with history and display the timestamp and refresh state.
4. Test process controls on a temporary worker, including cancellation, exited targets, and permission errors.
5. Review visible resource warnings and the corresponding recommendations.
6. Run the automated checks, merge tested feature branches, and retain at least seven real revisions.
7. Rebuild this report from current code, fill in actual evidence, and prepare a demonstration and viva explanation.

## Appendix B. Problem statement

Project 13: Real-Time Process Monitoring Dashboard

"Create a graphical dashboard that displays real-time information about process states, CPU usage, and memory consumption. The tool should allow administrators to manage processes efficiently and identify potential issues promptly."
