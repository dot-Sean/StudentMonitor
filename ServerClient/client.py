import socket
import os
import shutil
from config import PORT, DOCUMENTS_PATH, RECONNECT_TIME, COLLECTING_TIME, EOF_MSG, XML_NAME, SCREENSHOT_NAME
from threading import Thread
from PIL import ImageGrab
from studentXml import StudentXML
from time import sleep


class Client(object):
    def __init__(self, port):
        try:

            if not os.path.exists(DOCUMENTS_PATH):
                os.makedirs(DOCUMENTS_PATH)
            self.username = socket.gethostname()
            self.s = socket.socket()
            self.host = socket.gethostname()  # Get local machine name
            self.s.connect((self.host, port))
            self.doc_maker = StudentXML(socket.gethostbyname(self.host), self.username)

            self.s.send(self.username.encode())

        except ConnectionRefusedError:
            from time import sleep
            sleep(RECONNECT_TIME)
            self.__init__(port)

    def start_routine(self):
        try:
            while True:
                sleep(COLLECTING_TIME)
                self.send_all()
        except ConnectionResetError:
            print('Server disconnected, trying to reconnect')
            self.__init__()

    def send_XML(self):
        try:
            self.s.send('send_xml'.encode())
            f = open(os.path.join(DOCUMENTS_PATH, XML_NAME), 'rb')

            print('Sending xml...')
            l = f.read(1024)
            while l:
                self.s.send(l)
                l = f.read(1024)
            f.close()

            sleep(2)
            self.s.send(EOF_MSG.encode())
            print("Done sending")

        except ConnectionResetError:
            print("Server disconected while sending files")

    def send_image(self):
        img = ImageGrab.grab()
        save_as = os.path.join(DOCUMENTS_PATH, SCREENSHOT_NAME)
        img.save(save_as)

        self.s.send('send_image'.encode())
        try:
            f = open(save_as, 'rb')
            print('Sending image...')

            l = f.read(1024)
            while l:
                self.s.send(l)
                l = f.read(1024)
            f.close()

            sleep(2)
            self.s.send(EOF_MSG.encode())
            print('Done sending')

        except ConnectionResetError:
            print("Server disconected while sending files")

    def send_all(self):
        try:
            self.doc_maker.generate_document()
            self.send_XML()
            self.send_image()

            #shutil.rmtree(DOCUMENTS_PATH)
            #os.mkdir(DOCUMENTS_PATH)
        except:
            print("Error occured:", self.send_all.__name__)


if __name__ == '__main__':
    c1 = Client(PORT)

    t1 = Thread(target=c1.start_routine, args=())
    t1.start()
    t1.join()


    #t1 = Thread(target=c1.send_XML, args=())
    #t2 = Thread(target=c2.send_XML, args=())

    #t1.start()

    #from time import sleep

    #sleep(3)

    #t2.start()

    #t1.join()
    #t2.join()