from communication.exhalytics import ExhalyticsSampleReader,ExhalyticStatusMonitor
from communication.tcp_test_services import TCPBouncer,TCPInbound
import socket
import time 

def test_mail():
    print('foo')
    assert True

def test_bouncer_tcp_echo():
    print('==== Test Bouncer TCP ====')
    print("Make sure that the TCP_Bouncer script is running..")
    words = ['hej', 'på', 'dig', 'nu']
    receive_buffer = []
    bouncer = TCPBouncer(50000)
    bouncer.start_run_thread()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 50000))

    for w in words:
        time.sleep(1)
        s.sendall(w.encode())
        receive_buffer.append(s.recv(1024).decode())

    print('received:')  
    for inx,b in enumerate(receive_buffer):
        print(b)
        assert b == words[inx]

    bouncer.close()
    s.close()
    time.sleep(4)

def test_bouncer_tcp_response():
    print('==== Test Bouncer TCP Response ====')
    words = ['hej', 'dag', 'namn', 'foo']
    responses = {'hej':'då', 'dag':'måndag', 'namn':'Kalle','foo':'bar'}
    receive_buffer = []
    bouncer = TCPBouncer(50000, responses)
    bouncer.start_run_thread()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 50000))

    for w in words:
        time.sleep(1)
        s.sendall(w.encode())
        received = s.recv(1024).decode()
        print('sent:'+w)
        print('received: '+received)
        assert responses[w] == received

    bouncer.close()
    s.close()
    time.sleep(4)

def test_tcp_exhalytics_monitor_single():
    ''' Should simulate that this app is sending a status-request query
    to an exhalytics instrument and retrieving a response
    telling the status of the instrument. '''

    print('==== Test Exhalytics Monitor  ====')
    port = 50000 
    bouncer = TCPBouncer(port)
    bouncer.start_run_thread()
    
    time.sleep(2)
    status_monitor = ExhalyticStatusMonitor()
    status_monitor.add_target('localhost', port)
    status_monitor.connect_to_targets()
    status_monitor.update_target_statuses()
    response = status_monitor.targets[0].status
    assert response == 'OK' 
    status_monitor.close()
    bouncer.close()
    time.sleep(4)

def test_tcp_exhalytics_monitor_multi_ok():
    '''
    Same as single but with multiple targets(bouncers) 
    '''

    print('==== Test Exhalytics Monitor Multi  ====')
    num_bouncers = 3
    bouncers = []
    for i in range(num_bouncers):
        port = 50000 + i
        bouncer = TCPBouncer(port)
        bouncer.start_run_thread()
        bouncers.append(bouncer)
    
    time.sleep(2)
    status_monitor = ExhalyticStatusMonitor()
    for i in range(num_bouncers):
        status_monitor.add_target('localhost', 50000 + i)
    
    #add one target that is not connected
    #status_monitor.add_target('localhost', 50000 + num_bouncers)

    status_monitor.connect_to_targets()
    status_monitor.update_target_statuses()
    status_monitor.print_target_statuslist()
    for t in status_monitor.targets[:num_bouncers-1]:
        assert t.status == 'OK'
    
    status_monitor.close()
    for b in bouncers:
        b.close()
    time.sleep(4)

def test_tcp_exhalytics_sample_reader():
    ''' Tests if it can receive sample data as sent
     from an Exhalytics instrument '''

    print('==== Test Exhalytics Sample  ====')
    port = 50001
    send_msg = ['sent','from','test','sender TCPInbound']
    inbound = TCPInbound(port, send_msg)
    
    sample_reader = ExhalyticsSampleReader('localhost',port)
    
    # inbound has a 2 sec delay and then starts 
    sample_reader.start_run_thread()
    inbound.start_run_thread()

    while not inbound.finished:
        time.sleep(1)

    reply = sample_reader.get_msgs()

    inbound.close()
    sample_reader.close()
    print("Compare input with output")
    for i,j in zip(reply,send_msg):
        print(i+" vs "+j)
    assert reply == send_msg

    # start the tcp_autosender