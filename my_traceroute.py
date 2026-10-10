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

def rcv_response(icmp_socket, send_time, timeout, dest_ip, dest_port):
    icmp_socket.settimeout(timeout)

    try:
        pkt_data, ip_address = icmp_socket.recvfrom(1024)

        ip_header_length = (pkt_data[0] & 0x0F) * 4
        icmp_header = pkt_data[ip_header_length:ip_header_length + 8]

        ip_start = ip_header_length + 8
        ip_length = (pkt_data[ip_start] & 0x0F) * 4
        udp_header_start = ip_start + ip_length

        required_dest_port = int.from_bytes(pkt_data[udp_header_start + 2:udp_header_start + 4])

        dest_ip_address_rcv = ip_address[0]
        type = int.from_bytes(icmp_header[0:1])
        code = int.from_bytes(icmp_header[1:2])
        checksum = int.from_bytes(icmp_header[2:4])
        rcv_id = int.from_bytes(icmp_header[4:6])
        rec_seq_num = int.from_bytes(icmp_header[6:8])

        arr_time = time.monotonic()

        dest_reached = (type == 3 and code == 3 and dest_ip_address_rcv == dest_ip)
        rtt = (arr_time - send_time) * 1000

        if(type != 11 and not (type == 3 and code == 3)):
            return None

        if required_dest_port != dest_port:
            return None 
        
        return dest_ip_address_rcv, rtt, dest_reached
    except socket.timeout:
        return None


if __name__ == "__main__":
    main()

