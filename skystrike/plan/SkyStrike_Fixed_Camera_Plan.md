# SkyStrike Fixed Camera Sensing and Tracking Project Plan

Planning proposal for a six-person senior design team — September 21, 2026

## Project goal

Design, build, and evaluate a standalone system that uses fixed cameras and approach sensors to detect incoming objects, recognize specified artificial fruit and ball classes, maintain object identities, recover after temporary obstruction, and automatically report measured performance. Use an instrumented moving-object test rig to provide an independent reference for position and speed.

The cameras remain stationary. The project uses a premade dataset as its starting point and records a separate local evaluation set containing the actual props and operating conditions. A premade dataset is not necessarily a pretrained model; selecting a compatible model and determining whether additional training is needed remain engineering tasks.

This plan consolidates the selected ideas into a proposed scope. It does not indicate that the features have been built, validated, or approved by the advisor. It supersedes the earlier moving-camera concept for this proposal.

## Scope and outputs

The system produces labeled video, object identities, approach alerts, confidence and uncertainty indicators, event histories, and experimental reports. It has no connection to weapon aiming, triggering, or firing controls. Person and animal detection are evaluated as scene-exclusion features, not represented as guarantees or physical safety interlocks.

The A.S.S. II release is background reference material, not a software dependency or implementation starting point for this sensing system. Its automated airsoft targeting and firing functionality is outside this plan. Reusing its frame as a non-firing structure remains an unselected option; no turret speed or firing modification is included.

## System concept

Approach detected → event timestamped → object enters camera view → classification assessed → identity maintained → result logged.

An approach sensor reports an event, not an object class. The software must explicitly assess whether an observed object corresponds to that event. If several associations are plausible, retain the uncertainty rather than selecting one without evidence. An event may expire without ever being matched to a camera observation.

Fixed cameras feed recognition and tracking software. Sensor events feed a separate timestamped event stream. An association module compares observations, while a dashboard displays the resulting tracks and system status. Recording and evaluation tools consume the same observations and logs. The test rig supplies independent reference measurements; those measurements must not leak into the tracking algorithm during evaluation.

## Camera arrangement

| Arrangement | Purpose | Main limitation |
| --- | --- | --- |
| One fixed camera | Establish a baseline for recognition and tracking | Cannot observe beyond its view or through an obstruction |
| Two fixed cameras with overlapping views | Test whether another viewpoint improves continuity and obstruction recovery | Requires cross-view association, time alignment, and calibration |
| Two fixed cameras with adjacent views | Test early observation and identity handoff along a path | A gap between views makes association more uncertain |

Proposed development direction: establish the one-camera baseline, then add two overlapping fixed views. Treat adjacent coverage as an alternative layout experiment if time permits. Camera count and positions remain subject to room, budget, and compute measurements.

Two cameras do not automatically provide depth. Metric stereo depth would require a specifically calibrated configuration and suitable synchronized observations; it is not a baseline requirement. A hidden object cannot be observed by either camera if both views are obstructed.

### Camera requirements to establish before purchase

Camera selection is currently open. The following properties must be specified rather than discovered after purchase, because each one can make the recorded data unusable for fast-moving props regardless of how good the software is.

| Property | Requirement | Consequence if unspecified |
| --- | --- | --- |
| Shutter type | Global shutter | A rolling shutter exposes image rows at different times, so a fast object is recorded skewed. Its measured position and shape are then wrong in a way no later processing can undo. |
| Frame rate | Derived from the fastest prop speed and the largest acceptable between-frame displacement, not chosen by convention | At 30 fps an object moving 10 m/s travels about 0.33 m between frames. Association and velocity estimates degrade sharply once displacement approaches object size. |
| Exposure time | Short enough that motion blur stays below the tolerated centroid error at maximum prop speed | Blur enlarges and biases the detected object. This constrains lighting, which constrains budget. |
| Synchronisation | Hardware trigger or an equivalent common time base across cameras, with the residual offset measured | Independent software timestamps drift. For two views of a fast object, a few milliseconds of offset appears as a large position disagreement, which corrupts cross-view association. |
| Interface and latency | Measured capture-to-available latency for the specific camera and driver path, not the vendor frame-rate figure | Frame rate describes throughput, not delay. A camera can deliver many frames per second and still present each one late. |
| Resolution and lens | Chosen together, from required workspace coverage and the pixels needed on the smallest prop at maximum range | Resolution alone does not determine whether a prop is detectable. |
| Mount rigidity | Rigid enough that vibration does not move the view beyond calibration tolerance | Mount movement silently invalidates a stored calibration. |

