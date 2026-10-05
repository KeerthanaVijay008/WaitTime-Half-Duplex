import socket
import time
import threading
import json
import task_scheduler


# ============================================================
# CONFIGURATION
# ============================================================

HOST = "127.0.0.1"
PORT = 5001

ROUNDS = 3
DATA_SIZE = 1024 * 1024

SAFETY_FACTOR = 0.80


# ============================================================
# TASK EXECUTION
# ============================================================

def run_task(task_name, timing_result):
    """
    Execute the selected task in a separate thread
    and record its actual execution time.
    """

    timing_result["start"] = time.perf_counter()

    task_scheduler.execute_task(task_name)

    timing_result["end"] = time.perf_counter()


# ============================================================
# SERVER SETUP
# ============================================================

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

server.bind((HOST, PORT))
server.listen(1)


print("=" * 38)
print("          DEVICE B SERVER")
print("=" * 38)
print(f"Listening on {HOST}:{PORT}")
print()
print("Device B waiting for Device A...")


sock, address = server.accept()

print("Device A connected.")
print("Starting half-duplex communication...")
print()


# ============================================================
# LOAD TASK TIMES
# ============================================================

task_times = task_scheduler.load_task_times()


# ============================================================
# EXPERIMENT VARIABLES
# ============================================================

previous_wait_times = []

results = []

total_waiting_time = 0.0
total_utilized_time = 0.0

# Tasks already used during this experiment
used_tasks = set()


# ============================================================
# COMMUNICATION ROUNDS
# ============================================================

for round_no in range(1, ROUNDS + 1):

    # --------------------------------------------------------
    # PREDICT WAITING TIME
    # --------------------------------------------------------

    if len(previous_wait_times) == 0:

        predicted_wait = 0.0

    else:

        predicted_wait = (
            sum(previous_wait_times)
            / len(previous_wait_times)
        )

        predicted_wait = predicted_wait * SAFETY_FACTOR


    # --------------------------------------------------------
    # SELECT TASK
    # --------------------------------------------------------

    selected_task = task_scheduler.choose_task(
    predicted_wait,
    task_times,
    used_tasks
)


    if selected_task is not None:

        task_name = selected_task[0]
        expected_task_time = selected_task[1]

        # Remember this task for the next round
        previous_task = task_name

    else:

        task_name = None
        expected_task_time = 0.0


    # --------------------------------------------------------
    # PREPARE TASK TIMING
    # --------------------------------------------------------

    timing_result = {
        "start": None,
        "end": None
    }


    # --------------------------------------------------------
    # START WAITING PERIOD
    # --------------------------------------------------------

    waiting_start = time.perf_counter()


    # Start selected task in parallel
    if task_name is not None:

        task_thread = threading.Thread(
            target=run_task,
            args=(task_name, timing_result)
        )

        task_thread.start()

    else:

        task_thread = None


    # --------------------------------------------------------
    # RECEIVE DATA FROM DEVICE A
    # --------------------------------------------------------

    received_bytes = 0

    while received_bytes < DATA_SIZE:

        data = sock.recv(
            min(65536, DATA_SIZE - received_bytes)
        )

        if not data:
            break

        received_bytes += len(data)


    # --------------------------------------------------------
    # END WAITING PERIOD
    # --------------------------------------------------------

    waiting_end = time.perf_counter()

    actual_waiting_time = (
        waiting_end - waiting_start
    )


    # --------------------------------------------------------
    # WAIT FOR TASK TO FINISH
    # --------------------------------------------------------

    if task_thread is not None:

        task_thread.join()


    # --------------------------------------------------------
    # CALCULATE TASK EXECUTION TIME
    # --------------------------------------------------------

    if (
        timing_result["start"] is not None
        and timing_result["end"] is not None
    ):

        actual_task_time = (
            timing_result["end"]
            - timing_result["start"]
        )

    else:

        actual_task_time = 0.0


    # --------------------------------------------------------
    # CALCULATE UTILIZED WAITING TIME
    # --------------------------------------------------------

    utilized_waiting_time = min(
        actual_task_time,
        actual_waiting_time
    )


    unused_waiting_time = max(
        0.0,
        actual_waiting_time
        - utilized_waiting_time
    )


    if actual_waiting_time > 0:

        utilization_percentage = (
            utilized_waiting_time
            / actual_waiting_time
        ) * 100

    else:

        utilization_percentage = 0.0


    # --------------------------------------------------------
    # STORE WAITING TIME FOR NEXT PREDICTION
    # --------------------------------------------------------

    previous_wait_times.append(
        actual_waiting_time
    )


    # --------------------------------------------------------
    # UPDATE TOTALS
    # --------------------------------------------------------

    total_waiting_time += actual_waiting_time

    total_utilized_time += utilized_waiting_time


    # --------------------------------------------------------
    # SAVE ROUND RESULT
    # --------------------------------------------------------

    results.append({

        "round": round_no,

        "predicted_waiting_time": predicted_wait,

        "actual_waiting_time": actual_waiting_time,

        "selected_task": task_name,

        "expected_task_time": expected_task_time,

        "actual_task_time": actual_task_time,

        "utilized_waiting_time": utilized_waiting_time,

        "unused_waiting_time": unused_waiting_time,

        "utilization_percentage": utilization_percentage
    })


    # --------------------------------------------------------
    # SEND RESPONSE TO DEVICE A
    # --------------------------------------------------------

    response = (
        f"ACK|DATA_FROM_B_ROUND_{round_no}|TURN_TO_A"
    ).encode()

    sock.sendall(response)


