import json
import os
from datetime import datetime

import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="WaitTime Dashboard",
    page_icon="🌐",
    layout="wide"
)


# ============================================================
# FILE LOCATION
# ============================================================

RESULT_FILE = "experiment_results.json"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def load_results():
    """Load experiment results from JSON file."""

    if not os.path.exists(RESULT_FILE):
        return None

    try:
        with open(RESULT_FILE, "r") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
    return None


def to_number(value, default=0.0):
    """Safely convert a value to float."""

    try:
        if value is None:
            return default

        return float(value)

    except (TypeError, ValueError):
        return default


def format_ms(seconds):
    """Convert seconds to milliseconds."""

    return f"{to_number(seconds) * 1000:.3f} ms"


# ============================================================
# LOAD DATA
# ============================================================

data = load_results()


# ============================================================
# HEADER
# ============================================================

st.title("🌐 WaitTime Dashboard")

st.subheader(
    "Utilizing Waiting Time in Half-Duplex Communication"
)

st.write(
    "A Computer Networks project that measures the waiting "
    "time during half-duplex communication and utilizes "
    "that waiting window for local task execution."
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("WaitTime")

    st.success("HALF-DUPLEX")

    st.write("### Device A")
    st.info("Transmitter / Receiver")

    st.write("### Device B")
    st.info("Receiver / Task Executor")

    st.divider()

    st.write("### Dashboard")

    if st.button(
        "🔄 Refresh Results",
        use_container_width=True
    ):
        st.rerun()

    st.divider()

    st.caption(
        "Data source:"
    )

    st.code(
        "experiment_results.json"
    )


# ============================================================
# CHECK RESULTS
# ============================================================

if data is None:

    st.warning(
        "experiment_results.json was not found."
    )

    st.write(
        "Run your Device A and Device B programs first."
    )

    st.write(
        "After the experiment creates "
        "experiment_results.json, refresh this dashboard."
    )

    st.stop()

# ============================================================
# EXPORT RESULTS
# ============================================================

st.download_button(
    label="⬇️ Download Experiment Results",
    data=json.dumps(data, indent=4),
    file_name="experiment_results.json",
    mime="application/json"
)


# ============================================================
# EXTRACT DATA
# ============================================================

rounds = data.get(
    "rounds",
    []
)

total_waiting = to_number(
    data.get(
        "total_waiting_time",
        0
    )
)

total_utilized = to_number(
    data.get(
        "total_utilized_time",
        0
    )
)

total_unused = to_number(
    data.get(
        "total_unused_time",
        0
    )
)

overall_utilization = to_number(
    data.get(
        "overall_utilization_percentage",
        0
    )
)


# ============================================================
# EXPERIMENT STATUS
# ============================================================

st.divider()

st.header("Experiment Status")

status1, status2, status3 = st.columns(3)

with status1:

    st.success(
        "### Device A\n"
        "Transmitter / Receiver"
    )

with status2:

    st.info(
        "### Communication\n"
        "HALF-DUPLEX"
    )

with status3:

    st.success(
        "### Device B\n"
        "Receiver / Task Executor"
    )


# ============================================================
# COMMUNICATION FLOW
# ============================================================

st.divider()

st.header("Communication Flow")

flow1, flow2, flow3, flow4, flow5 = st.columns(
    [2, 1, 2, 1, 2]
)

with flow1:

    st.info(
        "### Device A\n\n"
        "Transmits Data"
    )

with flow2:

    st.markdown(
        "# →"
    )

with flow3:

    st.warning(
        "### Device B\n\n"
        "Waits for Data"
    )

with flow4:

    st.markdown(
        "# →"
    )

with flow5:

    st.success(
        "### Waiting Window\n\n"
        "Execute Suitable Task"
    )


# ============================================================
# OVERALL PERFORMANCE
# ============================================================

st.divider()

st.header("Overall Performance")

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:

    st.metric(
        "Total Waiting Time",
        format_ms(total_waiting)
    )

with metric2:

    st.metric(
        "Utilized Time",
        format_ms(total_utilized)
    )

with metric3:

    st.metric(
        "Unused Time",
        format_ms(total_unused)
    )

with metric4:

    st.metric(
        "Overall Utilization",
        f"{overall_utilization:.2f}%"
    )


# ============================================================
# SUMMARY
# ============================================================

st.divider()

st.header("Experiment Summary")

task_count = 0

for result in rounds:

    if result.get("selected_task") is not None:
        task_count += 1


summary1, summary2, summary3 = st.columns(3)

with summary1:

    st.metric(
        "Communication Rounds",
        len(rounds)
    )

with summary2:

    st.metric(
        "Tasks Executed",
        task_count
    )

with summary3:

    st.metric(
        "Unused Waiting Percentage",
        f"{max(0, 100 - overall_utilization):.2f}%"
    )


# ============================================================
# ROUND RESULTS
# ============================================================

st.divider()

st.header("Round-by-Round Results")


if len(rounds) == 0:

    st.info(
        "No round results are available."
    )

else:

    for result in rounds:

        round_number = result.get(
            "round",
            "-"
        )

        predicted_wait = result.get(
            "predicted_waiting_time"
        )

        actual_wait = to_number(
            result.get(
                "actual_waiting_time",
                0
            )
        )

        selected_task = result.get(
            "selected_task"
        )

        expected_task_time = to_number(
            result.get(
                "expected_task_time",
                0
            )
        )

        actual_task_time = to_number(
            result.get(
                "actual_task_time",
                0
            )
        )

        utilized_time = to_number(
            result.get(
                "utilized_waiting_time",
                0
            )
        )

        unused_time = result.get(
            "unused_waiting_time"
        )

        if unused_time is None:

            unused_time = max(
                actual_wait - utilized_time,
                0
            )

        else:

            unused_time = to_number(
                unused_time
            )

        utilization = to_number(
            result.get(
                "utilization_percentage",
                0
            )
        )


        # ----------------------------------------------------
        # ROUND TITLE
        # ----------------------------------------------------

        st.subheader(
            f"Round {round_number}"
        )


        # ----------------------------------------------------
        # ROUND INFORMATION
        # ----------------------------------------------------

        col1, col2, col3 = st.columns(3)


        with col1:

            st.write(
                "**Predicted Waiting Time**"
            )

            if predicted_wait is None:

                st.write(
                    "Not available"
                )

            else:

                st.write(
                    format_ms(predicted_wait)
                )


            st.write(
                "**Actual Waiting Time**"
            )

            st.write(
                format_ms(actual_wait)
            )


        with col2:

            st.write(
                "**Selected Task**"
            )

            if selected_task is None:

                st.write(
                    "No task selected"
                )

            else:

                st.write(
                    selected_task
                )


            st.write(
                "**Expected Task Time**"
            )

            st.write(
                format_ms(expected_task_time)
            )


        with col3:

            st.write(
                "**Actual Task Time**"
            )

            st.write(
                format_ms(actual_task_time)
            )


            st.write(
                "**Round Utilization**"
            )

            st.write(
                f"{utilization:.2f}%"
            )

            st.progress(
                min(
                    max(
                        utilization / 100,
                        0
                    ),
                    1
                )
            )


        # ----------------------------------------------------
        # UTILIZED / UNUSED
        # ----------------------------------------------------

        time1, time2 = st.columns(2)

        with time1:

            st.success(
                f"Utilized Waiting Time: "
                f"{format_ms(utilized_time)}"
            )

        with time2:

            st.warning(
                f"Unused Waiting Time: "
                f"{format_ms(unused_time)}"
            )


        st.divider()


# ============================================================
# TASK SCHEDULING
# ============================================================

st.header("Task Scheduling Details")


found_task = False


for result in rounds:

    task_name = result.get(
        "selected_task"
    )

    if task_name is None:
        continue

    found_task = True

    round_number = result.get(
        "round",
        "-"
    )

    expected_time = to_number(
        result.get(
            "expected_task_time",
            0
        )
    )

    actual_time = to_number(
        result.get(
            "actual_task_time",
            0
        )
    )

    utilized_time = to_number(
        result.get(
            "utilized_waiting_time",
            0
        )
    )


    with st.expander(
        f"Round {round_number} — {task_name}"
    ):

        t1, t2, t3 = st.columns(3)

        with t1:

            st.write(
                "**Task**"
            )

            st.write(
                task_name
            )

        with t2:

            st.write(
                "**Expected Execution Time**"
            )

            st.write(
                format_ms(expected_time)
            )

        with t3:

            st.write(
                "**Actual Execution Time**"
            )

            st.write(
                format_ms(actual_time)
            )

        st.write(
            "**Waiting Time Utilized:** "
            f"{format_ms(utilized_time)}"
        )


if not found_task:

    st.info(
        "No task was selected during the available "
        "waiting windows."
    )


# ============================================================
# PROJECT WORKFLOW
# ============================================================

st.divider()

st.header("How WaitTime Works")

step1, step2, step3, step4 = st.columns(4)


with step1:

    st.markdown(
        """
        ### 1. Communicate

        Device A transmits data to Device B.
        """
    )


with step2:

    st.markdown(
        """
        ### 2. Measure

        Device B measures the time it spends waiting.
        """
    )


with step3:

    st.markdown(
        """
        ### 3. Select Task

        The scheduler checks whether a task can fit
        inside the available waiting window.
        """
    )


with step4:

    st.markdown(
        """
        ### 4. Utilize

        The selected task is executed while waiting,
        and utilized and unused time are measured.
        """
    )


# ============================================================
# FORMULA
# ============================================================

st.divider()

st.header("Performance Calculation")

st.write(
    "**Waiting Time**"
)

st.code(
    "Waiting Time = Waiting End Time - Waiting Start Time"
)

st.write(
    "**Unused Waiting Time**"
)

st.code(
    "Unused Time = Actual Waiting Time - Utilized Time"
)

st.write(
    "**Utilization**"
)

st.code(
    "Utilization = (Utilized Time / Waiting Time) × 100"
)


# ============================================================
# LAST UPDATED
# ============================================================

try:

    modified_time = os.path.getmtime(
        RESULT_FILE
    )

    last_updated = datetime.fromtimestamp(
        modified_time
    ).strftime(
        "%d-%m-%Y %H:%M:%S"
    )

except Exception:

    last_updated = "Unknown"


st.divider()

st.caption(
    "WaitTime • Half-Duplex Communication Project"
)

st.caption(
    f"Results last updated: {last_updated}"
)
