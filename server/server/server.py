import socket
from threading import Thread
from .clientthread import ClientThread
from .gamestate import GameState


class ChessServer:


    def __init__(self):
        self.address = '127.0.0.1'
        self.port = 6667
        self.server = None
        self.connected_clients = []
        self.running = False
        self.game = GameState()
        self.game.init_pieces()


    def start_server(self):
        print('Starting on : (' + self.address + ', ' + str(self.port) + ')')
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.address, self.port))
        self.server.listen(1)
        self.running = True

        print('Starting server completed')

        thread = Thread(target=self.start_listening, daemon=True)
        thread.start()
        
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print('ki')
            self.running = False
            self.on_disconnect()


    def start_listening(self):
        print('listening on : (' + self.address + ', ' + str(self.port) + ')')
 
        conn = None    
        
        while self.running:
            try:
                conn, addr = self.server.accept()
                self.handle_client(addr, conn)
            except:
                print('conn error')
                self.running = False
                self.on_disconnect()


    def handle_client(self, addr, conn):
        print('new client : (' + str(addr) + ', ' + str(conn) + ')')
        new_client = ClientThread(addr, conn, self)
        self.connected_clients.append(new_client)
        new_client.start_connection()
        
        print(self.connected_clients)


    def send_to_all(self, data):
        """
            send data to all connected clients
        """

        for client in self.connected_clients:
            client.send_data(data)

    
    def on_disconnect(self):
        """
            send disconnect signal to all connected clients
            close all connections before shuting down server
        """

        for client in self.connected_clients:
            client.end_connection()
        self.server.close()


    def remove_client(self, client):
        """
            remove client form clients list
        """

        self.connected_clients.remove(client)
        print(self.connected_clients)



# package {
# source : name
# form : signal, message, action
# data : dep on type (dict)
#}
