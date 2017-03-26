import argparse
import socket

from states.follower import Follower
from ftqueue.ftqueue import FTQueue


SERVER_DIRECTORY = {}

SERVER_INFO_NAME_INDEX = 0
SERVER_INFO_LISTEN_PORT_INDEX = 1
SERVER_INFO_IP_ADDR_INDEX = 2
port_list = {8000:'No',8002:'No',8001:'No'}
#ack_port = []

class Server(object):
    def __init__(self, server_directory_index):
        server_info = SERVER_DIRECTORY[server_directory_index]

        self._name = server_info[SERVER_INFO_NAME_INDEX]
        self._ip_addr = server_info[SERVER_INFO_IP_ADDR_INDEX]
        self._listen_port = int(server_info[SERVER_INFO_LISTEN_PORT_INDEX])

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

        self._state = None

        self._ftqueue = FTQueue()

    def run(self):
        self._state = Follower()
        self._state.set_server(self)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self._ip_addr, self._listen_port))
        sock.listen(4)
	if self._listen_port == 8000:
		self._state = 'Master'
	
        while True:
	    #port_list = [8000,8001,8002,8003,8004]
	    
	    port_list[self._listen_port] = 'Yes'
	    for i in port_list:
		if port_list[i] != 'Yes':
		    msg = "hello"
		    try:
                    	sock1= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    	serv_addr=('127.0.0.1',i)
			sock1.connect(serv_addr)
			sock1.sendall(msg)
                    except socket.error as msg:
                    	#print "ERROR - failed to bind to socket:"
                    	sock1.close()
                try:
			print sock1
                	response = sock1.recv(2048)
			sock1.settimeout(2)
                	print response
			#sock1.close()
			if response:
				port_list[i] = 'Yes'
				print port_list
				
		except:
			print 'Error no response'
		else:
			continue
		    
            conn, addr = sock.accept()  # spin off thread?
            #print "CONNECTION ADDRESS: {0}".format(addr)

            message = conn.recv(2048)
	    sock.settimeout(None)
	    #print conn.port()
	    self._log.append(message)
	    if self._state == 'Master':
	    	for i in port_list:
			if port_list[i] == 'Yes' and i != 8000:
	    			if len(message) > 0:
					try:
                    				sock1= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	        				serv_addr=('127.0.0.1',i)
						sock1.connect(serv_addr)
						sock1.sendall(message)
					except socket.error as msg:
                    				#print "ERROR - failed to bind to socket:"
                    				sock1.close()
	    message = ''
	    msg1 = "ack"
	    conn.send(msg1)
	    print self._log
	    
            # process message here; either CLIENT, APPEND_ENTRIES, RESPONSE, or REQUEST_VOTE


            #self.on_message(message)

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server_index', type=int, required=True)

    args = parser.parse_args()

    parse_config()

    s = Server(args.server_index)
    s.run()


def parse_config():
    config_file = file('server.config', 'r')

    id = 0
    for server_info in config_file.readlines():
        SERVER_DIRECTORY[id] = server_info.split()
        id += 1


if __name__ == "__main__":
    main()


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
