import socket 
import struct
import time
import os 

def checksum(pkt_data):
    #Make the packet an even length if it is not already 
    if len(pkt_data) % 2:
        pkt_data += b"\x00"

    checksum = 0

    for i in range(0, len(pkt_data), 2):
        checksum += (pkt_data[i] << 8) + pkt_data[i + 1]

    checksum = (checksum >> 16) + (checksum & 0xFFFF)  #overflow plus lower 16 bits  
    checksum += (checksum >> 16)

    return checksum & 0xFFFF            

def create_icmp_packet(pkt_id, seq_num):
    icmp_type = 8
    icmp_code = 0
    checksum = 0

    payload = struct.pack("!d")

    header = struct.pack('!BBHHH', icmp_type, icmp_code, checksum, pkt_id, seq_num)

    checksum = (header + payload) 
    header = struct.pack('!BBHHH', icmp_type, icmp_code, checksum, pkt_id, seq_num)

    return header + payload 

def send_ping(dest_ip):
    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

