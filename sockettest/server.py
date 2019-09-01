'''
Created on 2019年9月1日

@author: danny
'''
import socket
import threading

# 创建一个socket套接字，该套接字还没有建立连接
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定监听端口，这里必须填本机的IP192.168.27.238，localhost和127.0.0.1是本机之间的进程通信使用的
server.bind(('192.168.0.7', 6688))
# 开始监听，并设置最大连接数
server.listen(5)

def severhandle(connect, host, port):
    while True:
        # 接受客户端的数据
        data = connect.recv(1024)
        # 如果接受到客户端要quit就结束循环
        if data == b'quit' or data == b'':
            print(b'the client has quit.')
            break
        else:
            # 发送数据给客户端
            connect.sendall(b'your words has received.')
            print(b'the client say:' + data)

while True:
    print(u'waiting for connect...')
    # 等待连接，一旦有客户端连接后，返回一个建立了连接后的套接字和连接的客户端的IP和端口元组
    connect, (host, port) = server.accept()
    print(u'the client %s:%s has connected.' % (host, port))
    threading._start_new_thread(severhandle,(connect, host, port))   


# 结束socket
server.close()
