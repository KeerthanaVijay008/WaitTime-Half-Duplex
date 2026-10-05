import socket
import time

HOST = "127.0.0.1"
PORT = 5000
ROUNDS = 5

# Create server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen(1)

print("Device B waiting for Device A...")

sock, address = server.accept()

print("Device A connected")
print("Starting half-duplex communication...\n")

total_waiting_time = 0.0
total_transmission_time = 0.0

for round_no in range(1, ROUNDS + 1):

    print(f"--- Round {round_no} ---")

    # -----------------------------
    # B waits for A's data
    # -----------------------------
    print("B: Waiting for A's data...")

    waiting_start = time.perf_counter()

    data = sock.recv(1024)

    waiting_end = time.perf_counter()

    waiting_time = waiting_end - waiting_start

    total_waiting_time += waiting_time

    print(
        f"B waiting time: "
        f"{waiting_time:.6f} seconds"
    )

    # -----------------------------
    # Acknowledgement
    # -----------------------------
    sock.sendall(b"ACK")

    # -----------------------------
    # B transmits
    # -----------------------------
    message = f"DATA_FROM_B_ROUND_{round_no}".encode()

    transmission_start = time.perf_counter()

    sock.sendall(message)

    transmission_end = time.perf_counter()

    transmission_time = (
        transmission_end - transmission_start
    )

    total_transmission_time += transmission_time

    print(
        f"B transmission time: "
        f"{transmission_time:.6f} seconds"
    )

    # -----------------------------
    # Give turn back to A
    # -----------------------------
    sock.sendall(b"TURN_TO_A")

    print()

# -----------------------------
# Final results
# -----------------------------

print("==============================")
print("       DEVICE B RESULTS")
print("==============================")

print(
    f"Total transmission time: "
    f"{total_transmission_time:.6f} seconds"
)

print(
    f"Total waiting time: "
    f"{total_waiting_time:.6f} seconds"
)

sock.close()
server.close()