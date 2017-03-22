import socket

from server.states.follower import Follower


SERVER_DIRECTORY = {0: ('SERVER-0', 8000, '127.0.0.1'),
                    1: ('SERVER-1', 8001, '127.0.0.1'),
                    2: ('SERVER-2', 8002, '127.0.0.1'),
                    3: ('SERVER-3', 8003, '127.0.0.1'),
                    4: ('SERVER-4', 8004, '127.0.0.1')}

SERVER_INFO_NAME_INDEX = 0
SERVER_INFO_LISTEN_PORT_INDEX = 1
SERVER_INFO_IP_ADDR_INDEX = 2


class Server(object):
    def __init__(self, server_directory_index):
        server_info = SERVER_DIRECTORY[server_directory_index]

        self._name = server_info[SERVER_INFO_NAME_INDEX]
        self._ip_addr = server_info[SERVER_INFO_IP_ADDR_INDEX]
        self._listen_port = server_info[SERVER_INFO_LISTEN_PORT_INDEX]

        self._neighbors = []
        # for server_info in SERVER_DIRECTORY.values():
        #     server_name = server_info[SERVER_INFO_NAME_INDEX]
        #
        #     if server_name != self._name:
        #         self._neighbors[server_name] =

        self._log = []
        self._commitIndex = 0
        self._currentTerm = 0
        self._lastApplied = 0
        self._lastLogIndex = 0
        self._lastLogTerm = None

        self._state = Follower()
        self._state.set_server(self)

        self._queue_table = {}

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.bind((self._ip_addr, self._listen_port))

        self._sock.listen(4)
        while True:
            conn, addr = self._sock.accept()
            print "CONNECTION ADDRESS: {0}".format(addr)

            message = conn.recv(2048)

            # process message here; either CLIENT, APPEND_ENTRIES, RESPONSE, or REQUEST_VOTE

            self.on_message(message)

    def send_message(self, message):
        for n in self._neighbors:
            message._receiver = n._name
            n.post_message(message)

    def send_message_response(self, message):
        n = [n for n in self._neighbors if n._name == message.receiver]
        if (len(n) > 0):
            n[0].post_message(message)

    def post_message(self, message):
        self._messageBoard.post_message(message)

    def on_message(self, message):
        state, response = self._state.on_message(message)

        self._state = state


# class ZeroMQServer(Server):
#     def __init__(self, name, state, log, messageBoard, neighbors, port=6666):
#         super(ZeroMQServer, self).__init__(name, state, log, messageBoard, neighbors)
#         self._port = 6666
#
#         class SubscribeThread(threading.Thread):
#             def run(thread):
#                 context = zmq.Context()
#                 socket = context.socket(zmq.SUB)
#                 for n in neighbors:
#                     socket.connect("tcp://%s:%d" % (n._name, n._port))
#
#                 while True:
#                     message = socket.recv()
#                     self.on_message(message)
#
#         class PublishThread(threading.Thread):
#             def run(thread):
#                 context = zmq.Context()
#                 socket = context.socket(zmq.PUB)
#                 socket.bind("tcp://*:%d" % self._port)
#
#                 while True:
#                     message = self._messageBoard.get_message()
#                     if not message:
#                         continue  # sleep wait?
#                     socket.send(message)
#
#         self.subscribeThread = SubscribeThread()
#         self.publishThread = PublishThread()
#
#         self.subscribeThread.daemon = True
#         self.subscribeThread.start()
#         self.publishThread.daemon = True
#         self.publishThread.start()
