import socket
import time

HOST = "127.0.0.1"
PORT = 5001
ROUNDS = 3

DATA_SIZE = 1024 * 1024   # 1 MB


# ==================================
# CONNECT TO DEVICE B
# ==================================

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

sock.connect(
    (HOST, PORT)
)


# ==================================
# COMMUNICATION
# ==================================

data_block = b"A" * DATA_SIZE

total_transmission_time = 0.0
total_waiting_time = 0.0


for round_no in range(1, ROUNDS + 1):

    # --------------------------------
    # A sends data to B
    # --------------------------------

    transmission_start = time.perf_counter()

    sock.sendall(data_block)

    transmission_end = time.perf_counter()

    transmission_time = (
        transmission_end
        - transmission_start
    )

    total_transmission_time += (
        transmission_time
    )


    # --------------------------------
    # A waits for B
    # --------------------------------

    waiting_start = time.perf_counter()

    message = sock.recv(1024)

    waiting_end = time.perf_counter()

    waiting_time = (
        waiting_end
        - waiting_start
    )

    total_waiting_time += (
        waiting_time
    )


# ==================================
# FINAL RESULTS
# ==================================

print()
print("=" * 70)
print(
    "                     DEVICE A RESULTS"
)
print("=" * 70)

print(
    f"Total Transmission Time : "
    f"{total_transmission_time:.6f} seconds"
)

print(
    f"Total Waiting Time      : "
    f"{total_waiting_time:.6f} seconds"
)

print("=" * 70)


# ==================================
# CLOSE CONNECTION
# ==================================

sock.close()