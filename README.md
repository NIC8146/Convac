
# Convac

**Now only one client file for both linux and windows**

**linux files does not support sign out and notifications**

Convac is python webhook and socket based tool to execute important and minimum tasks in remote system.

Convac_client.py is only for windows system not tested for linux.

* **You need a system to run as server with static ip and run continuously** 



## Benefits

Control your remort system with some webhook links

Here **192.168.xx.xx** is server ip and **yyyy** is port on which flask_server is running default is 8080 .
send port requests to any following url for specific opration.

* **192.168.xx.xx:yyyy/shutdown** to shutdown remort system

* **192.168.xx.xx:yyyy/signout** to signout remort system

* **192.168.xx.xx:yyyy/space** to press space bar on remort system 

* **192.168.xx.xx:yyyy/altf4** to press Alt+F4 on remort system

* **192.168.xx.xx:yyyy/enter** to press ENTER on remort system

* **192.168.xx.xx:yyyy/check_online** to check online status of remort system


## Requirments

To install required pakages for both **client** and **server** run following command.
```bash
pip install -r requirments.txt
```
# Setup
Clone the project

```bash
  git clone https://github.com/NIC8146/Convac.git
```

Go to the project directory

```bash
  cd Convac
```

First of all you need do some shanges in both client and server file.

* In Convac_client.py change ip named as variable **SERVER** variable you also can change port names as **PORT** variable.
Note that **PORT** in Convac_client.py should be as same as socket listen **PORT** on server

* In Convac_server.py change ip of server named as variable **SERVER** and port of server named as variable **PORT** 

# 
Convac_client.py is python file which used promte or terminal to run and it is not good to open terminal on every startup and remain opened.

So convert it to .exe file which run on startup with opening terminal on screen.

**To convert it to .exe**

install **pyinstaller** utility by following command. 
```bash
pip install pyinstaller
```

**convert python file to .exe by following command**
```bash
pyinstaller -i "client.ico" --onefile -w "Convac_client.py"
```
after completing the process inside "dist" directory you found **Convac_client.exe** .

Copy the **Convac_client.exe** to  **c:\temp\\** directory.

#
Use task sheduler to run Convac_client.exe on startup on system you want to control.

On server system just run **Convac_server.py** by following command.
```bash
python3 Convac_server.py

```
or
```bash
python Convac_server.py
```

and you are good to go.
