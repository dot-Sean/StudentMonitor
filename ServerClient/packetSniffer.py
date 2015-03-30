import socket
import sys
import _socket
import struct


def receiveData(s):
    data = ''
    try:
        data = s.recvfrom(65565)
    except _socket.timeout:
        data = ''
    except:
        print("An error happened")
        sys.exc_info()
    return data[0]

def getTOS(data):
    """
    http://www.networksorcery.com/enp/protocol/ip.htm#Differentiated%20Services
    """
    precendence = {0: "Routine", 1: "Priority", 2: "Immediate", 3: "Flash", 4:
                   "Flash override", 5: "CRITIC/ECP", 6: "Internetwork control", 7: "Network control"}
    #TODO
    #delay =
    #throughput =
    #reliability =
    #cost =

    D = data & 0x10 #dilej
    D >>= 4
    T = data &0x8 #fruput
    T >>= 3
    R = data & 0x4 # itd.
    R >>=2
    C = data & 0x2
    C >>= 1

    tabs ='\n\t\t\t'
    TOS = precendence[data >> 5] + tabs + delay[D] + tabs + throughput[T] + tabs + reliability[R] + tabs + cost[C]

    return TOS






HOST = socket.gethostbyname(socket.gethostname())

s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
s.bind((HOST, 0))

s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

data = receiveData(s)
unpackedData = struct.unpack('!BBHHHBBH4s4s', data[:20])

version_IHL = unpackedData[0]
version = version_IHL >> 4
IHL = version_IHL & 0xF
TOS = getTOS(unpackedData[1])
totalLength = unpackedData[2]
ID = unpackedData[3]

# get the type of serivce - 8 bits


s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)