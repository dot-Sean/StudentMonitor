import _socket as socket
import struct
import sys
import re

HOST = socket.gethostbyname(socket.gethostname())
PORT = 0


class TCPSniffer:
    def __init__(self):
        self.s = self.connect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

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

    def get_ip_header(self, data=None, data_type='Protocol'):
        if not data:
            data = self.receive_data()
        unpacked_data = struct.unpack('!BBHHHBBH4s4s', data[:20])

        if data_type == 'Version':
            return unpacked_data[0] >> 4
        if data_type == 'IHL':
            return unpacked_data[0] & 0xf
        if data_type == 'Differentiated Services':
            return unpacked_data[1]
        if data_type == 'Total Length':
            return unpacked_data[2]
        if data_type == 'Identification':
            return unpacked_data[3]
        if data_type == 'Flags':
            return unpacked_data[4]
        if data_type == 'Fragment Offset':
            return unpacked_data[4] & 0x1FFF
        if data_type == 'TTL':
            return unpacked_data[5]
        if data_type == 'Protocol':
            return unpacked_data[6]
        if data_type == 'Header Checksum':
            return unpacked_data[7]
        if data_type == 'Source IP':
            return socket.inet_ntoa(unpacked_data[8])
        if data_type == 'Destination IP':
            return socket.inet_ntoa(unpacked_data[9])

    def get_tcp_header(self, data=None, data_type='Source Port'):
        if not data:
            data = self.receive_data()
        if self.get_ip_header(data=data, data_type='Protocol') == 6:
            unpacked_data = struct.unpack('!HHIIHHHH', data[20:40])  # [20:40]

            if data_type == 'Source Port':
                return unpacked_data[0]
            if data_type == 'Destination Port':
                return unpacked_data[1]
            if data_type == 'Sequence Number':
                return unpacked_data[2]
            if data_type == 'Acknowledgment Number':
                return unpacked_data[3]
            if data_type == 'Data Offset':
                return unpacked_data[4] >> 12
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
        else:
            return -1

    def get_tcp_data(self, data=None):
        if not data:
            data = self.receive_data()
        data_offset = self.get_tcp_header(data, 'Data Offset')
        ihl = self.get_ip_header(data, 'IHL')
        total_length = self.get_ip_header(data, 'Total Length')
        data_length = total_length - (ihl + data_offset)*4
        data_start = (ihl+data_offset)*4
        data_end = data_start + data_length

        unpacked_data = struct.unpack("!%ds" % data_length, data[data_start:data_end])

        return unpacked_data

    def get_http_referer(self, data=None):
        if not data:
            data = self.receive_data()
            port = self.get_tcp_header(data, 'Destination Port')
            if port == 80:
                packet_data = self.get_tcp_data(data)
                packet_data = re.findall(r'.+Referer:\s(.+)\\r\\nCookie:.*', str(packet_data))

                return packet_data


if __name__ == '__main__':
    #### do testowania offsetu
    #with TCPSniffer() as tcpsniffer:
    #    while True:
    #        data = tcpsniffer.receive_data()
    #        a = tcpsniffer.get_tcp_header(data=data, data_type='Acknowledgment Number')
    #        if a:
    #            b = tcpsniffer.get_tcp_header(data=data, data_type='Data Offset')
    #            print(b)

    #with TCPSniffer() as tcpsniffer:
        #data = tcpsniffer.receive_data()
        #ip_header = tcpsniffer.get_ip_header(data, 'Total Length')
        #print('Total Length:', ip_header)

        ### do sprawdzenia poprawnosci tcp headera
        #tcp_header = tcpsniffer.get_tcp_header(data, 'Source Port')
        #print(tcp_header)
        #tcp_header = tcpsniffer.get_tcp_header(data, 'Destination Port')
        #print(tcp_header)
        #tcp_header = tcpsniffer.get_tcp_header(data, 'Sequence Number')
        #print(tcp_header)
        #tcp_header = tcpsniffer.get_tcp_header(data, 'Acknowledgment Number')
        #print(tcp_header)
        #tcp_header = tcpsniffer.get_tcp_header(data, 'Data Offset')
        #print('data offset', tcp_header)
        #tcp_header = tcpsniffer.get_tcp_header(data, 'ECN')
        #print(tcp_header)
        #tcp_header = tcpsniffer.get_tcp_header(data, 'Control Bits')
        #print(tcp_header)
        #tcp_header = tcpsniffer.get_tcp_header(data, 'Window')
        #print(tcp_header)
        #tcp_header = tcpsniffer.get_tcp_header(data, 'Checksum')
        #print(tcp_header)
        #tcp_header = tcpsniffer.get_tcp_header(data, 'Urgent Pointer')
        #print(tcp_header)
        #while True:
        #    with TCPSniffer() as tcpsniffer:
        #        data = tcpsniffer.receive_data()
        #        port = tcpsniffer.get_tcp_header(data, 'Destination Port')
        #       if port == 443:
        #            packet_data = tcpsniffer.get_tcp_data(data)
        #            print(packet_data)

        with TCPSniffer() as tcpsniffer:
            tcpsniffer.get_http_referer()
