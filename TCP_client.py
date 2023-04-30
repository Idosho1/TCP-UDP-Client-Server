import sys
from socket import *
import datetime
 
# get number of arguments
num_arguments = len(sys.argv)

# expect 4 arguments + name of the program
if num_arguments != 5:
    print("Usage: python UDP_client.py <message> <server_ip> <server_port> <conection_id>")
    sys.exit(1)

# get IP and Port from arguments
serverIP = sys.argv[2]
serverPort = int(sys.argv[3])

# get connection id from arguments
connectionID = sys.argv[4]

# get message from arguments
message = sys.argv[1] + " " + connectionID

# count the number of retries left
retries = 4
first = True

while retries > 0:

    # remove a retry
    retries -= 1

    # if this is not the first retry prompt for new connection id
    if first:
        first = False
    else:
        connectionID = input("Enter new connection id: ")
        message = sys.argv[1] + " " + connectionID

    # create TCP socket
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # try to connect to the server
    try:
        clientSocket.connect((serverIP, serverPort))
    except ConnectionRefusedError:
        # exit gracefully
        retries = 0
        continue

    # send message to server in format: "HELLO <connection_id>"
    clientSocket.send(message.encode())

    # time out after 15 seconds if no reply is received
    clientSocket.settimeout(15)

    # try to get a reply without timeout
    try:
        # try to get a reply from the server
        try:
            reply = clientSocket.recv(1024)
        except ConnectionRefusedError:
            print("Connection Error " + connectionID + " on " + str(datetime.datetime.now()))

            # retry connection
            continue

        # decode the message
        reply = reply.decode()

        # split the reply
        reply = reply.split(" ")
        reply_status = reply[0]

        # if the reply is OK
        if reply_status == "OK":

            # get values from reply
            reply_connectionID = reply[1]
            reply_clientIP = reply[2]
            reply_clientPort = reply[3]

            print("Connection established " + reply_connectionID + " " + reply_clientIP + " " + reply_clientPort + " on " + str(datetime.datetime.now()))

            # close the TCP socket
            clientSocket.close()
            
            # exit gracefully
            sys.exit(0)

        elif reply_status == "RESET":
            print("Connection Error " + connectionID + " on " + str(datetime.datetime.now()))

            # retry connection
            continue
    
    except timeout:
        print("Connection Error " + connectionID + " on " + str(datetime.datetime.now()))

        # retry connection
        continue

# if all the retries have failed, exit
print("Connection Failure on " + str(datetime.datetime.now()))

# close the TCP socket
clientSocket.close()

# exit gracefully
sys.exit(0)