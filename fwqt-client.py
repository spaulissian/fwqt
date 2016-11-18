import sys
import socket
import threading
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *

# Test Firewall Client
# Sam Paulissian 
# create our window
app = QApplication(sys.argv)
w = QWidget()
w.setWindowTitle('Firewall Test Client')
txtresponse = '' 
# Create PortBox
portbox = QLineEdit(w)
portbox.move(20, 20)
portbox.resize(100,40)
ipbox = QLineEdit(w)
ipbox.move (160,20)
ipbox.resize(150,40)
l1 = QLabel(w)
l1.move (20,1)
l1.setText("Port")
l2 = QLabel(w)
l2.move (160,1)
l2.setText ("IP Address")
rcvbox = QLineEdit(w)
rcvbox.move (80, 80)
rcvbox.resize(300,150)
#rcvbox.setWordWrap(True)
 
# Set window size.
w.resize(420, 250)
 
# Create a button in the window
button = QPushButton('Send', w)
button.move(310,20)
btnclose = QPushButton('Exit', w)
btnclose.move (310,50)

layout = QVBoxLayout(w)

b1 = QRadioButton("TCP")
b1.setChecked(True)
layout.addWidget(b1)
b2 = QRadioButton("UDP")
b2.setChecked(False)
layout.addWidget(b2)

class myThread(threading.Thread):
   def __init__(self, threadID):
         threading.Thread.__init__(self)
         self.threadID = threadID
   def run(self):
    txtresponse = ''
    if b1.isChecked():
         # Create a TCP/IP socket
         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         # Bind the socket to the port
         server_address = (ipbox.text(), int(portbox.text()))
         try:
            sock.connect(server_address)
            sock.sendall(message)
            amount_received = 0
            amount_expected = len(message)
            while amount_received  < amount_expected:
                    data = sock.recv(16)
                    amount_received += len(data)
                    txtresponse = txtresponse + data
         except:
           txtresponse = "Error occured:  TCP " + ipbox.text() + ":" + portbox.text()
           print("Error occured.......")
         finally:
                  sock.close()
                  rcvbox.setText (txtresponse)
                  print("Sock Closed", txtresponse)
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (ipbox.text(), int(portbox.text()))
        print(server_address)
        try:
         sock.sendto(message,server_address)
         while True:
                amount_received = 0
                amount_expected = len(message)
                while amount_received < amount_expected:
                   data,client_address = sock.recvfrom(16)
                   txtresponse = txtresponse + data
        except:
              txtresponse = "Error occured: UDP " + ipbox.text() + ":" + portbox.text()
        finally:
                   rcvbox.setText(txtresponse)
                   sock.close()
                   print("Sock Closed", txtresponse)

message = "Message success: Sent and received message " 
# Create the actions
@pyqtSlot()
def on_click():

    if b1.isChecked():
       txtproto = "TCP"
    else:
       txtproto = "UDP"
    rcvbox.setText("Sending..."+ txtproto +" Port " + str(portbox.text()) + " IP: " + str(ipbox.text()))
    txtresponse = ''
    thread1 = myThread(1)
    thread1.start()
  
    print (txtresponse)

def on_exit():
    sys.exit()

# connect the signals to the slots
button.clicked.connect(on_click)

btnclose.clicked.connect(on_exit) 
# Show the window and run the app
w.show()
app.exec_()