# ============================================================
# OVERALL UTILIZATION
# ============================================================

if total_waiting_time > 0:

    overall_utilization = (
        total_utilized_time
        / total_waiting_time
    ) * 100

else:

    overall_utilization = 0.0


total_unused_time = (
    total_waiting_time
    - total_utilized_time
)


# ============================================================
# EXPERIMENT SUMMARY
# ============================================================

print()
print("=" * 100)
print("                              EXPERIMENT SUMMARY")
print("=" * 100)

print(
    f"{'Round':^7}|"
    f"{'Predicted':^13}|"
    f"{'Actual Wait':^15}|"
    f"{'Task':^25}|"
    f"{'Utilized':^14}|"
    f"{'Util %':^10}"
)

print("-" * 100)


for result in results:

    predicted = result["predicted_waiting_time"]
    actual_wait = result["actual_waiting_time"]
    task_name = result["selected_task"]
    utilized = result["utilized_waiting_time"]
    utilization = result["utilization_percentage"]


    if predicted == 0:

        predicted_text = "--"

    else:

        predicted_text = f"{predicted:.6f}"


    if task_name is None:

        task_text = "None"

    else:

        task_text = task_name


    print(
        f"{result['round']:^7}|"
        f"{predicted_text:^13}|"
        f"{actual_wait:^15.6f}|"
        f"{task_text:^25}|"
        f"{utilized:^14.6f}|"
        f"{utilization:^9.2f}%"
    )


print("-" * 100)

print(
    f"Total Waiting Time       : "
    f"{total_waiting_time:.6f} seconds"
)

print(
    f"Total Utilized Time      : "
    f"{total_utilized_time:.6f} seconds"
)

print(
    f"Total Unused Time        : "
    f"{total_unused_time:.6f} seconds"
)

print(
    f"Overall Utilization      : "
    f"{overall_utilization:.2f}%"
)

print("=" * 100)


# ============================================================
# SAVE EXPERIMENT RESULTS
# ============================================================

experiment_data = {

    "rounds": results,

    "total_waiting_time":
        total_waiting_time,

    "total_utilized_time":
        total_utilized_time,

    "total_unused_time":
        total_unused_time,

    "overall_utilization_percentage":
        overall_utilization
}


with open(
    "experiment_results.json",
    "w"
) as file:

    json.dump(
        experiment_data,
        file,
        indent=4
    )


print()
print("Experiment results saved to experiment_results.json")


# ============================================================
# CLOSE CONNECTIONS
# ============================================================

sock.close()
server.close()