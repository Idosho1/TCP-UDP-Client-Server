import sys
from socket import *
import time

# get number of arguments
num_arguments = len(sys.argv)

# expect 4 arguments + name of the program
if num_arguments != 3:
    print("Usage: python UDP_server.py <server_ip> <server_port>")
    sys.exit(0)

# get IP and Port from arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

# create TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# close the TCP socket after 2 minutes of inactivity
serverSocket.settimeout(120)

# bind the socket to the port
serverSocket.bind((serverIP, serverPort))

# listen for incoming connections
serverSocket.listen(1)
  
# keep track on connected clients
connectionIDs = {}

# continue to receive messages
while True:
    
    # remove connection ids that have been in the list for more than 30 seconds
    # casting the dictionary to a list so that items can be removed while iterating (Found suggestion on a stackoverflow post)
    for connectionID, t in list(connectionIDs.items()):
        if time.time() - t > 30:
            del connectionIDs[connectionID]

    # try to accept a connection without timeout
    try:
        # accept incoming connection
        connectionSocket, (client_address, client_port) = serverSocket.accept()

        # receive message from client
        message = connectionSocket.recv(1024)

        # decode the message in format "HELLO <connection_id>"
        message = message.decode()
        
        # get connection id from message
        connectionID = message.split(" ")[1]
        
        # create the reply
        reply = ""
        
        # if the connection id is not in the list
        if connectionID not in connectionIDs:
            reply = "OK " + str(connectionID) + " " + str(client_address) + " " + str(client_port)
            connectionIDs[connectionID] = time.time()
        else:
            reply = "RESET " + connectionID
        
        # send reply to client
        connectionSocket.send(reply.encode())

        # close the connection
        connectionSocket.close()

    except timeout:
        # if the socket times out, close it
        serverSocket.close()
        print("Socket timed out")
        sys.exit(0)