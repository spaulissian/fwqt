import sys
import socket
import threading
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *

# Test Firewall Server
# Sam Paulissian 
# create our window
app = QApplication(sys.argv)
w = QWidget()
title = "Firewall Test Server " + str(sys.argv[1])
w.setWindowTitle(title)
txtresponse = '' 
# Create PortBox
portbox = QLineEdit(w)
portbox.move(20, 20)
portbox.resize(100,40)
l1 = QLabel(w)
l1.move (20,1)
l1.setText("Port")
rcvbox = QLineEdit(w)
rcvbox.move (80, 80)
rcvbox.resize(300,150)
 
# Set window size.
w.resize(420, 250)
 
# Create a button in the window
button = QPushButton('Listen', w)
button.move(160,20)
btnclose = QPushButton('Exit', w)
btnclose.move (260,20)

layout = QVBoxLayout(w)

b1 = QRadioButton("TCP")
b1.setChecked(True)
layout.addWidget(b1)
b2 = QRadioButton("UDP")
b2.setChecked(False)
layout.addWidget(b2)
blListen = True

class myThread(threading.Thread):
   def __init__(self, threadID):
         threading.Thread.__init__(self)
         self.threadID = threadID
   def run(self):
       blListen=True
       txtresponse = ''
       if b1.isChecked():
         # Create a TCP/IP socket
         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         #sock.close()
         # Bind the socket to the port
         server_address = (sys.argv[1], int(portbox.text()))
         sock.bind(server_address)
         sock.listen(1)
         while blListen:
             connection, client_address = sock.accept()
             try:
                while True:
                    data = connection.recv(16)
                    txtresponse = txtresponse + data
                    rcvbox.setText (txtresponse)
                    if data:
                       connection.sendall(data)
                    else:
                       break
             except:
                  txtresponse = "Something went wrong..."
                  rcvbox.setText (txtresponse)
             finally:
                  connection.close()
       else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #sock.close()
        server_address = (sys.argv[1], int(portbox.text()))
        sock.bind(server_address)
        #host = socket.gethostname() #Get the local machine name
        #port = int(portbox.text()) # Reserve a port for your service
        #sock.bind((host,port)) #Bind to the port
        while blListen:
           try:
                   data,client_address = sock.recvfrom(32)
                   txtresponse = txtresponse + data
                   rcvbox.setText (txtresponse)
                   if data:
                      sock.sendto(data,client_address)
                   else:
                      break
           finally:
                  txtresponse = txtresponse + '-' + "Finished"
                  rcvbox.setText (txtresponse)
                  sock.close()

# Create the actions
@pyqtSlot()
def on_click():
    msg = "waiting for a connection on "
    if b1.isChecked():
        msg = msg + "TCP port "
    else:
        msg = msg + "UDP port "
    msg = msg + portbox.text()
    rcvbox.setText(msg)
    blListen = False
    thread1 = myThread(1)
    thread1.start()

def on_exit():
    blListen = False
    sys.exit()

# connect the signals to the slots
button.clicked.connect(on_click)

btnclose.clicked.connect(on_exit) 
# Show the window and run the app
if sys.argv < 3:
     print ("Usage:  python fwqt-server.py <ip address>")
     sys.exit()
w.show()
app.exec_()

