#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

#


# Commands to run on terminal
# python httpclient.py POST https://google.ca
# python httpclient.py GET https://google.ca
# python httpclient.py GET https://www.google.ca/ ### PATH doesn't pick up '/' at the end unless specified

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):

    def connect(self, host, port):
        # from Lab 2: create socket, connect, and recieve data

        # If no port was specified set to port 80
        if port == None:
            port = 80

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))

            print(f"Connected to {host}:{port}")

        except Exception as e:
            print(e)
            print('Hostname could not be resolved. Exiting')
            sys.exit()
        
        return self.socket

    # curl -v curl -v https://www.google.ca showed curl/7.64.1
    # Documentation used:
    #https: // developer.mozilla.org/en-US/docs/Web/HTTP/Messages
    #https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept
    #https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent
    # @ args: request_type,  host
    def get_headers(self, request_type, host, user_agent="curl/7.64.1", content_type="application/x-www-form-urlencoded"):

        if request_type == "GET":
            headers = f"""User-Agent: {user_agent}\r\nHost: {host}\r\nAccept: */*\r\nAccept-Charset: utf-8\r\nConnection: close\r\n\r\n
            """

        if request_type == "POST":
            pass

        return headers


    def get_code(self, data):
        # index 1 is the status code in the response
        code = int(data.split()[1])
        return code 

    
    def get_body(self, data):
        try:
            # Index 1 cause there is a empty line before
            body = data.split("\r\n\r\n")[1]
            return body
        except:
            return ""
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')
    
    # https://docs.python.org/3/library/urllib.parse.html
    def GET(self, url, args=None):
        
        parsed_url = urllib.parse.urlparse(url)
        print(parsed_url)
        
        # Variables intiated
        request_type = "GET"
        host = parsed_url.hostname
        port = parsed_url.port
        path = parsed_url.path
        if path == "":
            path = "/"

        query = parsed_url.query
        if (query == ""):
            print("NO QUERY")

        # Connect with host:port / OPEN CONNECTION
        self.socket = self.connect(host,port)
        
        status_line = "GET " + path + " HTTP/1.1\r\n"

        headers = self.get_headers(request_type, host)
        request = status_line + headers
        print("\n-----------GET REQUEST-----------")
        print(request)
        
        # Send GET Request through the open connection
        self.sendall(request)
        
        # Recieve data returned to the  socket
        response = self.recvall(self.socket)

        print("----------- RESPONSE -----------")
        print(response)

        # Parse response from socket
        code = self.get_code(response)
        body = self.get_body(response)

        # CLOSE CONNECTION
        self.close()

        print(f"Code: {code}\n")
        print("Body:\n")
        print(body)


        return HTTPResponse(code, body) 

    def POST(self, url, args=None):
        code = 500
        body = ""

        request_type = "POST"
        print("---------POST REQUEST-----------")
        return HTTPResponse(code, body)






    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
