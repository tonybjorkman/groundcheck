import socket
import select
import sys
import threading
import time
from types import SimpleNamespace


'''Messages from client to Exhalytic use one port and are answered on the same port,
Only one client can be connected to the port used for sending messages to the Exhalytics at any
time.

1.connects to targets
2.sends statusrequest to targets with ping_instrument()
3.responses are interpreted into a status for each target
4.print all statuses with print_status_list() 

 '''
class Event(object):
    pass

class Observable(object):
    def __init__(self):
        self.callbacks = []
    def subscribe(self, callback):
        self.callbacks.append(callback)
    def fire(self, **attrs):
        e = Event()
        e.source = self
        for k, v in attrs.items():
            setattr(e, k, attrs[k])
        for fn in self.callbacks:
            fn(e)

class ExhalyticStatusMonitor(Observable):

    class Target:
        def __init__(self,host,port):
            self.host = host
            self.port = port
            self.connected = False
            self.status = 'NO_CONNECTION'
            self.socket = None

        def __str__(self) -> str:
            return 'host:'+self.host+'port:'+str(self.port)+'connected:'+str(self.connected)+'status:'+str(self.status)

    def __init__(self):
        self.buffer = []
        self.targets = []
        self.thread = None
        self.cancelled = False
        self.callbacks = []
        self.prev_target_statuses = []
        print("created status monitor")

    def start_run_thread(self):
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()
        return self.thread

    def _run(self,sample_interval=5):
        next_tick = time.time()+sample_interval
        while not self.cancelled:
            if time.time() > next_tick:
                self.connect_to_targets()
                self.update_target_statuses()
                if self.has_targets_changed():
                    self.fire(event_type='target_change')
                self.print_target_statuslist()
                self.fire(event_type='tick')
                next_tick = time.time() + sample_interval                    
            time.sleep(1)

    def add_target(self, host, port):
        target = self.Target(host, port)
        self.targets.append(target)
        #prevent this change from triggering change event
        self.prev_target_statuses = self._get_target_statuses() 

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

    def _get_target_statuses(self):
        return [t.status for t in self.targets]
    
    def has_targets_changed(self):
        target_statuses = self._get_target_statuses()
        if target_statuses != self.prev_target_statuses:
            self.prev_target_statuses = target_statuses
            return True
        return False

    def update_target_statuses(self):
        for t in self.targets:
            try:
                response = self.ping_instrument(t, "STATUS?")
                if response is not None:
                    t.status = response
            except:
                t.status = 'NO_CONNECTION'
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

    def _close(self): 
        for t in self.targets:
            if t.socket is not None:
                t.socket.close()
            print("closed socket for target on port:"+str(t.port))
    
    def cancel(self):
        self.cancelled = True
        self._close()
        print("cancelled status monitor")
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