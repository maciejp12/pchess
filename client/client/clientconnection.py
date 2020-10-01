import socket
from threading import Thread
import json


class ClientConnection:


    def __init__(self):
        self.client_socket = None
        self.serv_addr = '127.0.0.1'
        self.serv_port = 6667
        self.active = True
        self.name = 'temp_name'


    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.serv_addr, self.serv_port))

            self.thread = Thread(target=self.run)
            self.thread.start()
        except ConnectionRefusedError:
            print('cannont connect to server')


    def run(self):
        connect_signal = {
            'source' : self.name,
            'form' : 'signal',
            'data' : {
                'signal_type' : 'connect'
            }
        }

        self.send(json.dumps(connect_signal))

        while self.active:
            try:
                data = self.client_socket.recv(4096).decode('utf8')
                print(data)
            except ConnectionAbortedError:
                print('connection aborted')
                self.active = False


    def send(self, data):
        if self.active:
            self.client_socket.send(data.encode('utf8'))


    def disconnect(self):
        self.active = False

        disconnect_signal = {
            'source' : self.name,
            'form' : 'signal',
            'data' : {
                'signal_type' : 'disconnect'
            }
        }

        self.send(json.dumps(disconnect_signal))

        self.client_socket.close()