Record achieved values, not only intended ones. Settle the frame-rate and exposure requirement early, because it drives lighting, interface, compute and cost together.

## Approach sensors

Place candidate sensors where the test path crosses an approach boundary outside camera coverage. Select the technology only after specifying the working distance, prop size, speed, ambient conditions, and required warning interval.

Candidate experiments include a boundary-crossing sensor and a distance sensor. Compare detection probability, false alerts, event timing, coverage, and whether the sensor detects the actual props. Do not assume a sensor's coverage or range exceeds the camera's useful coverage without measurements.

Record sensor events independently of camera classification. Association should allow unmatched alerts, multiple candidate objects, expired events, and sensor faults. A sensor alert must never be promoted directly to confirmed fruit.

Distinguish two different sensor roles and do not conflate them. A **boundary or presence sensor** answers "something crossed", producing a timestamped event with little or no position information and no velocity. A **measurement sensor** contributes a position or range estimate that could enter a state estimate alongside camera observations. The candidate devices discussed so far, including multizone time-of-flight modules, belong to the first category: their zone count, update rate and range resolution suit presence detection, not estimating where a prop is or where it is heading.

This bounds what the sensor subsystem can ever deliver. An event sensor can provide advance warning and an independent check on camera timing. It cannot refine a track, and it cannot support any later work that depends on knowing an object's trajectory. If a sensor is ever required to contribute to a state estimate, that is a different specification -- stated range resolution, stated update rate, stated latency -- and a different selection exercise.

## Selected feature requirements

| Feature | Planned behavior | Demonstration and evidence |
| --- | --- | --- |
| Persistent tracking of multiple objects | Assign track IDs, preserve them across visible motion, and let the operator select a track for display | Crossing-object trials; identity-switch and fragmentation counts |
| Recovery after obstruction | Mark a track as temporarily unobserved, attempt reassociation when it returns, and report ambiguity | Recovery time, correct reassociation rate, and false reassociations |
| Automatic camera calibration | Guide image collection from a known calibration target, calculate parameters, check quality, and save the setup version | Calibration error plus checks on independent images or known positions |
| Adaptive tracking modes | Adjust selected camera or processing settings based on measured conditions | Fixed-setting versus adaptive trials on the same condition set |
| Repeatable moving-object test rig | Move inert props along controlled paths with independent position or speed measurements | Path repeatability, reference-measurement uncertainty, and recorded speed |
| Automatic performance report | Generate results from versioned logs with consistent metric definitions | A report reproduced from the same saved trial data |

### Persistent identity and obstruction recovery

Classification and identity are separate: two objects can both be fruit without being distinguishable individuals. Use explicit tentative, confirmed, temporarily lost, ambiguous, and ended track states. Do not silently transfer a selected identity to a different object. Visually identical props after complete obstruction may require operator reselection.

During early tests, use distinguishable props to establish a baseline, then add similar props as a harder condition. Report both results separately.

### Calibration

Begin with guided calibration: a teammate presents a known board while software selects usable images, estimates lens parameters, and reports quality. With two cameras, also establish their relationship to the workspace and check time alignment. Fully unattended calibration is a stretch objective, not assumed in the baseline.

Record camera identity, resolution, relevant lens settings, mount position, date, and calibration version. Invalidate affected calibration when the camera or lens configuration changes. Test sensor-to-workspace mapping separately from camera calibration.

### Adaptive modes

Start with a small number of explainable modes, such as normal lighting, low light, and fast motion. Log the selected mode, the measurements that triggered it, and every setting change. Prevent rapid switching between modes. Each mode must be evaluated for recognition quality, latency, and track continuity; an adaptive mode is not successful merely because it changes settings.

### Moving-object test rig

Choose a constrained path appropriate for the room and budget, such as a guided carriage or small conveyor carrying artificial fruit and balls. Provide repeatable start positions, interchangeable props, and removable obstruction panels. Include a reachable stop control and appropriate mechanical guarding.

Measure actual motion using independent feedback rather than treating a commanded motor speed as ground truth. Characterize the rig's measurement uncertainty before using it to judge the camera system. Test-rig motion remains independent of object classification.

