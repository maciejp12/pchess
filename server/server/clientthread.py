from threading import Thread
from datetime import datetime
import json


class ClientThread:


    def __init__(self, addr, conn, serv):
        self.address = addr
        self.connection = conn
        self.server = serv
        self.active = True
    
        self.name = None
        self.id = None


    def connect(self):
        while self.active:
            try:
                data = self.connection.recv(4096).decode('utf8')
                if not data:
                    break
                buf = ''
                buf = buf + data
                if buf is not None and buf != '':
                    self.parse_data(buf)
                else:
                    print('empty buffer error')
            except ConnectionResetError:
                print('conn error in client thread')
                self.end_connection()


    def parse_data(self, data):
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

            if self.server.print_debug:
                green = '\033[92m'
                white = '\033[00m'
                print(f'{green}RECIEVED:{data_json}{white}')

            if form == 'signal':
                self.parse_signal(data_json)
            elif form == 'message':
                self.parse_message(data_json)
            elif form == 'action':
                self.parse_action(data_json)

    
    def parse_signal(self, data):
        signal = data['data']['signal_type']
        source = data['source']

        if signal == 'connect':
            self.name = source['name']
            self.id = self.server.connected_clients.index(self)
           
            self.server.game.handle_on_connect(self)

        if signal == 'disconnect':
            self.end_connection()

    
    def parse_message(self, data):

        """
            After recieving message signal from one of clients respond to all
            clients in sources client game with message signal with data of 
            source, recieved message text and current datetime
        """

        msg_response = {
            'form' : 'message',
            'data' : {
                'source' : data['source'],
                'content' : data['data']['content'],
                'datetime' : str(datetime.now())
            }
        }

        self.server.game.send_to_all(json.dumps(msg_response))

    def parse_action(self, data):
        action = data['data']
        action_type = action['action_type']

        if action_type == 'get_movable':
           
            self.server.game.handle_get_movable(data, self)
        elif action_type == 'move':
          
            self.server.game.handle_move(data, self)
        elif action_type == 'promotion_response':
            self.server.game.handle_promotion_response(data, self)


    def start_connection(self):
        thread = Thread(target=self.connect, daemon=True)
        thread.start()


    
    def end_connection(self):
        self.active = False
        self.connection.close()
        self.server.remove_client(self)
        print('Client ' + self.name + ' ' + str(self.id) + ' disconnected')


    def send_data(self, data):
        if self.active:
            if self.server.print_debug:
                blue = '\033[94m'
                white = '\033[00m'
                print(f'{blue}SENDING :{data}{white}')

            encoded = data.encode('utf8')
            self.connection.send(encoded)

