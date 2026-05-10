import socket
import json
import random
import time

SOCKET_PATH = '/tmp/ipc_socket'

# Generate 50 random values
vals = [round(random.uniform(1,100),2) for _ in range(50)]
print(f"[Client] Sending {len(vals)} values to server: {vals}")
print(f"[Client] Values: {vals}")

client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

client.connect(SOCKET_PATH)

# Start timer and send values to servber
start_time = time.time()
client.send(json.dumps(vals).encode())

# Shutdowm so server knows client done
client.shutdown(socket.SHUT_WR)

# Get results back from server
raw = b""
while True:
	part = client.recv(4096)
	if not part:
		break
	raw += part

end_time = time.time()

# Display results
stats = json.loads(raw.decode())
print(f"[Client] Results received from server:")
print(f" Mean:      {stats['mean']:.4f}")
print(f" Median:    {stats['median']:.4f}")
print(f" Std Dev:   {stats['std_dev']:.4f}")
print(f" Time taken: {(end_time - start_time)*1000:.2f} ms")


client.close()
