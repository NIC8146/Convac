import os
from pynput.keyboard import Key, Controller
from flask import Flask, request, json, abort
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

app = Flask(__name__)
keyboard = Controller()

#change port on which you want to run different port  
SERVER = "192.168.1.2" #socket ip
# change WEBHOOK_PORT use webhook with different port
WEBHOOK_PORT=8080 #Webhook port

# signout pc
@app.route('/signout', methods=['POST'])
def sign_out():
    if request.method == 'POST':
        if win:
            os.system("rundll32.exe user32.dll,LockWorkStation")
        elif linux:
            # not working
            pass
        return "out"
    else:
        abort(400)
    
# shutdown pc
@app.route('/shutdown', methods=['POST'])
def shutdown_pc():
    if request.method == 'POST':
        if win:
            os.system("shutdown /s /t 0")
        elif linux:
            os.system("poweroff")
        return 'shutdown'
    else:
        abort(400)

# press spacebar
@app.route('/space',methods=['POST'])
def press_space_():
    
    if request.method == 'POST':
        keyboard.press(Key.space)
        keyboard.release(Key.space)
        return 'spacebar pressed'
    else:
        abort(400)

# press ALT+F4
@app.route('/altf4',methods=['POST'])
def press_altf4():

    if request.method == 'POST':
        keyboard.press(Key.alt)
        keyboard.press(Key.f4)
        keyboard.release(Key.f4)
        keyboard.release(Key.alt)
        return 'alt f4 pressed'
    else:
        abort(400)

# press ENTER
@app.route('/enter',methods=['POST'])
def enter_space():
    
    if request.method == 'POST':
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        return 'enter pressed'
    else:
        abort(400)

@app.route('/check_online',methods=['POST'])
def checkOnline():
    return 'system is online' 

def flask_server():
    #server ip and port 
    app.run(host=SERVER,port=WEBHOOK_PORT)

if ( __name__ == "__main__" ):
    flask_server()