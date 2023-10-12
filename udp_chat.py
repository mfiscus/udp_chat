import datetime
import re
import socket
import sys
import threading
from os import system, name


# define clear function
def __clear():
 
    # for windows
    if name == 'nt':
        _ = system('cls')
 
    # for mac and linux (here, os.name is 'posix')
    else:
        _ = system('clear')


# Function to send messages
def __send_message(host, port):

    try:

        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        while True:

            # Generate input prompt
            message = input( '\nTo ' + '\x1b[1;34;40m' + host.split('.')[0] + '\x1b[0m\n' + '\x1b[0;32;40m' + '• ' + '\x1b[0m' )
            
            
            # Check if the user wants to exit
            if message.lower() == 'exit':
                break
            
            # Send the message to the specified host and port
            sock.sendto(message.encode(), (host, port))
    
    
        # Close the socket when done
        sock.close()

    except Exception as e:

        print(f'Error: {str(e)}')


# Function to receive messages
def __receive_messages(host, port):

    try:

        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Bind the socket to the specified host and port
        sock.bind((host, port))
        
        while True:

            data, addr = sock.recvfrom(port)
            timestamp = datetime.datetime.now()
            ipaddr = addr[0]

            # strip fqdn to get hostname
            fromhost = socket.gethostbyaddr(ipaddr)[0].split('.')[0]
            print('\r \nFrom ' + '\x1b[1;34;40m' + fromhost + '\x1b[0m' + ' at ' + timestamp.strftime('%Y/%m/%d %H:%M:%S'))
            print( '\x1b[1;34;40m\r' + '• ' + '\x1b[0m' + f'{data.decode()}\n\n' + 'To ' + '\x1b[1;34;40m' + fromhost + '\x1b[0m\n' + '\x1b[0;32;40m' + '• ' + '\x1b[0m', end='' )

        
    except Exception as e:

        print(f'Error: {str(e)}')
    

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print( '\nUsage: python ' + sys.argv[0] + ' <host> <port>\n' )
        sys.exit(1)
    
    send_host = sys.argv[1]
    port = 30847
    receive_host = socket.gethostname()

    # Clear screen and print title
    __clear()
    print( '\x1b[0m\nSend message to ' + '\x1b[1;34;40m' + send_host.split('.')[0] + '\x1b[0m' )
    
    # Create two threads for sending and receiving messages
    send_thread = threading.Thread(target=__send_message, args=(send_host, port))
    receive_thread = threading.Thread(target=__receive_messages, args=(receive_host, port))
    
    # Start the threads
    send_thread.start()
    receive_thread.start()
    
    # Wait for both threads to finish
    send_thread.join()
    receive_thread.join()
