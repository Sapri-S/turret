from pathlib import Path
from docx import Document
from docx.shared import Pt

# Resolves relative to this script so the folder can move without an edit.
ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "SkyStrike_Editable_Project_Plan_Updated.docx"
OUTPUT = ROOT / "SkyStrike_Project_Plan_With_Software_Build.docx"

doc = Document(SOURCE)


def h1(t):
    doc.add_paragraph(t, style="Heading 1")


def h2(t):
    doc.add_paragraph(t, style="Heading 2")


def p(t):
    doc.add_paragraph(t)


def step(n, title, body, check):
    para = doc.add_paragraph(style="Plan Step")
    para.add_run(f"{n}. {title}. ").bold = True
    para.add_run(body)
    para.add_run(f"  Done when: {check}").italic = True


def table(headers, rows):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = ""
        c.paragraphs[0].add_run(h).bold = True
    for r in rows:
        cells = t.add_row().cells
        for i, v in enumerate(r):
            cells[i].text = v
    for row in t.rows:
        for c in row.cells:
            for para in c.paragraphs:
                para.paragraph_format.space_after = Pt(2)
                for run in para.runs:
                    run.font.size = Pt(9)
    doc.add_paragraph()


doc.add_page_break()
doc.add_paragraph("Part 2: Software Build Plan for the Fast Fruit Tracker", style="Title")
p("Added to the Sep 17 working draft. Everything here is non-firing: it detects fruit, "
  "follows it, and centers a camera. Numbers below are draft targets to revise after the "
  "first measurements, not promises.")

h1("Goal and what \"fast enough\" means")
p("The system must find a moving fake fruit, keep it identified as fruit and not a tennis "
  "ball, and keep a camera pointed at it while it moves. \"Fast enough\" is defined by three "
  "numbers we measure, not by the accelerator's advertised TOPS:")
table(
    ["Measure", "Draft target", "Why it matters"],
    [
        ["Pipeline rate", "At least 30 frames per second, steady", "Below this, a moving fruit jumps several body-widths between looks."],
        ["Camera-to-servo delay", "100 ms or less end to end", "The camera is aimed at where the fruit was; delay is the main cause of overshoot and hunting."],
        ["Centering time", "Under 1 second after the fruit stops or slows", "This is the demo the advisor will actually watch."],
        ["Fruit vs tennis ball", "No tennis ball ever treated as fruit in the held-out clips", "A wrong class moves the motors; it is the costliest error."],
        ["Track loss", "Fewer than 1 in 20 clips lose the fruit for more than 0.5 s", "Shows the tracker survives blur and brief misses."],
    ],
)
p("Test speed with the slowest realistic prop: a fake fruit thrown or rolled across the table, "
  "then swung on a string. If the system follows that, slower motion is easy.")

h1("Architecture")
p("Four stages run in separate threads so a slow stage never blocks a fast one. Each stage "
  "passes only the newest result forward and drops stale ones.")
table(
    ["Stage", "Job", "Speed rule"],
    [
        ["1. Capture", "Read camera frames into a one-slot buffer. Always keep only the newest frame.", "Never queue frames. A queue of old frames is the most common cause of lag."],
        ["2. Detect", "Run the compiled detector on the AI HAT. Output boxes, class, confidence.", "Small input size (start at 640 or 320 pixels wide). Batch of one."],
        ["3. Track", "Match this frame's boxes to the fruit from the last frame. Smooth the position and estimate its velocity (constant-velocity Kalman filter). Decide fruit or not using several frames, not one.", "Runs on the CPU in well under 5 ms. If detection runs slower than the camera, this stage fills the gaps."],
        ["4. Control", "Turn the tracked position into small, rate-limited pan and tilt commands. Send them to the servo driver.", "Fixed update rate (for example 50 Hz), independent of the camera."],
    ],
)
p("The existing Windows hand tracker already uses the right idea for stage 1: a capture "
  "thread that keeps only the latest frame, low resolution, MJPEG, and a buffer size of 1. Reuse "
  "that pattern on the Pi. Do not copy the hand tracker's firing or its center-box logic.")

