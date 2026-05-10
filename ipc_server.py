import socket
import os
import json
import statistics, time

SOCKET_PATH = '/tmp/ipc_socket'

# Removes old socket file
if os.path.exists(SOCKET_PATH):
	os.remove(SOCKET_PATH)

# Creats Unix domain socket
server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(SOCKET_PATH)
server.listen(1)
print("[Server] Waiting for data...")

# Accepts connection from client
conn, _ = server.accept()
start = time.time()

# Receives data in intervals till client finished sending
raw = b""
while True:
	part = conn.recv(4096)
	if not part:
		break
	raw += part

values = json.loads(raw.decode())
print(f"[Server] Received {len(values)} values: {values}")

# Get stats
mean = statistics.mean(values)
median = statistics.median(values)
std_dev = statistics.stdev(values)

print(f"[Server] Mean:        {mean:.4f}")
print(f"[Server] Median:      {median:.4f}")
print(f"[Server] Std Dev:     {std_dev:.4f}")

# Send stats back to client
stats = {"mean": mean, "median": median, "std_dev": std_dev}
conn.send(json.dumps(stats).encode())

print(f"[Server] processing time: {round(time.time()-start, 4)} seconds")
conn.close()
server.close()
