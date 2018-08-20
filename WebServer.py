#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import re
import sys

from multiprocessing import Process

HTML_ROOT_DIR = "./html"
WSGI_PYTHON_DIR = "./wsgipython"


class HTTPServer(object):
    """
    PythonHttp服务器
    支持静态文件
    支持py文件
    """
    def __init__(self):
        self.webserver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.webserver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def bind(self, port):
        self.webserver_socket.bind(("", port))

    def start(self):
        """
        多进程服务器
        """
        self.webserver_socket.listen(128)
        while True:
            #等待客户端到来
            self.client_socket, self.client_address = self.webserver_socket.accept()
            print("[%s, %s]用户连接上了服务器" % self.client_address)
            handle_client_process = Process(target=self.handle_client, args=(self.client_socket,))
            handle_client_process.start()
            self.client_socket.close()

    def start_response(self, status, headers):
        '''
        server_headers = [
            ("Server", "My WebServer"),
        ]
        '''
        response_headers = "HTTP/1.1 " + status + "\r\n"
        for header in headers:
            response_headers += "%s: %s\r\n" % header
        self.response_headers = response_headers


    def handle_client(self, client_socket):
        """
        处理客户端请求
        """
        # 获取客户端请求数据
        request_data = client_socket.recv(1024)
        print("requset_data", request_data)
        request_lines = request_data.splitlines()
        for line in request_lines:
            print(line)

        # 提取文件名
        request_start_line = request_lines[0]
        file_name = re.match(r"\w+ +(/[^ ]*)", request_start_line.decode("utf8")).group(1)
        method = re.match(r"(\w+) +/[^ ]*", request_start_line.decode("utf8")).group(1)

        # "time.py"
        if file_name.endswith(".py"):
            try:
                m = __import__(file_name[1:-3])
            except Exception:
                self.response_headers = "HTTP/1.1 404 Not Found\r\n"
                response_body =  "File Not Found"
            else:
                env = {
                    "PATH_INFO": file_name,
                    "Method": method
                }
                response_body = m.application(env, self.start_response)
            response = self.response_headers + "\r\n" + response_body

        else:

            if "/" == file_name:
                file_name = "/index.html"

            try:
                file = open(HTML_ROOT_DIR+file_name, "rb")
            except IOError:
                response_start_line = "HTTP/1.1 200 OK\r\n"
                response_headers = "Server: My server0.2\r\n"
                response_body = "This file not found"
            else:
                file_data = file.read().decode("utf8")
                file.close()
                # 构造响应数据
                response_start_line = "HTTP/1.1 200 OK\r\n"
                response_headers = "Server: My server0.2\r\n"
                response_body = file_data
            response = response_start_line + response_headers + "\r\n" + response_body
        print("response data:", response)
        client_socket.sendall(bytes(response, "utf8"))

        client_socket.close()


def main():
    sys.path.insert(1, WSGI_PYTHON_DIR)
    httpserver = HTTPServer()
    httpserver.bind(8080)
    httpserver.start()


if __name__ == '__main__':
    main()


