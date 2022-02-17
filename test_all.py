from communication.exhalytics import ExhalyticsSampleReader,ExhalyticStatusMonitor
from communication.tcp_test_services import TCPBouncer,TCPInbound
import socket
import time 



def test_mail():
    print('foo')
    assert True

def test_bouncer_tcp():
    print("Make sure that the TCP_Bouncer script is running..")
    words = ['hej', 'på', 'dig', 'nu']
    receive_buffer = []
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 50000))

    for w in words:
        time.sleep(3)
        s.sendall(w.encode())
        receive_buffer.append(s.recv(1024).decode())

    print('received:')  
    for inx,b in enumerate(receive_buffer):
        print(b)
        assert b == words[inx]

    s.close()

def test_tcp_exhalytics_monitor():
    ''' Tests that send and response for requesting status
        from instrument works'''
    bouncer = TCPBouncer(80)
    bouncer.start_run_thread()
    status_monitor = ExhalyticStatusMonitor('localhost',80)
    status_monitor.connect()
    sent = 'myping'
    status_monitor.send_message(sent)
    response = status_monitor.recv_message()
    assert response == sent 
    status_monitor.close()
    bouncer.close()

def test_tcp_exhalytics_sample_reader():
    ''' Tests if it can receive sample msgs as from Exhalytics'''
    send_msg = ['sent','from','test','sender TCPInbound']
    inbound = TCPInbound(80,send_msg)
    sample_reader = ExhalyticsSampleReader('localhost',80)
    sample_reader.start()
    inbound.start_run_thread()
    reply = sample_reader.get_msgs()
    inbound.close()
    sample_reader.close()
    assert reply == send_msg

    # start the tcp_autosender