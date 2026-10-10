import socket
import struct
import time 
import argparse 

def main():
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

def send_probe(udp_socket, ttl, dest_ip, dest_port):
    udp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

    udp_packet = b'\x00'
    send_time = time.monotonic()
    udp_socket.sendto(udp_packet, (dest_ip, dest_port))

    return send_time

def rcv_response(icmp_socket, send_time, timeout, dest_ip):
    icmp_socket.settimeout(timeout)

    try:
        pkt_data, ip_address = icmp_socket.recvfrom(1024)
        arr_time = time.monotonic()
        rtt = (arr_time - send_time) * 1000
    except timeout:
        return TimeoutError


if __name__ == "__main__":
    main()