h1("Software step by step")
step(1, "Create the project skeleton",
     "Make one repository with folders: capture, detect, track, control, tools, clips, results. Put every threshold (confidence, frame counts, angle limits, speeds) in one config file. Add a simple logger that writes a timestamp for each stage of every frame.",
     "Running the empty program prints one timing line per frame and exits cleanly on a key press.")
step(2, "Set up the Pi and confirm the accelerator",
     "Install the packages for your exact AI HAT variant, then run the official object-detection example from the vendor documentation. Note the exact package versions in a text file, because compiled models must match them.",
     "The stock example shows labeled boxes on live camera video at a stable frame rate.")
step(3, "Build the fast capture stage",
     "Open the camera at 640 by 480 (try 30 and 60 frames per second), use MJPEG for a USB camera or the Pi camera library for Camera Module 3, and set the buffer to 1. Put capture on its own thread and expose one call: give me the newest frame and its capture time. Lock exposure short (around 5 to 10 ms) and add light instead of raising gain, so a moving fruit is not smeared.",
     "Measured capture rate matches the setting, and a fast wave of the prop shows no visible smear.")
step(4, "Record a standard clip set",
     "Record short clips with fake fruit and tennis balls: still, slow, fast, thrown, on a string, mixed on one table, and empty scenes. Vary the background and lighting. Name each clip by session so sessions can be split later. Save the raw video, not screenshots.",
     "At least 30 clips across at least 3 sessions, with a written note of the distance and lighting for each.")
step(5, "Run a pretrained detector as a baseline",
     "Run a small pretrained detector (candidates: YOLOv8n and YOLO11n) on the clips on the laptop first, then on the Pi. Overlay boxes, labels, and confidence. Save the misses: fruit not found, ball called fruit, boxes that jump.",
     "A saved gallery of successes and failures, and a written list of which prop and condition fails most.")
step(6, "Label and split data if the baseline is not enough",
     "If pretrained labels miss the fake fruit or cannot separate it from a tennis ball, label boxes for two classes: fruit and tennis_ball. Include blurred and partly hidden frames. Split by recording session, never by frame, so near-identical frames do not appear in both training and test.",
     "A held-out test set exists whose sessions were never used for training.")
step(7, "Train or fine-tune a compact model",
     "Fine-tune the smaller candidate on the labeled frames. Use augmentation for motion blur, brightness, and small rotations. Compare candidates on the held-out clips for accuracy and, separately, for speed on the Pi. Pick the smallest model that meets the tennis-ball rule.",
     "One model is chosen, with a table of precision, recall, and ball-as-fruit errors on held-out clips.")
step(8, "Compile and deploy the model to the AI HAT",
     "Export the model, compile it for the exact HAT with the vendor toolchain, and run it through the accelerator. Test the model again on the Pi, because compiling can change accuracy slightly. Record inference time per frame with the camera running.",
     "The compiled model runs on the HAT at the target rate, and its held-out accuracy is within a few points of the laptop result.")
step(9, "Wire detect into the live pipeline",
     "Connect stage 1 to stage 2 with the newest-frame rule. Draw the box and label on screen with the total delay from capture to display. If inference is slower than the camera, run detection on every second frame and let the tracker fill in between.",
     "Live video shows stable fruit versus tennis-ball decisions with the delay printed on screen.")
step(10, "Build the tracker",
     "Match each new fruit box to the previous one by overlap and distance. Smooth the center with a constant-velocity Kalman filter and keep its velocity estimate. Call something fruit only after it is labeled fruit in several of the last frames, and drop it after a short run of misses. Output the predicted center, pushed forward by the measured pipeline delay, so the camera aims where the fruit is going.",
     "On the fast clips, the predicted center stays on the fruit and does not jump when detection briefly misses or flips class.")
step(11, "Choose fruit and reject balls",
     "Add a simple selection rule: follow only a track confirmed as fruit; ignore tennis balls and uncertain tracks completely, with no motion. If several fruit are visible, follow the largest or the one already being followed, and do not switch mid-motion.",
     "A tennis ball alone in view causes zero servo commands across all clips; two fruit do not cause target flipping.")
