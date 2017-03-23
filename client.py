import socket

from messages.client_request import ClientRequestMessage


Q_CREATE_COMMAND_STR = 'qcreate'
Q_ID_COMMAND_STR = 'qid'
Q_POP_COMMAND_STR = 'qpop'
Q_PUSH_COMMAND_STR = 'qpush'
Q_TOP_COMMAND_STR = 'qtop'
Q_SIZE_COMMAND_STR = 'qsize'


class FTQueueClient(object):

    def run(self):
        print "Welcome to the FTQClient. You may being entering commands below."

        self.print_usage()

        while True:
            user_input = raw_input('> ')

            client_request, err_msg = self.parse_client_request(user_input)

            if client_request == None:
                print "ERROR - " + err_msg

            else:
                server_addr = (client_request._dst_ip_addr, client_request._dst_port)

                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect(server_addr)
                except socket.error as msg:
                    print "ERROR - failed to bind to socket: {0}:{1}".format(server_addr[0], server_addr[1])
                    sock.close()
                    continue

                sock.sendall(client_request.to_string())

                response = sock.recv(2048)
                print response

                sock.close()

    def print_usage(self):
        print "COMMAND := <IP ADDR> <PORT> <COMMAND_KEY> <ARG>+"
        print "COMMAND_KEY := [Q_CREATE_COMMAND, Q_ID_COMMAND, Q_POP_COMMAND, Q_PUSH_COMMAND, Q_TOP_COMMAND, " \
              "Q_SIZE_COMMAND]"
        print "Q_CREATE_COMMAND := \'qcreate (int label)\'"
        print "    Q_ID_COMMAND := \'qid     (int label)\'"
        print "   Q_POP_COMMAND := \'qpop    (int queue_id, int item)\'"
        print "  Q_PUSH_COMMAND := \'qpush   (int queue_id)\'"
        print "   Q_TOP_COMMAND := \'qtop    (int queue_id)\'"
        print "  Q_SIZE_COMMAND := \'qsize   (int queue_id)\'"

    def parse_client_request(self, user_input):
        input_tokens = user_input.split()

        if len(input_tokens) < 3:
            return None, "invalid command: {0}".format(user_input)

        dst_ip_addr = input_tokens[0]
        dst_port = int(input_tokens[1])
        command_str = input_tokens[2].lower()
        args_list = input_tokens[3:]

        if not self.validate_dst_ip_addr(dst_ip_addr):
            return None, "invalid ip address: {0}".format(dst_ip_addr)

        if not self.validate_dst_port(dst_port):
            return None, "invalid port number: {0}".format(dst_port)

        if not self.validate_command_token(command_str, args_list):
            return None, "invalid command: {0} {1}".format(command_str, args_list)

        return ClientRequestMessage(dst_ip_addr, dst_port, command_str, args_list), None

    def validate_dst_ip_addr(self, dst_ip_addr):
        if dst_ip_addr == '':
            return False

        ip_octets = dst_ip_addr.split('.')
        if len(ip_octets) != 4:
            return False

        for octet in ip_octets:
            if octet != '' and (int(octet) < 0 or int(octet) > 255):
                return False

        return True

    def validate_dst_port(self, dst_port):
        if dst_port < 0 or dst_port > 65535:
            return False

        return True

    def validate_command_token(self, command_str, args_list):
        if command_str == Q_CREATE_COMMAND_STR and len(args_list) == 1:
            return True
        elif command_str == Q_ID_COMMAND_STR and len(args_list) == 1:
            return True
        elif command_str == Q_PUSH_COMMAND_STR and len(args_list) == 2:
            return True
        elif command_str == Q_POP_COMMAND_STR and len(args_list) == 1:
            return True
        elif command_str == Q_TOP_COMMAND_STR and len(args_list) == 1:
            return True
        elif command_str == Q_SIZE_COMMAND_STR and len(args_list) == 1:
            return True
        else:
            return False


if __name__ == "__main__":
    client = FTQueueClient()
    client.run()
