import socket
#importing socket library

import threading
#importing threading library
#threading is used to run multiple task at same time

import _thread
#importing thread library
#thread is an infrastructure code used to implement threading
 
import time
#importing time module
#because we're going to use time sleep function

HOST = "192.168.0.135 "
#the ip adrr of the host (server ip addr)

PORT = 8023
#port used to connect between server and client
#telnet protocol port 23
 
def accept(conn):
#function in python is defined by def statement(function named accept)
    """
    Call the inner func in a thread so as not to block. Wait for a 
    name to be entered from the given connection. Once a name is 
    entered, set the connection to non-blocking and add the user to 
    the users dict.
    """
    def threaded():
    #defining function named threaded
        while True:
        #while loop,as long as the condition is true 
            conn.send(str.encode("Please enter your name: "))
            #conn.send, sending data from a socket to another socket
            #str.encode, converting string into byte
            #every sending process needs to be converted into byte
            try:
                name = conn.recv(1024).strip()
                name = name.decode("utf-8")
		#decode, convert byte to string
            except socket.error:
	    #try-except statements 
            #used for error & exception handling 
                continue
                #used to end the current iteration(while)
            if name in users:
                conn.send(str.encode("Name entered is already in use.\n"))
            elif name:
                conn.setblocking(False)
                users[name] = conn
                broadcast(name, "+++ %s arrived +++" % name)
                break
            #if else if statement
#    import _thread
    _thread.start_new_thread(threaded, ())
 
def broadcast(name, message):
#defining broadcast function
    """
    Send a message to all users from the given name.
    """
    print(message)
    #display messages by users

    for to_name, conn in users.items():
        if to_name != name:
           try:
               
                conn.send(str.encode(message + "\n"))
               
              
           except socket.error:
              pass
              #null statement
 
# Set up the server socket.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#TCP
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setblocking(False)
server.bind((HOST, PORT))
server.listen(1)
print ("Listening on %s" % ("%s:%s" % server.getsockname()))
 
# Main event loop.
users = {}
while True:
    try:
        # Accept new connections.
        while True:
            try:
                conn, addr = server.accept()
            except socket.error:
                break
            accept(conn)
        #read from connections
        for name, conn in users.items():
            try:
                message = conn.recv(1024)
            except socket.error:
                continue
            if not message:
                #empty string is given on disconnect
                del users[name]
                broadcast(name, "--- %s leaves ---" % name)
            else:
                message = message.decode("utf-8")
                #decode the message from byte to string
                broadcast(name, "%s> %s" % (name, message.strip()))
                #display the n ame along with the message
        time.sleep(.1)
	#time sleep function used to add delay in the program execution
    except (SystemExit, KeyboardInterrupt):
        break

