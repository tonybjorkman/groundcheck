import socket
import sys


'''Messages from client to Exhalytic use one port and are answered on the same port,
Only one client can be connected to the port used for sending messages to the Exhalytics at any
time. '''
class ExhalyticStatusMonitor:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        self.sock:socket.socket = socket.create_connection((self.host, self.port))

    def send_message(self,message):
        self.sock.sendall(message)
        
    def recv_message(self):
        return self.sock.recv(1024)

    def close(self):
        self.sock.close()

'''
messages from Exhalytics that have not been requested are sent on a separate port.
 Any number of clients can be connected to the port for unrequested messages from
Exhalytics. 
'''
class ExhalyticsSampleReader:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.buffer = []

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        self.connection, address = self.sock.accept()
        print('Connected by', address)

    def receive(self):
        # accept connection
        self.connection, address = self.sock.accept()
        print('Connected by', address)
        data = self.connection.recv(1024)
        print('Received', repr(data))
        self.connection.sendall(data)

    def get_msgs(self):
        return self.buffer

    def close(self):
        self.connection.close()
        self.sock.close()

# Collects information from outside systems such as Unison and Exhalytics.

def poll_instrument_messages():
    pass

def poll_entrances():
    pass

def add_active_entrance(entrance):
    pass

def match_test_with_existing_entrances(test):
    pass