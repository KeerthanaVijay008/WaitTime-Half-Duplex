import json
import random
import task


def load_task_times():
    """Load automatically measured task times."""

    with open("task_times.json", "r") as file:
        task_times = json.load(file)

    return task_times


def choose_task(waiting_time, task_times, used_tasks=None):
    """
    Select a task that can fit inside the available
    waiting time.

    A task already used in the current experiment
    will not be selected again.
    """

    if used_tasks is None:
        used_tasks = set()

    suitable_tasks = []

    # Find tasks that fit within the waiting time
    for task_name, execution_time in task_times.items():

        if (
            execution_time <= waiting_time
            and task_name not in used_tasks
        ):
            suitable_tasks.append(
                (task_name, execution_time)
            )

    # No unused task can fit
    if not suitable_tasks:
        return None

    # Randomly select one of the suitable tasks
    selected_task = random.choice(suitable_tasks)

    # Remember that this task has been used
    used_tasks.add(selected_task[0])

    return selected_task


def execute_task(task_name):

    tasks = {
        "Calculate Checksum": task.calculate_checksum,
        "Process Data": task.process_data,
        "Update Log": task.update_log,
        "Prepare Data": task.prepare_data,
        "Quick Calculation": task.quick_calculation,
        "Small Data Check": task.small_data_check,
        "Update Status": task.update_status
    }

    if task_name not in tasks:
        return 0.0

    execution_time = tasks[task_name]()

    return execution_time