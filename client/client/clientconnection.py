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
            'source' : {
                'name' : self.name,
                'side' : None
            },
            'form' : 'signal',
            'data' : {
                'signal_type' : 'connect'
            }
        }

        self.send(json.dumps(connect_signal))

        while self.active:
            try:
                data = self.client_socket.recv(4096).decode('utf8')
           
                sep = '}{'

                splited = data.split(sep)
            
                if len(splited) == 2:
                    splited[0] += '}'
                    splited[1] = '{' + splited[1]
                elif len(splited) > 2:
                    splited[0] += '}'
                    for i in range(1, len(spltied) - 1):
                        splited[i] = '{' + splited[i] + '}'
                    splited[-1] = '{' + splited[-1]


                for s in splited:
                    data_json = json.loads(s) 
                    content = data_json['data']

                    if data_json['form'] == 'signal':
                        self.parse_signal(content)
                    elif data_json['form'] == 'action':
                        self.parse_action(content)
                    elif data_json['form'] == 'message':
                        self.parse_message(content)

            except ConnectionAbortedError:
                print('connection aborted')
                self.active = False


    def parse_signal(self, data):
        if data['signal_type'] == 'onstart':
            self.client.gameboard.load_state(data['state'])
            self.client.gameboard.side = data['color']


    def parse_action(self, data):
        print('RECIEVED ACTION : ' + str(data))
        if data['action_type'] == 'before_turn':
            self.client.gameboard.update_turn(data['cur_turn'])
        elif data['action_type'] == 'movable_response':
            self.client.gameboard.handle_movable_response(data)


    def parse_message(self, data):
        pass


    def send(self, data):
        if self.active:
            print('sending to server : ' + str(data))
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
