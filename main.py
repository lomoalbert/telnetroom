#!/usr/bin/env python
#-*- coding:utf-8 -*-

import socket,select



def main():
    host='127.0.0.1'
    port=23
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host,port))
    s.listen(5)
    socklist=[s]
    while True:
        listening(socklist)
def listening(socklist):
    rlist,wlist,elist=select.select(socklist,[],[],0)
    for sock in rlist:
        if sock==socklist[0]:
            print 's.accept',socklist
            clientsock,clientaddr = sock.accept()
            socklist.append(clientsock)
        else:
            words=sock.recv(8196)
            print [words]
            if not words:
                sock.close()
                socklist.remove(sock)
                continue
            sendall(socklist,words,sock)
def sendall(socklist,line,tsock):
    if '\xff' in line:return#对telnet命令符号过滤
    for sock in socklist[1:]:
        if sock!=tsock:
            sock.send(line)
if __name__ == "__main__":
    main()