A guided carriage or conveyor produces constant-velocity motion along a fixed straight path. That is the easiest case the system will ever see. It is a deliberate starting point, not a sufficient one: it does not exercise acceleration, path curvature, apparent size changing with range, or the shorter observation window of a fast prop.

Plan a second motion condition with a curved, accelerating path -- an inclined guided path, a pendulum carrier, or a prop released down a ramp and allowed to fall -- so recognition and tracking are evaluated against changing velocity. Keep the independent reference measurement for this condition too; a trajectory nobody measured is not evidence. Report straight-path and curved-path results separately rather than pooling them, because pooling hides the harder case.

### Automatic report

Every report should identify software and configuration versions, model and dataset versions, calibration, camera layout, sensor settings, prop identities, lighting conditions, trial count, and rejected or incomplete trials.

Include detection precision and recall, class confusion, identity switches, tracking losses, recovery time, event-association errors, sensor warning interval, processing latency, and hardware health. Include plots, representative failure examples, and limitations. Report uncertainty and trial counts; zero observed errors does not establish that errors are impossible.

## Classification and scene exclusions

The intended recognition vocabulary consists of specified artificial fruit and ball classes. Arbitrary round objects are not automatically accepted: shape alone is insufficient evidence of class.

The original plan rejected tennis balls. Later discussion proposed fruit and balls as supported objects. Keep this as an explicit open decision rather than silently changing the evaluation labels.

Use supported, distractor, and unknown classifications. When a person or animal is detected, display a scene-exclusion indicator and withhold a confirmed-prop status for the affected scene according to a documented rule. Missing or stale camera data produces an unavailable state. Evaluate missed exclusions and false exclusions; these software features do not certify that a scene contains no people or animals.

Prefer artificial props and existing appropriately licensed footage for exclusion evaluation. No live animal participation is needed. Handle any recordings containing people according to university and participant requirements.

## Six-person ownership

| Member | Primary responsibility | Individual technical deliverable | Main collaboration |
| --- | --- | --- | --- |
| 1 — Vision and model evaluation | Premade dataset review, model selection, local test set, class and exclusion evaluation | Reproducible recognition benchmark and error analysis | Members 2 and 3 |
| 2 — Embedded computing and camera pipeline | Pi and AI HAT deployment, fixed-camera capture, timing, compute and thermal measurements | Versioned capture/inference pipeline and performance benchmark | Members 1 and 6 |
| 3 — Tracking and association | Multiple-object identities, cross-view matching, sensor-event association, recovery | Evaluated tracker with uncertainty states and replay tests | Members 1, 4, and 6 |
| 4 — Sensors and electronics | Approach sensing, timestamps, acquisition firmware, wiring, diagnostics | Characterized sensor subsystem and electrical documentation | Members 3 and 5 |
| 5 — Mechanical design and metrology | Fixed mounts, controlled-motion rig, reference feedback, repeatability | CAD, rig assembly, and independent measurement validation | Members 4 and 6 |
| 6 — Calibration, integration, and reporting | Calibration workflow, dashboard, trial orchestration, report generation | Integrated operator workflow and reproducible result package | All members |

Balance workload at weekly reviews. Member 2 owns adaptive capture and processing implementation; Members 1 and 6 help define and evaluate its behavior. Member 6 coordinates calibration software while Members 2, 4, and 5 provide camera, sensor, and physical reference measurements. Each person tests and documents their own subsystem. Rotate meeting administration; advisor liaison is not a standalone engineering role.

## Interfaces and working practice

Agree on shared records before subsystem implementation: frame ID and capture timestamp; camera ID; detection box, class, and score; track ID and state; sensor ID and event timestamp; reference position; and configuration/calibration versions.

Document timestamp meaning and clock relationships. On one machine, use a suitable monotonic clock for elapsed-time measurement. For separate devices, quantify synchronization and timestamp uncertainty. Do not equate processing completion time with capture time or sensor crossing time.

Use a replay mode so recognition, tracking, and reports can be developed without access to the rig. Keep datasets and large model files in agreed shared storage and reference their versions from the repository. Every subsystem should provide sample input and output records for integration.

## Evaluation plan

