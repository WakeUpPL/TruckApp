import socket

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY, 1)
sock.connect(('localhost',10000))

old_data=(0)

while True:
    #read enter msg
    print ('opent reiler door?')
    td=input ()

    #send msg on server
    sock.send(td.encode())

    #takeing msg from server
    data=sock.recv(1024)
    data=data.decode()
    if data!=old_data:
        old_data=data
        print(data)
    else:
        pass
    


    
