import json
import task


def benchmark_task(task_function, runs=3):
    """Measure the average execution time of a task."""

    total_time = 0.0

    for _ in range(runs):
        execution_time = task_function()
        total_time += execution_time

    return total_time / runs


def create_timetable():

    tasks = {
    "Calculate Checksum": task.calculate_checksum,
    "Process Data": task.process_data,
    "Update Log": task.update_log,
    "Prepare Data": task.prepare_data,
    "Quick Calculation": task.quick_calculation,
    "Small Data Check": task.small_data_check,
    "Update Status": task.update_status
}

    timetable = {}

    print("Creating task timetable...\n")

    for task_name, task_function in tasks.items():

        average_time = benchmark_task(task_function)

        timetable[task_name] = average_time

        print(
            f"{task_name}: "
            f"{average_time:.6f} seconds"
        )

    # Save timetable to a JSON file
    with open("task_times.json", "w") as file:
        json.dump(timetable, file, indent=4)

    print("\nTask timetable saved to task_times.json")

    return timetable


if __name__ == "__main__":

    timetable = create_timetable()

    print("\n==============================")
    print("       TASK TIMETABLE")
    print("==============================")

    for task_name, execution_time in timetable.items():

        print(
            f"{task_name}: "
            f"{execution_time:.6f} seconds"
        )