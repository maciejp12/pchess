import socket
from threading import Thread
import json


class ClientConnection:


    def __init__(self, cli):
        self.client = cli
        self.client_socket = None
        self.serv_addr = '127.0.0.1'
        self.serv_port = 6667
        self.active = True
        self.name = 'temp_name'


    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.serv_addr, self.serv_port))

            self.thread = Thread(target=self.run, daemon=True)
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
                
                data_json = json.loads(data) 
                
                if data_json['form'] == 'signal':
                    self.parse_signal(data_json['data'])
                elif data_json['form'] == 'action':
                    self.parse_action(data_json['data'])
                elif data_json['form'] == 'message':
                    self.parse_message(data_json['data'])

            except ConnectionAbortedError:
                print('connection aborted')
                self.active = False


    def parse_signal(self, data):
        if data['signal_type'] == 'onstart':
            self.client.gameboard.load_state(data['state'])
            self.client.gameboard.side = data['color']


    def parse_action(self, data):
        pass


    def parse_message(self, data):
        pass


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