step(12, "Test the control loop without hardware",
     "Write a software simulator: a virtual camera view, a virtual pan and tilt with a set speed limit and delay, and a fruit that moves along recorded paths. Run the controller against it. Tune a proportional gain first, add damping only if it overshoots, and cap the speed and step per update. Add a dead zone so tiny errors cause no motion.",
     "In simulation the fruit is centered quickly with little overshoot, and the controller stops when the target is stale.")
step(13, "Build the servo driver and safety limits",
     "Wrap the servo controller behind four calls: set angle, stop, enable, disable. Enforce angle limits and a maximum step in this one place. Add a watchdog: if no fresh command arrives within a short time, hold still. Keep servo power on its own switched supply.",
     "Manual commands stay inside the limits, a killed program stops motion, and the power switch removes all movement.")
step(14, "Close the loop on the real camera mount",
     "Run the full pipeline with the camera on the pan and tilt frame. Start at low speed and gain, then raise them. Log the fruit's position error against time for each trial.",
     "The camera centers a slowly moving fruit smoothly, with no hunting, cable strain, or runaway.")
step(15, "Push the speed",
     "Raise the fruit speed in steps. When tracking breaks, look at the logs: is it capture rate, blur, detection time, delay, or the servos' own speed? Fix the biggest cause first. Options in order of cheapness: more light and shorter exposure, smaller model input, detect every other frame, faster camera mode, then a faster servo or lighter mount.",
     "A written table of the fastest fruit speed followed reliably, and the cause of the limit.")
step(16, "Evaluate against the targets",
     "Run the full clip set and the live trials. Report pipeline rate, end-to-end delay, centering time and overshoot, track loss, and every tennis-ball-as-fruit error. Compare laptop and Pi.",
     "A results table against the targets above, with failure examples.")
step(17, "Package the demo and handover",
     "Write a one-page run guide, freeze the config, and record a camera-only demo video. Store the model file, the config, and the clips together with version notes.",
     "A teammate can start the demo from the guide and reproduce the results table.")

h1("Testing and metrics")
table(
    ["Test", "How", "Pass"],
    [
        ["Detection accuracy", "Held-out clips only; count fruit found, missed, and balls called fruit.", "Meets the recognition goal set at the advisor meeting; zero balls treated as fruit."],
        ["Latency", "Flash an LED or move the prop against a clock in view; compare the frame time to the servo move.", "100 ms or less, or the measured value is written down with its cause."],
        ["Frame rate", "Log timestamps per stage for 5 minutes.", "Steady at target with no growing delay."],
        ["Centering", "Fruit moved to five positions, then along a path.", "Center error and time within the goals."],
        ["Robustness", "Change lighting, background, and add a distractor.", "No loss of the safety behavior even if accuracy drops."],
        ["Failure behavior", "Unplug the camera, cover the lens, kill the program, flip the power switch.", "Servos hold or stop every time."],
    ],
)

h1("Schedule (draft, in weeks)")
table(
    ["Weeks", "Work", "Milestone"],
    [
        ["1", "Steps 1 to 3: skeleton, Pi and HAT, capture", "Live camera runs at the target rate."],
        ["2", "Steps 4 to 5: clip set and baseline detector", "Baseline gallery and failure list."],
        ["3 to 4", "Steps 6 to 8: label, train, compile", "Compiled model running on the HAT."],
        ["5", "Steps 9 to 11: live pipeline, tracker, selection", "Stable on-screen fruit-versus-ball demo."],
        ["6", "Steps 12 to 13: simulator, servo driver, safety", "Controller tuned in simulation; hardware limits proven."],
        ["7", "Steps 14 to 15: closed loop and speed push", "Camera follows a moving fruit."],
        ["8", "Steps 16 to 17: evaluation and handover", "Results table and repeatable demo."],
    ],
)

