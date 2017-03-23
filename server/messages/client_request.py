import json

from base import MSG_TYPE_KEY
from base import BaseMessage


CLIENT_REQUEST_MESSAGE_TYPE = "CLIENT_REQUEST_MESSAGE"

SRC_IP_ADDR_KEY = "scr_ip_addr"
SRC_PORT_KEY = "src_port"

DST_IP_ADDR_KEY = "dst_ip_addr"
DST_PORT_KEY = "dst_port"

COMMAND_KEY = "command"
ARGS_LIST_KEY = "args_list"


class ClientRequestMessage(BaseMessage):
    def __init__(self, dst_ip_addr, dst_port, command, args_list):
        self._src_ip_addr = ""
        self._src_port = ""

        self._dst_ip_addr = dst_ip_addr
        self._dst_port = dst_port

        self._command = command
        self._args_list = args_list

    def to_string(self):
        json_data = json.dumps(
            {
                MSG_TYPE_KEY: CLIENT_REQUEST_MESSAGE_TYPE,
                SRC_IP_ADDR_KEY: self._src_ip_addr,
                SRC_PORT_KEY: self._src_port,
                COMMAND_KEY: self._command,
                ARGS_LIST_KEY: self._args_list
           }
        )

        return "{0} {1}".format(CLIENT_REQUEST_MESSAGE_TYPE, json_data)

    @staticmethod
    def from_message_string(message):
        json_data = json.load(message)

        dst_ip_addr = json_data[DST_IP_ADDR_KEY]
        dst_port = json_data[DST_PORT_KEY]
        command = json_data[COMMAND_KEY]
        args_list = json_data[ARGS_LIST_KEY]

        return ClientRequestMessage(dst_ip_addr, dst_port, command, args_list)

    @staticmethod
    def is_client_message(message):
        json_data = json.load(message)

        msg_type = json_data[MSG_TYPE_KEY]

        return msg_type == CLIENT_REQUEST_MESSAGE_TYPE

