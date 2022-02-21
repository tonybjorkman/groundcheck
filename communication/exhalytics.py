import socket
import select
import sys
import threading
from types import SimpleNamespace


'''Messages from client to Exhalytic use one port and are answered on the same port,
Only one client can be connected to the port used for sending messages to the Exhalytics at any
time.

1.connects to targets
2.sends statusrequest to targets with ping_instrument()
3.responses are interpreted into a status for each target
4.print all statuses with print_status_list() 

 '''
class ExhalyticStatusMonitor:

    class Target:
        def __init__(self,host,port):
            self.host = host
            self.port = port
            self.connected = False
            self.status = 'not connected'
            self.socket = None

        def __str__(self) -> str:
            return 'host:'+self.host+'port:'+str(self.port)+'connected:'+str(self.connected)+'status:'+str(self.status)

    def __init__(self):
        self.buffer = []
        self.targets = []
        print("created status monitor")

    def add_target(self, host, port):
        target = self.Target(host, port)
        self.targets.append(target) 

    def print_target_statuslist(self):
        for t in self.targets:
            if t is not None:
                print(t)
            else:
                print("target is None")

    def connect_to_targets(self):
        for t in self.targets:
            if not t.connected:
                try:
                    t.socket = socket.create_connection((t.host, t.port))
                    t.connected = True
                except:
                    print("Could not connect to target on port:"+str(t.port))
                    t.connected = False

    def update_target_statuses(self):
        for t in self.targets:
            try:
                response = self.ping_instrument(t, "minping")
                if response == 'minping':
                    t.status = 'OK'
                elif response == 'error':
                    t.status = 'Error'
                elif response is None:
                    t.status = 'not connected'
            except:
                t.status = 'not connected'
                t.connected = False
    
    def ping_instrument(self,target,message):
        print("Monitor making status-request:"+message)
        if target.connected: 
            try:
                target.socket.sendall(message.encode())
                data = target.socket.recv(1024).decode()
                print("Got status-response:"+data)
            except: 
                print("Could not send status-request to target on port:"+str(target.port))
                target.connected = False
            return data
        return None

    def get_buffer(self):
        return self.buffer

    def close(self): 
        for t in self.targets:
            t.socket.close()
            print("closed socket for target on port:"+str(t.port))

'''
messages from Exhalytics that have not been requested are sent on a separate port.
 Any number of clients can be connected to the port for unrequested messages from
Exhalytics.

1new thread
2Wait for single connection
3Read msg from connection into buffer
4buffer grabbed with get_msgs()

'''
class ExhalyticsSampleReader:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.buffer = []
        self.thread = None
        self.cancelled = False

    def start_run_thread(self):
        self.thread = threading.Thread(target=self.wait_for_connection)
        self.thread.daemon = True
        self.thread.start()

    def wait_for_connection(self):
        print("waiting for connection")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        self.connection, address = self.sock.accept()
        self.connection.setblocking(False)
        print('Connected by', address)
        self.run()

    def run(self):
        print("Running")
        timeout_in_seconds = 1
        while not self.cancelled: 
            ready = select.select([self.connection], [], [], timeout_in_seconds)
            if ready[0]:
                data = self.connection.recv(4096)
                #skip empty byte from timeout
                if data != b'':
                    print('Received', repr(data))
                    self.buffer.append(data.decode())
            else:
                print("Nothing received") 
        print("exited exhalytic listener")

        self.connection.close()
        self.sock.close()

    def get_msgs(self):
        return self.buffer

    def close(self):
        self.cancelled = True

# Collects information from outside systems such as Unison and Exhalytics.

def poll_instrument_messages():
    pass

def poll_entrances():
    pass

def add_active_entrance(entrance):
    pass

def match_test_with_existing_entrances(test):
    pass