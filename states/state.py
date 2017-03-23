import random
import time

from messages.base_raft import BaseRaftMessage
from messages.response import ResponseMessage
from messages.client_request import ClientRequestMessage
from messages.append_entries import AppendEntriesMessage
from messages.request_vote import RequestVoteMessage
from messages.request_vote import RequestVoteResponseMessage


class State(object):
    def set_server(self, server):
        self._server = server

    def on_message(self, message):
        """This method is called when a message is received,
        and calls one of the other corrosponding methods
        that this state reacts to.

        """
        if ClientRequestMessage.is_client_message(message):
            message = ClientRequestMessage.from_message_string(message)
            print "NOT SURE WHAT TO DO NOW..."

        if (message.term > self._server._currentTerm):
            self._server._currentTerm = message.term
        # Is the messages.term < ours? If so we need to tell
        #   them this so they don't get left behind.
        elif (message.term < self._server._currentTerm):
            self._send_response_message(message, yes=False)
            return self, None

        if AppendEntriesMessage.is_append_entries_message():
            message = AppendEntriesMessage.from_message_string(message)

            return self.on_append_entries(message)

        elif RequestVoteMessage.is_request_vote_message(message):
            message = RequestVoteMessage.from_message_string(message)

            return self.on_vote_request(message)

        elif RequestVoteResponseMessage.is_request_vote_response_message(message):
            message = RequestVoteResponseMessage.from_message_string(message)

            return self.on_vote_received(message)

        elif ResponseMessage.is_response_message(message):
            message = ResponseMessage.from_message_string(message)

            return self.on_response_received(message)

    def on_leader_timeout(self, message):
        """This is called when the leader timeout is reached."""

    def on_vote_request(self, message):
        """This is called when there is a vote request."""

    def on_vote_received(self, message):
        """This is called when this node recieves a vote."""

    def on_append_entries(self, message):
        """This is called when there is a request to
        append an entry to the log.

        """

    def on_response_received(self, message):
        """This is called when a response is sent back to the Leader"""

    def on_client_command(self, message):
        """This is called when there is a client request."""

    def _nextTimeout(self):
        self._currentTime = time.time()
        return self._currentTime + random.randrange(self._timeout,
                                                    2 * self._timeout)

    def _send_response_message(self, msg, yes=True):
        response = ResponseMessage(self._server._name, msg.sender, msg.term, {
            "response": yes,
            "currentTerm": self._server._currentTerm,
        })
        self._server.send_message_response(response)