h1("Risks and fallbacks")
table(
    ["Risk", "Sign", "Fallback"],
    [
        ["Detector too slow on the HAT", "Delay over 100 ms or frame rate under 30", "Smaller input, smaller model, detect every other frame with the tracker filling in."],
        ["Motion blur ruins detection", "Boxes vanish on fast passes", "Shorter exposure, more light, or a camera with faster readout."],
        ["Fake fruit not recognized", "Pretrained model misses it", "Label your own data (step 6) and fine-tune (step 7)."],
        ["Ball looks like fruit", "Ball-as-fruit errors on held-out clips", "More labeled ball frames, higher confidence and more frames required before acting."],
        ["Camera hunts or overshoots", "Oscillation around the target", "Lower gain, add a dead zone, add damping, use the predicted position."],
        ["Servos too slow for the fruit", "Error grows even with good tracking", "Lighter mount, faster servos, or slower prop speed with the limit written in the report."],
        ["Schedule slips", "Behind the weekly milestone", "Drop the speed push (step 15) before dropping tests or safety limits."],
    ],
)

h1("Safety and scope")
p("This part stays inside the non-firing rules of Part 1. No launcher, ammunition, trigger, or "
  "laser is connected while building or testing this software. The optional foam-dart trial in "
  "Part 1 is a separate, supervised, manual test on a printed target. The Windows Dream Cheeky "
  "hand tracker is a different project and is not part of this plan.")

doc.add_page_break()
doc.add_paragraph("Part 3: Gaps to Close Before the Build Starts", style="Title")
p("Parts 1 and 2 cover the hardware and the tracker software. This part collects everything "
  "they leave out. Some of it is technical work that Part 2 quietly assumes; the rest is "
  "project management that a senior project is graded on. Fill in every blank at the next "
  "advisor meeting.")

h1("A. Calibration: turning pixels into angles")
p("Part 2 step 14 says to turn the fruit's position into pan and tilt commands, but never says "
  "how many degrees one pixel is worth. Without that, the controller is guessing, and tuning "
  "the gain becomes trial and error that has to be redone whenever the lens, mount, or distance "
  "changes. Do this before step 14, not after.")
step("A1", "Fix the sign conventions",
     "With the fruit still, command a small pan in one direction and record whether the fruit's pixel x goes up or down. Repeat for tilt. Write the four directions into the config file. Include whether the preview image is mirrored, and mirror only for display, never for the math.",
     "A short table in the config maps each servo direction to the pixel direction it causes.")
step("A2", "Measure degrees per pixel",
     "Put a marker near image center at the working distance. Command a known servo step, measure how far the marker moved in pixels, and divide. Repeat near the left, right, top, and bottom edges, because a wide lens moves more degrees per pixel at the edge than at the center. Record the distance you measured at.",
     "Degrees per pixel is recorded for the center and edges, with the test distance noted.")
step("A3", "Set the aim point",
     "For the camera-only demo the aim point is the image center. It stops being the center the moment anything is mounted beside the camera, because that device points along its own line, not the camera's. Keep the aim point as two numbers in the config so it can be moved without touching code.",
     "The aim point is a config value, and the on-screen marker is drawn from it.")
step("A4", "Zero the aim point if a dart device is ever mounted",
     "Do this only inside the supervised trial in Part 1. Fire at a printed target, see where the dart lands relative to the aim marker, move the aim point toward the miss, and repeat. This is the same procedure as zeroing a scope. A camera mounted a few centimetres to the side of a launcher misses by a predictable, constant amount at a fixed distance, and no amount of tracking accuracy fixes it.",
     "Shots land in the marked region at the tested distance, and the zeroed offset and that distance are written down.")
p("Evidence for step A4: on the team's separate Windows Dream Cheeky launcher, tracking was "
  "accurate and shots still missed every time, purely because the camera sat to the left of the "
  "barrel. The fix was an offset applied to the aim point, tuned by firing test shots. Expect the "
  "same here, and note that the offset is only valid at the distance it was measured at.")
step("A5", "Re-calibrate after any change",
     "Treat calibration as expiring whenever the lens, camera position, mount, or working distance changes. Store the numbers with the date and the setup they were measured on.",
     "The config carries a calibration date, and the run guide says when to redo it.")

