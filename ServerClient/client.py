import getpass
import socket
from config import PORT, XML_PATH
from threading import Thread


class Client(object):
    def __init__(self, port):
        try:
            self.username = getpass.getuser()
            self.s = socket.socket()
            self.host = socket.gethostname()  # Get local machine name
            self.s.connect((self.host, port))

            self.s.send(self.username.encode())

        except ConnectionRefusedError:
            from time import sleep
            sleep(30)
            self.__init__(port)

    # noinspection PyPep8Naming
    def send_XML(self):
        try:
            self.s.send('send_xml'.encode())

            f = open(XML_PATH + 'test.avi', 'rb')  # testowo!
            print('Sending...')
            l = f.read(1024)
            while l:
                self.s.send(l)
                l = f.read(1024)
            f.close()
            print("Done sending")
        except ConnectionResetError:
            print("Server disconected while sending files")

if __name__ == '__main__':
    c1 = Client(PORT)
    c2 = Client(PORT)

    t1 = Thread(target=c1.send_XML, args=())
    t2 = Thread(target=c2.send_XML, args=())

    t1.start()

    from time import sleep
    sleep(3)

    t2.start()

    t1.join()
    t2.join()