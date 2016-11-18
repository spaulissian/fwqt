# fwqt
CS 6250 Project 7 - Firewall GUI Client/Server
#
# CS 6250 - Project 7 required manually loading a server files for testing TCP and UDP ports.  Also required loading
# client side files to match the protocol and Port.
#
# My goal was to have a GUI Client and Server application where on the server side you would change the Protocol and Port
# If the Server App was listening on UDP Port 1234 you could change to TCP Port 8080 and clicking Listen.  The idea is to close
# UDP Port 1234 and then start listening on TCP port 8080.
#
# On the client side you would put in a Server IP, port and Protocol to send a message to and it would respond with a success or
# failure.  This would be a lot faster in testing the firewall rules of Project 7.
#  
#   Theoretically on one host you can run both the cleint and server program so long as your not trying to listen on the same port
# your sending on.  I.e. if the server is listening on TCP 8080, you might not be able to send a test from the client to another machine
# on TCP port 8080

