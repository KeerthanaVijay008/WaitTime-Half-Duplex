import time


def quick_calculation():
    start = time.perf_counter()

    total = 0

    for i in range(1000):
        total += i * i

    end = time.perf_counter()

    return end - start


def small_data_check():
    start = time.perf_counter()

    total = 0

    for i in range(5000):
        total += i

    end = time.perf_counter()

    return end - start


def update_status():
    start = time.perf_counter()

    status = {
        "device": "B",
        "status": "ready"
    }

    current_status = status["status"]

    # Small local processing
    for i in range(1000):
        current_status = current_status

    end = time.perf_counter()

    return end - start


def update_log():
    start = time.perf_counter()

    total = 0

    for i in range(10000):
        total += i * 2

    end = time.perf_counter()

    return end - start


def prepare_data():
    start = time.perf_counter()

    data = []

    for i in range(50000):
        data.append(i * 2)

    end = time.perf_counter()

    return end - start


def calculate_checksum():
    start = time.perf_counter()

    total = 0

    for i in range(150000):
        total += i

    end = time.perf_counter()

    return end - start


def process_data():
    start = time.perf_counter()

    data = []

    for i in range(250000):
        data.append(i * 2)

    # Perform additional processing
    total = sum(data)

    end = time.perf_counter()

    return end - start