| Experiment | Comparison | Main measurements |
| --- | --- | --- |
| Added camera | One fixed camera versus two overlapping fixed cameras | Identity switches, track continuity, recovery, processing cost |
| Advance sensing | Camera-only observations versus camera plus sensor alerts | Warning interval, missed approaches, false alerts, association errors |
| Adaptive behavior | Fixed settings versus adaptive modes | Recognition, latency, losses, mode-switch frequency |
| Obstruction | No obstruction, partial obstruction, complete temporary obstruction | Correct recovery, recovery time, ambiguity, incorrect identity transfers |
| Similar objects | Distinct props versus visually similar props | Identity consistency and reselection frequency |
| Sustained operation | Beginning versus end of an extended run | Frame rate, latency distribution, temperature, dropped observations |

Vary speed, distance, lighting, background, object count, and obstruction duration deliberately. Avoid changing every factor at once. Split data by recording session and reserve a final held-out evaluation set. Keep tuning separate from final test evaluation.

Define latency endpoints precisely, and measure more than one. Camera-to-servo delay from the old plan no longer applies.

Measure these separately:

- **Capture to result available** -- from frame exposure to the moment a completed detection and track update exists in memory. This describes how quickly the system could act on what it saw.
- **Capture to displayed result** -- the same path continued through rendering to the dashboard. Always larger. It describes the operator experience, not the system's responsiveness.
- **Sensor event to logged alert** -- the independent sensor path.

Reporting only the displayed figure conflates the processing pipeline with the rendering path. It would credit the system with a delay it does not have, or blame it for one belonging to the display. Instrument the boundary between them explicitly.

Derive a target for capture-to-result-available from the physics of the fastest prop **before** measuring: state the displacement that occurs within one pipeline delay, decide what displacement is acceptable, and let that set the requirement. Then measure whether it is met. Choosing a latency threshold after seeing the measurements records what was achieved but cannot show whether it was ever enough.

Report distributions, including a high-percentile value, rather than only averages. A pipeline that is fast on average and occasionally very slow behaves differently from a consistently moderate one, and the average hides exactly that.

Choose numeric acceptance thresholds after baseline measurements and advisor review. Specify required workspace coverage, prop speeds and sizes, detection performance, acceptable identity errors, recovery time, warning interval, runtime, and trial counts. Record any unmet thresholds honestly.

## Two-semester development plan

The team has two semesters. Exact dates and semester lengths remain to be confirmed. Organize work by phases and advisor milestones rather than assuming an eight-week build. Preserve time for coursework, procurement, exams, redesign, and final evaluation.

### Semester one — feasibility, funding, and subsystem prototypes

| Phase | Work | Evidence before moving on |
| --- | --- | --- |
| Early semester | Agree on requirements; inventory owned and borrowable equipment; confirm roles, room, dates, and AI HAT variant | Requirements draft, inventory, and responsibilities |
| Early to middle | Evaluate premade data and candidate models; test existing cameras; bench-test approach-sensor candidates | Baseline results and a list of demonstrated limitations |
| Middle | Compare camera layouts; sketch and prototype the test rig; define software records and calibration approach | Design comparison, initial CAD, and sample data flowing through logging |
| Middle to late | Prepare a costed bill of materials and funding request; seek equipment loans and fabrication support | Documented funding status and a minimum affordable design |
| Late | Demonstrate one-camera recognition, sensor logging, and a small repeatable motion experiment; review risks | Subsystem demonstrations and evidence supporting selected parts |
| End of semester | Advisor design review; set measurable targets; prioritize second-semester work; archive code and results | Approved direction, updated budget, procurement plan, and handover package |

Do not wait until the end of semester one to connect software components. Use saved recordings, simulated sensor records, and existing equipment for early integration. Do not assume access to labs or team labor during the semester break.

### Semester two — integration, improvements, and evaluation

| Phase | Work | Evidence before moving on |
| --- | --- | --- |
| Early semester | Assemble funded hardware; validate the test rig and independent reference measurements | Working baseline system and characterized measurement uncertainty |
| Early to middle | Integrate the second fixed camera if funded; add calibration, persistent identities, and sensor-event association | Repeatable integrated trials with explicit uncertainty states |
| Middle | Develop obstruction recovery and a small number of adaptive modes; complete dashboard and report generation | Comparisons against the retained baseline |
| Middle to late | Run fault and sustained-operation tests; correct major failures; freeze features and evaluation settings | Stable release ready for held-out testing |
| Final portion | Run held-out experiments; analyze results; finish report, poster, demonstration, and handover | Reproducible results and clearly stated limitations |

