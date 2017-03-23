import json

from base_raft import BaseRaftMessage
from base import MSG_TYPE_KEY


APPEND_ENTRIES_MESSAGE_TYPE = "APPEND_ENTRIES_MESSAGE"

SENDER_KEY = "sender"
RECEIVER_KEY = "receiver"
TERM_KEY = "term"
DATA_KEY = "data"


class AppendEntriesMessage(BaseRaftMessage):
    def __init__(self, sender, receiver, term, data):
        BaseRaftMessage.__init__(self, sender, receiver, term, data)

    def to_string(self):
        json_data = json.dumps(
            {
                MSG_TYPE_KEY: APPEND_ENTRIES_MESSAGE_TYPE,
                SENDER_KEY: self._sender,
                RECEIVER_KEY: self._receiver,
                TERM_KEY: self._term,
                DATA_KEY: self._data
            }
        )

        return "{0} {1}".format(APPEND_ENTRIES_MESSAGE_TYPE, json_data)

    @staticmethod
    def from_message_string(message):
        json_data = json.load(message)

        sender = json_data[SENDER_KEY]
        receiver = json_data[RECEIVER_KEY]
        term = json_data[TERM_KEY]
        data = json_data[DATA_KEY]

        return AppendEntriesMessage(sender, receiver, term, data)

    @staticmethod
    def is_client_message(message):
        json_data = json.load(message)

        msg_type = json_data[MSG_TYPE_KEY]

        return msg_type == APPEND_ENTRIES_MESSAGE_TYPE
