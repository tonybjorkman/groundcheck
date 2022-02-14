import socket
import time 
import select

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 50000))
s.listen(1)
conn, addr = s.accept()
print("connection accepted from "+addr[0]+":"+str(addr[1]))
while 1:
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
    #if not data:
    #    break
    conn.sendall(data)
conn.close()