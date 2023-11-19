import socket
import time

main_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY, 1)
main_socket.bind(('localhost',10000))
main_socket.setblocking(0)
main_socket.listen(5)
print('Create sockets')

users_socket=[]
while True:
    #check/add new connection
    try:
        new_socket,addr=main_socket.accept()
        print('Connection ',addr)
        new_socket.setblocking(0)
        users_socket.append(new_socket)
    except:
        print('No connections users')
        pass
    #read msg
    for sock in users_socket:
        try:
            data=sock.recv(1024)
            data=data.decode()
            print('Taking MSG ', data)
        except:
            pass

    #process data
    #send msg on client
    for sock in users_socket:
        try:
            sock.send('GAT #19'.encode())
        except:
            users_socket.remove(sock)
            sock.close()
            print('Disconnect user')
        

            


    #data base users
    #sleep
    time.sleep(1)