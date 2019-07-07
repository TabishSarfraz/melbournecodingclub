#!/usr/bin/env python3
# Python TCP Client A
import socket 

host = socket.gethostname() 
port = 2004
BUFFER_SIZE = 2000 
MESSAGE = input("tcpClientA: Enter message/ Enter exit:") 
 
tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpClientA.connect((host, port))

while MESSAGE != 'exit':
    tcpClientA.send(bytes(MESSAGE.encode()))     
    data = tcpClientA.recv(BUFFER_SIZE)
    print (" Client2 received data:", str(data))
    MESSAGE = input("tcpClientA: Enter message to continue/ Enter exit:")

tcpClientA.close() 
