"""
- NOTE: REPLACE 'N' Below with your section, year, and lab number
- CS2911 - 0NN
- Fall 202N
- Lab N
- Names:
  - 
  - 

An HTTP server

Introduction: (Describe the lab in your own words)




Summary: (Summarize your experience with the lab, what you learned, what you liked,what you disliked, and any suggestions you have for improvement)





"""

import socket
import re
import threading
import os
import mimetypes
import datetime


def main():
    """ Start the server """
    http_server_setup(8080)


def http_server_setup(port):
    """
    Start the HTTP server
    - Open the listening socket
    - Accept connections and spawn processes to handle requests

    :param port: listening port number
    """

    num_connections = 10
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_address = ('', port)
    server_socket.bind(listen_address)
    server_socket.listen(num_connections)
    try:
        while True:
            request_socket, request_address = server_socket.accept()
            print('connection from {0} {1}'.format(request_address[0], request_address[1]))
            # Create a new thread, and set up the handle_request method and its argument (in a tuple)
            request_handler = threading.Thread(target=handle_request, args=(request_socket,))
            # Start the request handler thread.
            request_handler.start()
            # Just for information, display the running threads (including this main one)
            print('threads: ', threading.enumerate())
    # Set up so a Ctrl-C should terminate the server; this may have some problems on Windows
    except KeyboardInterrupt:
        print("HTTP server exiting . . .")
        print('threads: ', threading.enumerate())
        server_socket.close()


def handle_request(request_socket):
    """
    Handle a single HTTP request, running on a newly started thread.

    Closes request socket after sending response.

    Should include a response header indicating NO persistent connection

    :param request_socket: socket representing TCP connection from the HTTP client_socket
    :return: None
    """

    pass  # Replace this line with your code


# ** Do not modify code below this line.  You should add additional helper methods above this line.

# Utility functions
# You may use these functions to simplify your code.


def get_mime_type(file_path):
    """
    Try to guess the MIME type of a file (resource), given its path (primarily its file extension)

    :param file_path: string containing path to (resource) file, such as './abc.html'
    :return: If successful in guessing the MIME type, a string representing the content type, such as 'text/html'
             Otherwise, None
    :rtype: int or None
    """

    mime_type_and_encoding = mimetypes.guess_type(file_path)
    mime_type = mime_type_and_encoding[0]
    return mime_type


def get_file_size(file_path):
    """
    Try to get the size of a file (resource) as number of bytes, given its path

    :param file_path: string containing path to (resource) file, such as './abc.html'
    :return: If file_path designates a normal file, an integer value representing the the file size in bytes
             Otherwise (no such file, or path is not a file), None
    :rtype: int or None
    """

    # Initially, assume file does not exist
    file_size = None
    if os.path.isfile(file_path):
        file_size = os.stat(file_path).st_size
    return file_size

def find_file(file_name):
    os.path.exists("./" + file_name)  #checks if file exists


def status_line_builder(response_number, file_name = "404.html"):
    """
    :Author: Adrianne Schellinger
    If your confused by file_name = "", it just means that the input parameter is optional.
    :param response_number: int indicating type of response to build
    :param file_name, if needed
    :return: A response.
    """

    response = ""
    timestamp = datetime.datetime.utcnow()
    timestring = timestamp.strftime('%a, %d %b %Y %H:%M:%S GMT')
    # Sun, 06 Nov 1994 08:49:37 GMT
    #200 OK
    #Note: this is a bad way of doing this, this will be very slow, but it will work for now.
    if response_number == 200:
        file_object = open(file_name, "rb")
        response += "HTTP/1.1 200 OK\r\n"
        response += "Date: " + timestring + "\r\n"
        response += "Connection: close\r\n"
        response += "Content Length: " + str(get_file_size(file_name)) + "\r\n"
        response += "Content Type: " + str(get_mime_type(file_name)) + "\r\n"
        response += "\r\n"
        response.encode()
        response += file_object.read()
        file_object.close()

    if response_number == 404: #impliments a custom 404 page
        file_object = open(file_name, "rb")
        response += "HTTP/1.1 404 Not Found\r\n"
        response += "Date: " + timestring + "\r\n"
        response += "Connection: close\r\n"
        response += "Content Length: " + str(get_file_size(file_name)) + "\r\n"
        response += "Content Type: " + get_mime_type(file_name) + "\r\n"
        response += "\r\n"
        response.encode()
        response += file_object.read()
        file_object.close()
    if response_number == 400:
        response += "HTTP/1.1 400 Bad Request\r\n"
        response.encode()

    return response
def next_byte(data_socket):
    """
    Read the next byte from the socket data_socket.

    Read the next byte from the sender, received over the network.
    If the byte has not yet arrived, this method blocks (waits)
      until the byte arrives.
    If the sender is done sending and is waiting for your response, this method blocks indefinitely.

    :param data_socket: The socket to read from. The data_socket argument should be an open tcp
                        data connection (either a client socket or a server data socket), not a tcp
                        server's listening socket.
    :return: the next byte, as a bytes object with a single byte in it
    """

    return data_socket.recv(1)

main()

# Replace this line with your comments on the lab
