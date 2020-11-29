import socket
from threading import Thread
import json
from random import randint


class ClientConnection:


    def __init__(self, cli):
        self.client = cli
        self.client_socket = None
        self.serv_addr = '127.0.0.1'
        self.serv_port = 6667
        self.active = True
        self.name = 'temp_name' + str(randint(0, 1024))


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

                splited = list()

                decoder = json.JSONDecoder()
                pos = 0

                while True:
                    try:
                        cur, pos = decoder.raw_decode(data, pos)
                        splited.append(cur)
                    except json.JSONDecodeError:
                        break


                for data_json in splited: 
                    form = data_json['form']
                    content = data_json['data']
                     
                    green = '\033[92m'
                    white = '\033[00m'
                    print(f'{green}RECIEVED:{data_json}{white}')

                    if form == 'signal':
                        self.parse_signal(content)
                    elif form == 'action':
                        self.parse_action(content)
                    elif form == 'message':
                        self.parse_message(content)

            except ConnectionAbortedError:
                print('connection aborted')
                self.active = False


    def parse_signal(self, data):
        if data['signal_type'] == 'onstart':
            self.client.waiting = False
            self.client.connected = True
            self.client.in_game = True

            self.client.gameboard.load_state(data['state'])
            self.client.gameboard.side = data['color']
            self.client.gameboard.turn = data['turn']
        elif data['signal_type'] == 'waiting':
            self.client.waiting = True
            self.client.connected = True
            self.client.in_game = False

    def parse_action(self, data):
        if data['action_type'] == 'before_turn':
            self.client.gameboard.update_turn(data)
        elif data['action_type'] == 'movable_response':
            self.client.gameboard.handle_movable_response(data)
        elif data['action_type'] == 'invalid_move':
            self.client.gameboard.on_invalid_move(data)
        elif data['action_type'] == 'after_promotion':
            self.client.gameboard.after_promotion(data)


    def parse_message(self, data):
        self.client.handle_message(data)


    def send(self, data):
        if self.active:
            blue = '\033[94m'
            white = '\033[00m'
            print(f'{blue}SENDING :{data}{white}')
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
