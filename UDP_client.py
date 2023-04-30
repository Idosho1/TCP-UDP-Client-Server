import sys
from socket import *
import datetime
 
# get number of arguments
num_arguments = len(sys.argv)

# expect 4 arguments + name of the program
if num_arguments != 5:
    print("Usage: python UDP_client.py <message> <server_ip> <server_port> <conection_id>")
    sys.exit(0)

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

    # create UDP socket
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    # send message to server in format: "HELLO <connection_id>"
    clientSocket.sendto(message.encode(),(serverIP, serverPort))

    # time out after 15 seconds if no reply is received
    clientSocket.settimeout(15)

    # try to get a reply without timeout
    try:
        # try to get a reply from the server
        try:
            reply, (address,port) = clientSocket.recvfrom(2048)
        except ConnectionResetError:
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

            # close the UDP socket
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

# close the UDP socket
clientSocket.close()

# exit gracefully
sys.exit(0)