import socket, os, json, time
from collections import Counter

SOCKET_PATH = '/tmp/ipc_socket2'

# Remove old socket file if exists
if os.path.exists(SOCKET_PATH):
    os.remove(SOCKET_PATH)

# Create Unix domain socket
server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(SOCKET_PATH)
server.listen(1)
print("[Server] Waiting for log data...")

# Accept connection from client
conn, _ = server.accept()
start = time.time()

raw = b""
while True:
    chunk = conn.recv(4096)
    if not chunk:
        break
    raw += chunk

# Decode the eceived  message
log = raw.decode()
print(f"[Server] Received log message: {log}")

# Analyse the text
words = log.lower().split()
total_words = len(words)
unique_words = len(set(words))
most_common = Counter(words).most_common(1)[0]

print(f"[Server] Total words:   {total_words}")
print(f"[Server] Unique words:  {unique_words}")
print(f"[Server] Most frequent: '{most_common[0]}' ({most_common[1]} times)")

# Send results back to client
result = json.dumps({
    "total_words": total_words,
    "unique_words": unique_words,
    "most_frequent_word": most_common[0],
    "most_frequent_count": most_common[1]
})
conn.send(result.encode())

print(f"[Server] Processing time: {round(time.time()-start, 4)} seconds")
conn.close()
server.close()
