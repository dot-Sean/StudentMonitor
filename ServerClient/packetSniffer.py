import _socket as socket
import struct
import sys

HOST = socket.gethostbyname(socket.gethostname())
PORT = 0


class TCPSniffer:
    def __init__(self):
        self.s = self.connect()

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        s.bind((HOST, 0))

        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        return s

    def receive_data(self):
        try:
            data = self.s.recvfrom(65565)
        except socket.timeout:
            print('socket timeout')
            data = ''
        except:
            print("An error happened")
            sys.exc_info()
        return data[0]

    def get_ip_data(self, data=None, data_type='Protocol'):
        if not data:
            data = self.receive_data()
        unpacked_data = struct.unpack('!BBHHHBBH4s4s', data[:20])

        if data_type == 'Version':
            return unpacked_data[0] >> 4
        if data_type == 'IHL':
            return unpacked_data[0] & 0xf
        if data_type == 'Differentiated Services':
            return unpacked_data[1]
        if data_type == 'Total length':
            return unpacked_data[2]
        if data_type == 'Identification':
            return unpacked_data[3]
        if data_type == 'Flags':
            return unpacked_data[4]
        if data_type == 'Fragment offset':
            return unpacked_data[4] & 0x1FFF
        if data_type == 'TTL':
            return unpacked_data[5]
        if data_type == 'Protocol':
            return unpacked_data[6]
        if data_type == 'Header checksum':
            return unpacked_data[7]
        if data_type == 'Source IP address':
            return socket.inet_ntoa(unpacked_data[8])
        if data_type == 'Destination IP address':
            return socket.inet_ntoa(unpacked_data[9])

    def get_tcp_data(self, data=None, data_type='Source Port'):
        if not data:
            data = self.receive_data()
        if self.get_ip_data(data=data, data_type='Protocol') == 6:
            unpacked_data = struct.unpack('!HHIIHHHH', data[20:40])

            if data_type == 'Source Port':
                return unpacked_data[0]
            if data_type == 'Destination Port':
                return unpacked_data[1]
            if data_type == 'Sequence Number':
                return unpacked_data[2]
            if data_type == 'Acknowledgment Number':
                return unpacked_data[3]
            if data_type == 'Data Offset':
                return unpacked_data[4] & 0xf000 >> 12
            if data_type == 'ECN':
                return unpacked_data[4] & 0x01c0 >> 6
            if data_type == 'Control Bits':
                return unpacked_data[4] & 0x003f
            if data_type == 'Window':
                return unpacked_data[5]
            if data_type == 'Checksum':
                return unpacked_data[6]
            if data_type == 'Urgent Pointer':
                return unpacked_data[7]


if __name__ == '__main__':
    tcpsniffer = TCPSniffer()
    while True:
        a = tcpsniffer.get_tcp_data(data_type='Urgent Pointer')
        if a:
            print(a)


