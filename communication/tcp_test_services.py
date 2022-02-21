import socket
import time 
import select
import threading

class TCPInbound:

    '''  Connects to a tcp server and sends predetermined messages '''

    def __init__(self,port,msgs) -> None:
        self.msgs = msgs
        self.port = port
        self.thread = None
        self.socket = None
        self.finished = False

    def start_run_thread(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()
        return self.thread

    def run(self):
        print("= TCPInbound started =")
        time.sleep(2)
        self.socket = socket.create_connection(('localhost', self.port))
        for msg in self.msgs:
            time.sleep(1)
            print("Inbound: sent"+msg)
            self.socket.sendall(msg.encode())
        self.finished = True

    def close(self):
        self.socket.close()
        print("= TCP Inbound Finished =") 

class TCPBouncer:
    '''
        Responds to incomming messages with predetermined responses
        If no response is specified, the message is echoed back
    '''
    def __init__(self,port,responses=None) -> None:
        self.port = port
        self.thread = None
        self.cancelled = False
        self.response = responses

    def start_run_thread(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()
        return self.thread

    def run(self):
        print("TCP Bouncer script. \n Autoreply to incomming msgs port "+str(self.port))
        while not self.cancelled:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind(('localhost', self.port))
                break
            except:
                print('could not open port:'+str(self.port))
                time.sleep(1)

        s.listen(1)
        conn, addr = s.accept()
        print("connection accepted from "+addr[0]+":"+str(addr[1]))
        while not self.cancelled:

            time.sleep(1)
            wait = time.time()
            data = conn.recv(1024)
            print('. waited '+str(time.time()-wait)+ " got message '"+data.decode()+"'")
            if data and self.response is not None and data.decode() in self.response:
                reply = self.response[data.decode()].encode()
                conn.sendall(reply)
            elif data:
                conn.sendall(data)

            #if reply is not None:
            #    print('connection lost, waiting for new..')
            #    conn, addr = s.accept()
            #    print('new connection acquired')

        conn.close()
        s.close()
        print('= Bouncer Closed =')

    def close(self):
        self.cancelled = True
