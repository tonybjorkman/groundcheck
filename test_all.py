import mailservice.mail
import mailservice.collector
import socket
import time 

class TestTcp:
    def __init__(self,port) -> None:
        socket.create_server('localhost',80)

def test_mail():
    print('foo')
    assert True

def test_send_tcp():
    words = ['hej', 'på', 'dig', 'nu']
    receive_buffer = []
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 50000))

    for w in words:
        time.sleep(3)
        s.sendall(w.encode())
        receive_buffer.append(s.recv(1024).decode())

    print('received:')  
    for b in receive_buffer:
        print(b)

    s.close()

def test_tcp_client():
    client = mailservice.collector.ExhalyticClient('localhost',80)
    server = mailservice.collector.ExhalyticsEventReceiver('localhost',80)
    server.start()
    client.connect()
    client.send_message('myping')
    client.recv_message()
    client.close()
    assert True

