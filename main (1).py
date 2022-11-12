"""
- CS2911 - 011
- Fall 2021
- Lab 6
- Names:
  -Augustus Sorci
  -Adrianne Schellinger

An HTTP server

Introduction: This lab completed the task of handling and http request and sending a response.
The runtime of our implementation is a bit on the higher end, but if you look past the superficial
errors you will see that this lab has each component mentioned in the design and more.

Summary: It was difficult conceptually to understand how to ensure that the HTTP request was formatted
correctly, but in the end we compared it to a template string of what the request looks like after
all of the attributes and such are parsed out. Other problems arose but that was the most prominent one.

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
     :author: Augustus Sorci
     :param request_socket:
     :return:
     """
    """
    Handle a single HTTP request, running on a newly started thread.

    Closes request socket after sending response.

    Should include a response header indicating NO persistent connection

    :param request_socket: socket representing TCP connection from the HTTP client_socket
    :return: None
    """
    request, status = request_interpreter(request_socket)
    request_copy = request
    file_name = parse_file_name(request)
    response = make_response_string(status, file_name)
    response = response.encode('ascii')
    request_socket.send(response)
    request_socket.close()


def request_interpreter(request_socket):
    sample = "GETHTTP/1.1\r\n"
    request = request_reader(request_socket)
    request_copy = request
    file_name = parse_file_name(request)
    header_lines = dictionary(request_copy)
    keys = header_lines.keys()
    values = header_lines.values()
    for x in keys:
        if request.__contains__(x):
            request.replace(x, "")
    for x in values:
        if request.__contains__(x):
            request.replace(x, "")
    if request.__contains__(sample):
        return file_name, 200
    else:
        return file_name, 404


def dictionary(request):
    req = request
    index = req.index("\r\n")
    str2 = req[index + 1: len(req)]
    lines = str2.split("\r\n")
    x = len(lines)
    pairs = {"": ""}
    for i in range(x):
            egg = lines[i].split(":")
            print(len(egg))
            if len(egg) > 1:
                pairs[egg[0]] = egg[1]+"\r\n"

    return pairs


def parse_file_name(request):
    file_name = " "
    stri = str(request)
    print(stri)
    if stri == "/":
        return "index.html"
    else:
        if stri.__contains__(" "):
            array = stri.split(" ")
            file_name = array[1]
        else:
            file_name = "404.html"
    return file_name


def request_reader(request_socket):
    b = b'\0x'
    request = b'\0x'
    while not request.endswith(b'\r\n\r\n'):
        request += read_next_line(request_socket)

    return request.decode()


def make_response_string(response_number, file_name="404.html"):
    """
    :Author: Adrianne Schellinger
    If your confused by file_name = "", it just means that the input parameter is optional.
    :param response_number: int indicating type of response to build
    :param file_name, if needed
    :return: A response.
    """
    response = ""
    if file_name == "GET":
        file_name = "404.html"
    timestamp = datetime.datetime.utcnow()
    timestring = timestamp.strftime('%a, %d %b %Y %H:%M:%S GMT')
    # Sun, 06 Nov 1994 08:49:37 GMT
    # 200 OK
    # Note: this is a bad way of doing this, this will be very slow, but it will work for now.
    if response_number == 200:
        print(file_name+"<-- there should be a file_name right there")
        file_object = open(file_name, "rb")
        response += "HTTP/1.1 200 OK\r\n"
        response += "Date: " + timestring + "\r\n"
        response += "Connection: close\r\n"
        response += "Content Length: " + str(get_file_size(file_name)) + "\r\n"
        response += "Content Type: " + str(get_mime_type(file_name)) + "\r\n"
        response += "\r\n"
        response += str(file_object.read())
        response.encode()
        file_object.close()

    if response_number == 404:  # impliments a custom 404 page
        print(file_name + "<-- there should be another file name here")
        file_object = open(file_name, "rb")
        response += "HTTP/1.1 404 Not Found\r\n"
        response += "Date: " + timestring + "\r\n"
        response += "Connection: close\r\n"
        response += "Content Length: " + str(get_file_size(file_name)) + "\r\n"
        response += "Content Type: " + str(get_mime_type(file_name)) + "\r\n"
        response += "\r\n"
        response.encode()
        response += str(file_object.read())
        file_object.close()
    if response_number == 400:
        response += "HTTP/1.1 400 Bad Request\r\n"
        response.encode()

    return response


def next_byte(data_socket):
    """
       :author: Adrianne Schellinger
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


def read_file():
    print()


def attach_payload(status_code):
    print()


def read_next_line(data_socket):
    """
      :author: Augustus Sorci
      :param data_socket: The socket used to do my bidding
    """
    end = False
    line = b''
    second_store = b'-1'
    while not end:
        store = next_byte(data_socket)
        line += store
        if second_store == b'\r' and store == b'\n':
            end = True
        if store == b'\r':
            second_store = store
    return line[:len(line)]


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

# I enjoyed this and that and the other thing.
main()