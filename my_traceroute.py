import socket
import time 
import argparse 

def main():
    parser = argparse.ArgumentParser()

    #Create argument values for each required option 
    parser.add_argument("-n", action="store_true")
    parser.add_argument("-q", type=int, default=3)
    parser.add_argument("-S", "--summary", action="store_true")
    parser.add_argument("dest_ip")
    args = parser.parse_args()

    dest_ip = socket.gethostbyname(args.dest_ip)
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    max_ttl = 30
    base_port = 33434
    is_dest_reached = False

    #Loop while under the max amount of hops 
    for ttl in range(1, max_ttl + 1):
        responses = []
        unaswered = 0

        print(ttl, end=" ")
        for probe_index in range(args.q):
            dest_port = base_port + (ttl -1) * args.q + probe_index

            send_time = send_probe(udp_socket, ttl, dest_ip, dest_port)
            receive = rcv_response(icmp_socket, send_time, 2, dest_ip, dest_port)

            responses.append(receive)

            if receive is None:
                unaswered += 1
                print("*", end=" ")
            else:
                response_ip, rtt, dest_reached = receive

                if args.n:
                    print(f"{response_ip} {rtt:.2f} ms", end=" ")
                else:
                    try:
                        hostname = socket.gethostbyaddr(response_ip)[0]
                        print(f"{hostname} ({response_ip}) {rtt:.2f} ms", end=" ")
                    except socket.herror:
                        print(f"{response_ip} {rtt:.2f} ms", end=" ")
                        is_dest_reached = True 
                        
                if dest_reached:
                    is_dest_reached = True

        print()
        if args.summary: 
            print(f"{unaswered} probes unanswered")

        if is_dest_reached:
            break

        
#Send a UDP socket 
def send_probe(udp_socket, ttl, dest_ip, dest_port):
    udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)

    udp_packet = b'\x00'
    send_time = time.monotonic()
    udp_socket.sendto(udp_packet, (dest_ip, dest_port))

    return send_time

#REceive an ICMP socket 
def rcv_response(icmp_socket, send_time, timeout, dest_ip, dest_port):
    icmp_socket.settimeout(timeout)

    while True:
        try:
            pkt_data, ip_address = icmp_socket.recvfrom(1024)
            print("Received packet from:", ip_address[0])

            #Extract data from the ICMP packet received 
            ip_header_length = (pkt_data[0] & 0x0F) * 4
            icmp_header = pkt_data[ip_header_length:ip_header_length + 8]

            ip_start = ip_header_length + 8
            ip_length = (pkt_data[ip_start] & 0x0F) * 4
            udp_header_start = ip_start + ip_length

            required_dest_port = int.from_bytes(pkt_data[udp_header_start + 2:udp_header_start + 4])

            dest_ip_address_rcv = ip_address[0]
            type = int.from_bytes(icmp_header[0:1])
            code = int.from_bytes(icmp_header[1:2])

            arr_time = time.monotonic()

            dest_reached = (type == 3 and code == 3 and dest_ip_address_rcv == dest_ip)
            rtt = (arr_time - send_time) * 1000

            if(type != 11 and not (type == 3 and code == 3)):
                continue 

            if required_dest_port != dest_port:
                continue
            
            return dest_ip_address_rcv, rtt, dest_reached
        except socket.timeout:
            # print("ICMP receive timed out")
            return None 
        except OSError as e:
            # print("ICMP socket error:", e)
            return None

if __name__ == "__main__":
    main()