Reserve the final quarter of semester two primarily for evaluation, fixes, and presentation. Confirm the actual feature-freeze date with the course schedule. Reduce optional layouts or modes if necessary rather than consuming the evaluation period.

## Funding and purchasing plan

Funding availability and prices have not yet been researched. The categories below are a planning checklist, not confirmed funding sources or a quoted budget. No purchases, applications, or sponsor outreach are authorized by this document.

### Establish what the team already has

Verify the Pi 5 and AI HAT previously reported as owned, existing cameras, computers, power supplies, storage, props, and basic tools. Ask which equipment the department can lend and which fabrication facilities are available. Record ownership, availability, condition, and return obligations. Separate cash spending from the replacement value of borrowed or owned equipment.

### Build three budget options

| Option | Contents | Decision purpose |
| --- | --- | --- |
| Minimum baseline | Existing compute and one fixed camera, basic approach-sensor experiment, simple measured motion rig, logging | Establish a feasible demonstration if funding is limited |
| Target project | Two fixed views, selected approach sensors, independently measured rig, calibration and full evaluation software | Fund the planned comparative experiments |
| Optional expansion | Additional sensor comparisons, alternative camera layouts, extra adaptive modes | Add only after the target system and evaluation needs are funded |

For each line item record quantity, specification, supplier quote and date, shipping and taxes, lead time, funding source, owner, and whether it is essential or optional. Include mounts, cables, power, fabrication materials, reference feedback, props, storage, spare wear items, and any necessary compute costs. Set a contingency allowance after the initial estimates; do not disguise unknown costs as zero.

### Investigate funding routes

Start with the course or department's senior-design allocation and purchasing process. Then investigate university project grants, equipment loans, makerspace support, and relevant industry sponsorship or in-kind donations. Availability and eligibility require institution-specific verification. Team contributions are an option only if members voluntarily agree on a ceiling; do not assume equal personal spending is affordable.

Prepare a short funding package: project purpose, six-person responsibilities, preliminary evidence, itemized budget, minimum and target options, schedule, and intended deliverables. Describe the standalone sensing and tracking scope accurately. Confirm any sponsor conditions, ownership, publication expectations, and university acceptance process before accepting support.

### Spend in stages

1. Inventory and borrow before buying duplicates.
2. Buy only limited evaluation parts needed to resolve uncertain design choices.
3. Select production parts after prototype evidence and available funding are known.
4. Order the main build with delivery time and replacement risk accounted for.
5. Protect the remaining budget for validation, repairs, and final demonstration needs.

Maintain a funding tracker with requested amount, confirmed amount, restrictions, decision date, and purchasing status. Assign one team member as budget coordinator while each subsystem owner supplies their own estimates. Review the budget at design reviews and whenever a major part changes.

## Decisions still needed

1. Are tennis balls accepted classes or distractors? Which fruit and ball types are supported?
2. Which premade dataset and model are proposed, and do their labels and permitted uses fit the project?
3. What are the exact AI HAT, cameras, available interfaces, and computing resources?
4. What are the budget, term dates, room dimensions, lighting, prop sizes, and motion speeds?
5. Is two-camera coverage a required deliverable or a stretch objective?
6. Which sensor technology meets the actual approach geometry and timing needs?
7. What independent reference accuracy can the test rig provide?
8. What numerical thresholds and trial counts will the advisor accept?

## Definition of done

The fixed-camera system recognizes the agreed props, reports uncertainty, maintains identities within its demonstrated limits, measures approach events, and documents obstruction recovery. The selected calibration and adaptive functions are evaluated rather than merely demonstrated. An independent rig supports the measurements, and the automatic report can be regenerated from retained logs. Code, configuration, calibration, model/data references, drawings, wiring documentation, and the run guide are handed over together.

## Technical references

- Camera calibration: https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html
- Stereo depth principles: https://docs.opencv.org/4.x/dd/d53/tutorial_py_depthmap.html
- Example multizone distance-sensing technology, not a selected part: https://www.st.com/en/imaging-and-photonics-solutions/vl53l5cx

Background reviewed: the local SkyStrike full plan and project records, plus the A.S.S. II README and hardware inventory. This proposal does not carry forward their installation commands or automated weapon functions.
