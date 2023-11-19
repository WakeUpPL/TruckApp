import socket
import time

class User():
    def __init__(self,conn,addr,err):
        self.conn=conn
        self.addr=addr
        self.err=err

main_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY, 1)
main_socket.bind(('localhost',10000))
main_socket.setblocking(0)
main_socket.listen(5)
print('Create sockets')

users=[]
while True:
    #check/add new connection
    try:
        new_socket,addr=main_socket.accept()
        print('Connection ',addr)
        new_socket.setblocking(0)
        new_user=User(new_socket, addr, 0)
        users.append(new_user)
    except:
        #print('No connections users')
        pass
    #read msg
    for user in users:
        try:
            data=user.conn.recv(1024)
            data=data.decode()
            print('Taking MSG ', data)
        except:
            pass

    #process data
    #send msg on client
    for user in users:
        try:
            user.conn.send('GATE $19'.encode())
            user.err=0
        except:
            user.err+=1

    #clear list users
    for user in users:
        if user.err == 10:
            user.conn.close()
            users.remove(user)            


    #data base users
    #sleep
    time.sleep(1)