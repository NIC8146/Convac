import socket
from pynput.keyboard import Key, Controller
import os
from sys import platform

if platform == "linux" or platform == "linux2":
    # if os is linux
    linux = True
    win = False
elif platform == "win32":
    # in os is windows
    linux = False
    win = True
    from winotify import Notification

keyboard = Controller()

HEADER = 64
SERVER = "192.168.1.10" #server ip address
PORT = 5050 #port same as server listen port
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    client.setblocking(False)
    client.settimeout(1)

    client.send(socket.gethostname().encode(FORMAT))

    def send(msg):
        message = msg.encode(FORMAT)
        client.send(message)
        print(client.recv(HEADER).decode(FORMAT))

    while True:
        try:
            command=client.recv(HEADER).decode(FORMAT)
        except:
            command=False
        
        if command:

            if command=="sign_out":
                client.send(f"\033[1;34m{socket.gethostname()}\033[1;35m is signing out\033[0m".encode(FORMAT))
                client.close()
                if win:
                    os.system("rundll32.exe user32.dll,LockWorkStation")
                elif linux:
                    # not working
                    pass

            if command=="shutdown":
                client.send(f"\033[1;34m{socket.gethostname()}\033[1;35m is Shutting down\033[0m".encode(FORMAT))
                client.close()
                if win:
                    os.system("shutdown /s /t 0")
                elif linux:
                    os.system("poweroff")

            if command=="press_space":
                keyboard.press(Key.space)
                keyboard.release(Key.space)
                client.send(f"\033[1;34m[{socket.gethostname()}]\033[1;35m SPACEBAR pressed\033[0m".encode(FORMAT))

            if command=="press_alt_f4":
                keyboard.press(Key.alt)
                keyboard.press(Key.f4)
                keyboard.release(Key.f4)
                keyboard.release(Key.alt)
                client.send(f"\033[1;34m[{socket.gethostname()}]\033[1;35m Alt + f4 is pressed\033[0m".encode(FORMAT))

            if command=="press_enter":
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
                client.send(f"\033[1;34m[{socket.gethostname()}]\033[1;35m ENTER key pressed\033[0m".encode(FORMAT))

except Exception as e:
    if win:
        if "No connection could be made because the target machine actively refused it" in str(e):
            notif = Notification(app_id="Convac",title="Connection Error",msg="server is not working or under maintenence")
            notif.show()
    elif linux:
        # not working
        pass