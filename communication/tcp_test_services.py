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
    class Response:
        '''
           replies to a message with a predetermined response
           which can be configured as either echo, seq, or pair
        '''
        def __init__(self,responses): 
            self.seq_replies = None
            self.pair_replies = None
            self.type = 'echo'
            self.seq_inx = 0
            if type(responses) == dict:
                self.set_pair_reply(responses)
            elif type(responses) == list:
                self.set_seq_reply(responses)
        
        def set_pair_reply(self,pairs):
            self.pair_replies = pairs
            self.type = 'pair'

        def set_seq_reply(self,seq):
            self.seq_replies = seq
            self.type = 'seq'

        def get_reply(self,msg):
            if self.type == 'seq':
                if self.seq_inx >= len(self.seq_replies):
                    self.seq_inx = len(self.seq_replies)-1
                reply = self.seq_replies[self.seq_inx]
                self.seq_inx += 1
                return reply 
            elif self.type == 'pair' and msg in self.pair_replies: 
                return self.pair_replies[msg]
            else:
                return msg 

    def __init__(self,port,responses=None) -> None:
        ''' responses - either dict or key/value strings
                        or seq of strings '''
        self.port = port
        self.thread = None
        self.cancelled = False
        self.response = TCPBouncer.Response(responses)

    def start_run_thread(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()
        return self.thread

    def set_response(self,responses):
        self.response = TCPBouncer.Response(responses)

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
            if data:
                reply = self.response.get_reply(data.decode()).encode()
                conn.sendall(reply)

            #if reply is not None:
            #    print('connection lost, waiting for new..')
            #    conn, addr = s.accept()
            #    print('new connection acquired')

        conn.close()
        s.close()
        print('= Bouncer Closed =')

    def close(self):
        self.cancelled = True