h1("B. Thermal, power, and long runs")
p("Every timing number in Part 2 is measured in short bursts. A demo runs for minutes, and a Pi 5 "
  "with an accelerator under sustained load gets hot and quietly slows itself down.")
step("B1", "Run a 30-minute soak test",
     "Run the full pipeline for 30 minutes while logging frame rate, inference time, CPU and accelerator temperature, and any throttling flag the OS reports. Do it in the real demo room, not a cold lab.",
     "Frame rate at minute 30 is within a few percent of minute 1, with temperatures logged.")
step("B2", "Fix throttling if it appears",
     "If the rate drops, add or improve active cooling before changing the model. Re-run the soak test. Record the ambient temperature the result is valid for.",
     "A passing soak test, with the cooling setup written into the parts list.")
step("B3", "Check power under load",
     "Confirm the Pi supply holds up with the accelerator and camera running, and that the servos stay on their own separate supply. Watch for low-voltage warnings during fast servo movement.",
     "No undervoltage warnings across a full soak test with the servos moving.")

h1("C. Fallback if the AI HAT path stalls")
p("Do not let one component decide whether the project has a demo. Pick the fallback now and "
  "write down the date by which the team switches.")
table(
    ["Fallback", "When to use it", "Cost"],
    [
        ["Colour and shape detection instead of a neural network", "Fake fruit is bright and uniform; a tennis ball is a different colour. Classical detection in HSV runs in a few milliseconds on the CPU.", "Less impressive, but fast, explainable, and a genuinely useful accuracy baseline to report alongside the model."],
        ["Detector on the CPU only", "The HAT or its toolchain will not cooperate.", "Lower frame rate; shrink the input size and detect every second or third frame."],
        ["Laptop does the detection, Pi does camera and servos", "The Pi cannot hit the rate at all.", "Adds network delay, so measure it; the demo needs the laptop present."],
    ],
)
step("C1", "Set the switch date",
     "Agree on a calendar date by which the HAT path must be working, and which fallback is taken if it is not.",
     "The date and the chosen fallback are written here: ____________________")

h1("D. Team, deliverables, and dates")
table(
    ["Role", "Owner", "Responsible for"],
    [
        ["Vision and model", "____________________", "Clip set, labelling, training, compiling, accuracy results."],
        ["Hardware and electrical", "____________________", "Mount, servos, wiring, separate supply, switch, fuse, spares."],
        ["Software integration", "____________________", "Threads, tracker, controller, config, run guide."],
        ["Test and documentation", "____________________", "Test protocol, logs, results tables, report and poster."],
        ["Advisor liaison", "____________________", "Weekly check-in, sign-offs, approvals for any dart trial."],
    ],
)
table(
    ["Deliverable", "Due", "Owner"],
    [
        ["Proposal or plan sign-off", "____________", "____________"],
        ["Mid-project progress report", "____________", "____________"],
        ["Camera-only tracking demo", "____________", "____________"],
        ["Poster", "____________", "____________"],
        ["Final report", "____________", "____________"],
        ["Final presentation and live demo", "____________", "____________"],
        ["Code and data handover", "____________", "____________"],
    ],
)
p("Add the weekly advisor check-in time here: ____________________. The 8-week schedule in Part 2 "
  "assumes work starts once the parts arrive; shift it by the ordering lead time in section G.")

h1("E. Repository, backups, and working practice")
step("E1", "Set up version control on day one",
     "One git repository for code and config, pushed to a remote the whole team and the advisor can reach. Commit the config file; never commit clips or model binaries. Tag a snapshot at the end of each week.",
     "Every teammate can clone the repository and run the skeleton from step 1.")
step("E2", "Decide where the large files live",
     "Video clips, labelled datasets, and compiled models are too big for git. Pick one shared drive or storage service, agree on a folder layout, and write the path into the repository's readme. Estimate the storage needed from the first session of clips and multiply.",
     "A written storage location and a size estimate, with at least one copy that is not on a single laptop.")
step("E3", "Keep a lab notebook",
     "One dated entry per working session: what changed, what was measured, what broke. The final report is far easier to write from this than from memory, and it is what lets a teammate reproduce a result.",
     "Entries exist for every session in which a measurement was taken.")
