# Ping and Traceroute 
### CSCI 651 Fall 2026
### Homework 2
### Katy Richardson

## How to compile the code:
This program is written in Python, and does not require any specific compilation steps. Be sure to install all dependencies from `requirements.txt`.

## How to run the code 
In order to run the code, you will need to open the command line and run:
`python my_ping.py [ip address]' to run my_ping.py
or
`python my_traceroute.py [ip address]' to run my_traceroute.py 

## Ping

This program allows flags to 
- Limit the number of packets received -c
- Wait a specific amount of time between pings -i
- Specify the packet size sent in the ping -s
- Specify the timeout for the program in seconds -t

### Example Command-Line Usage 
``` python my_ping.py 8.8.8.8
    python my_ping.py -c 5 8.8.8.8
    python my_ping.py -i 2 8.8.8.8
    python my_ping.py -s 52 8.8.8.8
    python my_ping.py -t 15 8.8.8.8
 ```

 ## Traceroute 

 This program allows the following flags
 - -n -> Print hop address strictly numerically 
 - -q -> Set the number of probes for hop 
 - -S -> A summary of how many probes were not answered 

 ### Example Command-Line Usage 
``` python my_traceroute.py 8.8.8.8
    python my_traceroute.py -n 8.8.8.8
    python my_traceroute.py -q 5 8.8.8.8
    python my_traceroute.py -S 8.8.8.8
 ```