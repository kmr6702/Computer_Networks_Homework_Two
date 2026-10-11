import socket 
import struct
import os
import time
import argparse

def main():
    pkt_recieved = 0

    parser=argparse.ArgumentParser()

    parser.add_argument("-c", "--count", type=int)
    parser.add_argument("-i", "--wait", type=float, default=1)
    parser.add_argument("-s", "--size", type=int, default=56)
    parser.add_argument("-t", "--timeout", type=float)
    parser.add_argument("dest_ip")

    args = parser.parse_args()

    dest_ip = args.dest_ip
    count = args.count
    wait = args.wait
    pkt_size = args.size 
    timeout = args.timeout 

    pkt_id = os.getpid() & 0xFFFF
    seq_num = 1
    start_time = time.monotonic()

    try:
        while True:
            if count is not None and pkt_recieved >= count:
                break 

            if timeout is not None and time.monotonic() - start_time >= timeout: 
                break 

            raw_socket, send_time, pkt_id, seq_num = send_ping(dest_ip, pkt_size, seq_num)

            try:
                if rcv_ping(raw_socket, send_time, pkt_id, seq_num):
                    pkt_recieved += 1
            finally:
                raw_socket.close()

            seq_num += 1
            time.sleep(wait)
    except KeyboardInterrupt:
        print("\n End of Ping")



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

def rcv_ping(raw_socket, send_time, pkt_id, seq_num):
    pkt_data, ip_address = raw_socket.recvfrom(1024)
    
    rcv_time = time.monotonic()
    ip_header_length = (pkt_data[0] & 0x0F) * 4
    icmp_header = pkt_data[ip_header_length:ip_header_length + 8]

    type = int.from_bytes(icmp_header[0:1])
    code = int.from_bytes(icmp_header[1:2])
    checksum = int.from_bytes(icmp_header[2:4])
    rcv_id = int.from_bytes(icmp_header[4:6])
    rec_seq_num = int.from_bytes(icmp_header[6:8])

    if(type == 0 and pkt_id == rcv_id and seq_num == rec_seq_num):
        rtt = (rcv_time - send_time) * 1000
        print(f"Reply from {ip_address[0]}: seq={rec_seq_num} time={rtt:.2f}ms")
        return True

    return False

if __name__ == "__main__":
    main()