# flask is used for reciving commands through web api or url
# socket is used connect server and client

import socket 
import threading
from flask import Flask, request, json, abort

app = Flask(__name__)

sign_out_pc=False
shutdown=False
press_space=False
press_alt_f4=0
press_enter=False


#change ip to your system ip andd port on which you want to run different port  
HEADER = 64
SERVER = "192.168.xx.xx" #socket ip
PORT = 5050 #server listen port
# change WEBHOOK_PORT use webhook with different port
WEBHOOK_PORT=8080 #Webhook port

ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
except:
    with socket.error as e:
        print(str(e))



# signout pc
@app.route('/signout', methods=['POST'])
def sign_out():
    global sign_out_pc
    if request.method == 'POST':
        if ((threading.active_count() - 3)>0):
            sign_out_pc=True
            return "out"
        else:
            return 'system is offline'
    else:
        abort(400)
    
# shutdown pc
@app.route('/shutdown', methods=['POST'])
def shutdown_pc():
    global shutdown
    if request.method == 'POST':
        if ((threading.active_count() - 3)>0):
            shutdown=True
            return 'shutdown'
        else:
            return 'system is offline'
    else:
        abort(400)

# press spacebar
@app.route('/space',methods=['POST'])
def press_space_():
    global press_space
    if request.method == 'POST':
        if ((threading.active_count() - 3)>0):
            press_space=True
            return 'spacebar pressed'
        else:
            return 'system is offline'
    else:
        abort(400)

# press ALT+F4
@app.route('/altf4',methods=['POST'])
def press_altf4():
    global press_alt_f4
    if request.method == 'POST':
        if ((threading.active_count() - 3)>0):
            press_alt_f4=True
            return 'alt f4 pressed'
        else:
            return 'system is offline'
    else:
        abort(400)

# press ENTER
@app.route('/enter',methods=['POST'])
def enter_space():
    global press_enter
    if request.method == 'POST':
        if ((threading.active_count() - 3)>0):
            press_enter=True
            return 'enter pressed'
        else:
            return 'system is offline'   
    else:
        abort(400)

@app.route('/check_online',methods=['POST'])
def checkOnline():
    if request.method == 'POST':
        if ((threading.active_count() - 3)==0):
            return 'system is offline' 
            

def handle_client(connection_socket, addr):
    global sign_out_pc
    global shutdown
    global press_space
    global press_alt_f4
    global press_enter

    connection_socket.setblocking(False)
    connection_socket.settimeout(1)

    print(f"\n\033[0;33m[NEW CONNECTION REQUEST] {addr}\033[0m")

    hostname=connection_socket.recv(HEADER).decode(FORMAT)
    print(f"\033[1;34m{hostname}\033[0m is trying to connect")
    print(f"\033[0;32m[CONNECTION ESTABLISHED]\033[0m with \033[1;34m{hostname}\n\033[0m")

    connected = True
    while connected:
        try:
            hostname=connection_socket.recv(HEADER).decode(FORMAT)
        except Exception as e:
            if "An existing connection was forcibly closed by the remote host" in str(e):
                print(f"\033[1;31m[ERROR]\033[1;34m\n{hostname}\033[1;31m crashed or shutdown manually or client application force closed\033[0m\n")
                print(f"\033[1;31mClosing connection with \033[1;34m{hostname}\033[0m\n")
                break
            elif "Connection reset by peer" in str(e):
                print(f"\033[1;31m[ERROR]\033[1;34m\n{hostname}\033[1;31m crashed or shutdown manually or client application force closed\033[0m\n")
                print(f"\033[1;31mClosing connection with \033[1;34m{hostname}\033[0m\n")
                break
            else:
                pass
                
        
        if sign_out_pc:
            connection_socket.send("sign_out".encode(FORMAT))
            msg = connection_socket.recv(HEADER).decode(FORMAT)
            print(f"\033[1;34m[{addr[0]}]\033[0m {msg}\n")
            sign_out_pc=False
            break

        if shutdown:
            connection_socket.send("shutdown".encode(FORMAT))
            msg = connection_socket.recv(HEADER).decode(FORMAT)
            print(f"\033[1;34m[{addr[0]}]\033[0m {msg}\n")
            shutdown=False
            break

        if press_space:
            connection_socket.send("press_space".encode(FORMAT))
            msg = connection_socket.recv(HEADER).decode(FORMAT)
            print(f"\033[1;34m[{addr[0]}]\033[0m {msg}\n")
            press_space=False

        if press_alt_f4:
            connection_socket.send("press_alt_f4".encode(FORMAT))
            msg = connection_socket.recv(HEADER).decode(FORMAT)
            print(f"\033[1;34m[{addr[0]}]\033[0m {msg}\n")
            press_alt_f4=False

        if press_enter:
            connection_socket.send("press_enter".encode(FORMAT))
            msg = connection_socket.recv(HEADER).decode(FORMAT)
            print(f"\033[1;34m[{addr[0]}]\033[0m {msg}\n")
            press_enter=False

def exeption_override(args):
    print("Error Occure")
    print(args[1])
    print(args[3])
    print("\n")

def flask_server():
    #server ip and port 
    app.run(host=SERVER,port=WEBHOOK_PORT)

def start():
    server.listen(2)
    print(f"\033[0;32m[LISTENING]\033[0m Server is listening on {SERVER}")
    threading.Thread(target=flask_server).start()
    print("\n")
    while True:
        connection_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection_socket, addr))
        thread.start()
        print(f"\033[0;32m[ACTIVE CONNECTIONS]\033[0m {threading.active_count() - 2}\n")

threading.excepthook=exeption_override
print("\033[0;32m[STARTING]\033[0m Server is starting...")
start()