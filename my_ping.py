import socket 
import struct
import os
import time
import argparse


# count(- c) : Stop after sending (and receiving) count ECHO_RESPONSE packets. If this option is not specified, ping will operate until interrupted.
# wait(- i) : Wait for wait seconds between sending each packet. Default is one second.
# packetsize(- s) : Specify the number of data bytes to be sent. Default is 56 (64 ICMP data bytes including the header).
# timeout (-t) : Specify a timeout in seconds before ping exits regardless of how many packets have been received.

def main():
    pkt_recieved = 0

def checksum(pkt_data):
    #Make the packet an even length if it is not already 
    if len(pkt_data) % 2:
        pkt_data += b"\x00"

    checksum = 0

    for i in range(0, len(pkt_data), 2):
        checksum += (pkt_data[i] << 8) + pkt_data[i + 1]

    checksum = (checksum >> 16) + (checksum & 0xFFFF)  #overflow plus lower 16 bits  
    checksum += (checksum >> 16)

    return ~checksum & 0xFFFF            

def create_icmp_packet(pkt_id, seq_num, data_bytes):
    #An icmp packet header needs: Type, Code, Checksum                                                             
    icmp_type = 8
    icmp_code = 0
    check_sum = 0

    data = b"\x00" * data_bytes

    header = struct.pack('!BBHHH', icmp_type, icmp_code, check_sum, pkt_id, seq_num)

    check_sum = checksum(header + data) 
    header = struct.pack('!BBHHH', icmp_type, icmp_code, check_sum, pkt_id, seq_num)

    return header + data 

def send_ping(dest_ip, pkt_size, seq_num):
    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

    pkt_id = os.getpid() & 0xFFFF

    packet = create_icmp_packet(pkt_id, seq_num, pkt_size)

    send_time = time.monotonic()
    raw_socket.sendto(packet, (dest_ip, 0))

    return raw_socket, send_time, pkt_id, seq_num
    
if __name__ == "__main__":
    main()