step("E4", "Keep a known-good image",
     "Once the Pi, accelerator, and camera work together, back up the microSD card image and record the exact package versions. Rebuilding the environment from scratch late in the term is a common way to lose a week.",
     "A stored card image plus a versions file, both dated.")

h1("F. Recordings, storage, and consent")
p("The clip set is training data, and people will end up in frame. Handle it deliberately.")
step("F1", "Set a naming and storage rule",
     "Name clips by session, date, prop, and condition. Keep raw clips separate from labelled exports so labels can be rebuilt.",
     "A naming rule is written down and the first session follows it.")
step("F2", "Handle people in frame",
     "Prefer framing that keeps people out of the shot. If a teammate appears, get their agreement to record and to use the footage in the report or presentation. Keep recordings on team storage, not personal cloud accounts, and do not publish faces.",
     "Agreement is recorded for anyone appearing in a clip that will be shown or published.")
step("F3", "Ask about university rules early",
     "This is not human-subjects research, but some departments still have rules about recording people and about publishing project data. One question to the advisor now avoids a problem at submission.",
     "The advisor has confirmed what applies: ____________________")

h1("G. Licensing, attribution, and ordering")
step("G1", "Check the model licence before committing to it",
     "The YOLOv8 and YOLO11 candidates named in Part 1 ship under AGPL-3.0, which carries obligations if the project's code is distributed or published. For coursework that stays internal this is usually fine, but the team should confirm with the advisor, and should know that permissively licensed detectors exist if publishing matters.",
     "The chosen model's licence is recorded, and the advisor has confirmed it is acceptable: ____________________")
step("G2", "Record attribution for anything reused",
     "List every third-party model, dataset, example, and code snippet with its source and licence. The two community launcher drivers already in the team's files belong to the separate project and stay out of this one.",
     "An attribution list exists in the repository and is copied into the report.")
step("G3", "Order with lead time and spares",
     "Order the mount, controller, supply, and wiring in one batch. Add spares for the parts that fail or get lost: a second pair of micro servos, a spare camera cable of the correct type, a spare microSD card, and spare fuses. Note each item's delivery estimate and set the schedule from the slowest one.",
     "One order placed, with a written expected arrival date for the slowest item: ____________")

h1("H. Definition of done")
p("The project is finished when all of the following are true. Agree on this wording with the "
  "advisor now, so the target does not move in the final weeks.")
table(
    ["Criterion", "Met when"],
    [
        ["It works", "The camera follows a moving fake fruit and ignores a tennis ball, repeatably, in the demo room."],
        ["It is measured", "The results table from Part 2 step 16 is filled in with real numbers, including the failures."],
        ["It is honest", "Limitations, the fastest speed it can follow, and the conditions it fails in are stated plainly."],
        ["It is reproducible", "A teammate can follow the run guide and repeat both the demo and the measurements."],
        ["It is safe", "No launcher was connected during development; any dart trial was supervised, on a printed target, with manual release."],
        ["It is handed over", "Code, config, model, clips, calibration numbers, and the notebook are in the agreed locations."],
    ],
)

h1("I. Questions still open after this draft")
p("These are not decisions the team can make alone. Take them to the advisor together with the "
  "list in Part 1.")
table(
    ["Question", "Why it matters", "Answer"],
    [
        ["Is the camera-only demo sufficient to pass?", "Decides whether the dart trial is ever needed.", "____________________"],
        ["What is the demo room, and what are its lighting and distances?", "Every speed and accuracy number depends on it.", "____________________"],
        ["What fruit speed must be followed?", "Turns Part 2 step 15 from open-ended into a target.", "____________________"],
        ["How many trials count as evidence?", "Sets the size of the test protocol.", "____________________"],
        ["Who approves the supervised dart trial, and where?", "Blocks Part 1 step 11 until answered.", "____________________"],
        ["What is the budget ceiling and who authorises spend?", "Blocks the order in G3.", "____________________"],
    ],
)

doc.save(OUTPUT)
print("saved", OUTPUT)
