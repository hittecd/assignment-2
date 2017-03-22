import socket


Q_CREATE_COMMAND_STR = 'qcreate'
Q_ID_COMMAND_STR = 'qid'
Q_POP_COMMAND_STR = 'qpop'
Q_PUSH_COMMAND_STR = 'qpush'
Q_TOP_COMMAND_STR = 'qtop'
Q_SIZE_COMMAND_STR = 'qsize'


class FTQueueClient:

    def run(self):
        print "Welcome to the FTQClient. You may being entering commands below."

        self.print_usage()

        while True:
            user_input = raw_input('> ')

            command, err_msg = self.parse_command(user_input)

            if command == None:
                print "ERROR - " + err_msg

            else:
                server_addr = (command._ip_addr, command._port)

                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect(server_addr)
                except socket.error as msg:
                    print "ERROR - failed to bind to socket: {0}:{1}".format(server_addr[0], server_addr[1])
                    sock.close()
                    continue

                sock.sendall(command.get_request())

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

    def parse_command(self, user_input):
        input_tokens = user_input.split()

        if len(input_tokens) < 3:
            return None, "invalid command: {0}".format(user_input)

        ip_addr = input_tokens[0]
        port = int(input_tokens[1])
        command_str = input_tokens[2].lower()
        args_list = input_tokens[3:]

        if not self.validate_ip_token(ip_addr):
            return None, "invalid ip address: {0}".format(ip_addr)

        if not self.validate_port_token(port):
            return None, "invalid port number: {0}".format(port)

        if not self.validate_command_token(command_str, args_list):
            return None, "invalid command: {0} {1}".format(command_str, args_list)

        return self.Command(ip_addr, port, command_str, args_list), None

    def validate_ip_token(self, ip_addr):
        if ip_addr == '':
            return False

        ip_octets = ip_addr.split('.')
        if len(ip_octets) != 4:
            return False

        for octet in ip_octets:
            if octet != '' and (int(octet) < 0 or int(octet) > 255):
                return False

        return True

    def validate_port_token(self, port):
        if port < 0 or port > 65535:
            return False

        return True

    def validate_command_token(self, command_str, args_list):
        if command_str == Q_CREATE_COMMAND_STR and len(args_list) == 1:
            return True
        elif command_str == Q_ID_COMMAND_STR and len(args_list) == 1:
            return True
        elif command_str == Q_POP_COMMAND_STR and len(args_list) == 2:
            return True
        elif command_str == Q_PUSH_COMMAND_STR and len(args_list) == 1:
            return True
        elif command_str == Q_TOP_COMMAND_STR and len(args_list) == 1:
            return True
        elif command_str == Q_SIZE_COMMAND_STR and len(args_list) == 1:
            return True
        else:
            return False

    class Command:
        def __init__(self, ip_addr, port, command, args_list):
            self._ip_addr = ip_addr
            self._port = port
            self._command = command
            self._args = args_list

        def get_request(self):
            arg_string = ""
            for arg in self._args:
                arg_string += (str(arg) + ' ')

            return "{0} {1}".format(self._command, self._args)


if __name__ == "__main__":
    client = FTQueueClient()
    client.run()
