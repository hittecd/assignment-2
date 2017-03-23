CLIENT_REQUEST_MESSAGE_TYPE = "CLIENT_MESSAGE"

MSG_TYPE_INDEX = 0
COMMAND_INDEX = 1
ARG_LIST_INDEX = 2


class ClientRequestMessage(object):
    def __init__(self, command, arg_list):
        self._msg_type = CLIENT_REQUEST_MESSAGE_TYPE
        self._command = command
        self._arg_list = arg_list

    def to_string(self):
        arg_tokens = ""
        for arg in self._arg_list:
            arg_tokens += str(arg)

        return "CLIENT_MESSAGE {0} {1}".format(self._command, arg_tokens)

    @staticmethod
    def from_string(message):
        request_tokens = message.split()

        command= request_tokens[COMMAND_INDEX]

        arg_list_tokens = request_tokens[ARG_LIST_INDEX:]
        arg_list = []

        for arg_token in arg_list_tokens:
            arg_list.append(int(arg_token))

        return ClientRequestMessage(command, arg_list)

    @staticmethod
    def from_client_command(client_command):
        return ClientRequestMessage(client_command._command, client_command._arg_list)

    @staticmethod
    def is_client_message(message):
        msg_tokens = message.split()
        msg_type = msg_tokens[MSG_TYPE_INDEX]

        return msg_type == CLIENT_REQUEST_MESSAGE_TYPE

