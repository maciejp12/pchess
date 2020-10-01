from threading import Thread
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
        data = json.loads(data)
        form = data['form']

        if form == 'signal':
            self.parse_signal(data)
        elif form == 'message':
            self.parse_message(data)
        elif form == 'action':
            self.parse_action(data)

    
    def parse_signal(self, data):
        signal = data['data']['signal_type']
        source = data['source']

        if signal == 'connect':
            self.name = source
            self.id = self.server.connected_clients.index(self)

        if signal == 'disconnect':
            self.end_connection()

    
    def parse_message(self, data):
        pass


    def parse_action(self, data):
        pass
        

    def start_connection(self):
        thread = Thread(target=self.connect)
        thread.start()


    
    def end_connection(self):
        self.active = False
        self.connection.close()
        self.server.remove_client(self)
        print('Client ' + self.name + ' ' + str(self.id) + ' disconnected')


    def send_data(self, data):
        encoded = data.encode('utf8')
        self.connection.send(encoded)