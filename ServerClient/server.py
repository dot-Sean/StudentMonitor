from encodings.utf_8 import decode
import os
import socket
import sys
from _thread import start_new_thread
import time
from config import *


class ServerSM(object):
    users_data = []

    def __init__(self, host, port):
        self.s = socket.socket()
        try:
            self.s.bind((host, port))
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        self.s.listen(10)

        self.wait_for_clients()

    def wait_for_clients(self):
        while True:
            conn, addr = self.s.accept()
            username = conn.recv(1024)
            username = decode(username)[0]

            addr = list(addr)
            addr.insert(2, str(username))
            addr = tuple(addr)

            self.users_data.append(addr)

            connected_users = [ip + ':' + str(port) + ' - ' + username for (ip, port, username) in self.users_data]
            print("Polaczono ", connected_users[-1])

            start_new_thread(self.client_recv, (conn, addr,))

    def close_conn(self, conn, addr):
        for x in range(len(self.users_data) - 1, -1, -1):
            if self.users_data[x][1] == addr[1]:
                del self.users_data[x]
                break
        print(addr[0] + ':' + str(addr[1]) + ' Disconnected (left ' + str(len(self.users_data)) + ')')
        conn.close()

    def client_recv(self, conn, addr):
        try:
            msg = conn.recv(1024)
            msg = decode(msg)[0]
            print('client sent: ', msg)

            if msg == 'send_xml':
                self.serve_xml(conn, addr, msg)

            if msg == 'update_whitelist':  # TODO
                pass

            if msg == 'send_image':  # TODO
                pass

        except ConnectionResetError:
            print('force close', str(addr[1]))
        finally:
            self.close_conn(conn, addr)

    def serve_xml(self, conn, addr, msg):
        username = None
        for x in range(len(self.users_data) - 1, -1, -1):
            if self.users_data[x][1] == addr[1]:
                username = self.users_data[x][2]

        if username is not None and not os.path.exists(username):
            os.makedirs(username)

        f = open(username + '\\recv_file_' + str(time.strftime("%H-%M-%S")) + '.avi', 'wb')

        print('Starting', msg, addr)
        l = conn.recv(1024)
        while l:
            f.write(l)
            l = conn.recv(1024)
        f.close()
        print('Done ', msg)
        msg = None

if __name__ == '__main__':
    s = ServerSM(HOST, PORT)




