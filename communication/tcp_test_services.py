import socket
import time 
import select
import threading

class TCPInbound:

    def __init__(self,port,msgs) -> None:
        self.msgs = msgs
        self.port = port
        self.thread = None
        self.socket = None
        self.cancelled = False

    def start_run_thread(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()
        return self.thread

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('localhost', self.port))
        for msg in self.msgs:
            time.sleep(3)
            self.socket.sendall(msg.encode())
        self.socket.close() 

    def close(self):
        self.thread.cancelled = True

class TCPBouncer:

    def __init__(self,port) -> None:
        self.port = port
        self.thread = None
        self.cancelled = False

    def start_run_thread(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()
        return self.thread

    def run(self):
        print("TCP Bouncer script. \n Autoreply to incomming msgs port 50000")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', self.port))
        s.listen(1)
        conn, addr = s.accept()
        print("connection accepted from "+addr[0]+":"+str(addr[1]))
        while not self.cancelled:
            try:
                ready_to_read, ready_to_write, in_error = \
                    select.select([conn,], [conn,], [], 5)
            except select.error:
                conn.shutdown(2)    # 0 = done receiving, 1 = done sending, 2 = both
                conn.close()
                # connection error event here, maybe reconnect
                print('connection error')
                break

            time.sleep(1)
            wait = time.time()
            data = conn.recv(1024)
            print('. waited '+str(time.time()-wait)+ " got message '"+data.decode()+"'")
            if not data:
                print('connection lost, waiting for new..')
                conn, addr = s.accept()
                print('new connection acquired')
            conn.sendall(data)

        conn.close()

    def close(self):
        self.cancelled = True
