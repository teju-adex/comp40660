import socket, json, time

SOCKET_PATH = '/tmp/ipc_socket2'

# Log message representing IoT device logs sent from edge device
log_message = (
    "error connection timeout error network error "
    "connection failed retry connection timeout "
    "error packet loss network error timeout "
    "retry failed error connection error network "
    "timeout connection retry error failed network"
)

print(f"[Client] Sending log message to server for analysis...")
print(f"[Client] Log: {log_message}")

# Create Unix domain socket and connect to server
client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
client.connect(SOCKET_PATH)

# Send log message and close write end
start_time = time.time()
client.send(log_message.encode())
client.shutdown(socket.SHUT_WR)

# Receive results back from server in chunks
raw = b""
while True:
    chunk = client.recv(4096)
    if not chunk:
        break
    raw += chunk

end_time = time.time()

# Parse and display results
result = json.loads(raw.decode())
print(f"\n[Client] Results received from server:")
print(f"  Total words:      {result['total_words']}")
print(f"  Unique words:     {result['unique_words']}")
print(f"  Most frequent:    '{result['most_frequent_word']}' ({result['most_frequent_count']} times)")
print(f"  Offloading time:  {(end_time - start_time)*1000:.2f} ms")

client.close()
