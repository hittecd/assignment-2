# from client_request import ClientRequestMessage
# from request_vote import RequestVoteMessage
# from request_vote import RequestVoteResponseMessage
# from response import ResponseMessage
# from append_entries import AppendEntriesMessage


MSG_TYPE_KEY = "msg_type"


class BaseMessage(object):

    # @staticmethod
    # def from_message_string(message):
    #
    #     if ClientRequestMessage.is_client_message(message):
    #         return ClientRequestMessage.from_message_string(message)
    #
    #     elif RequestVoteMessage.is_request_vote_message(message):
    #         return RequestVoteMessage.from_message_string(message)
    #
    #     elif RequestVoteResponseMessage.is_request_vote_response_message(message):
    #         return RequestVoteResponseMessage.from_message_string(message)
    #
    #     elif ResponseMessage.is_response_message(message):
    #         return ResponseMessage.from_message_string(message)
    #
    #     elif AppendEntriesMessage.is_append_entries_message(message):
    #         return AppendEntriesMessage.from_message_string(message)

    pass