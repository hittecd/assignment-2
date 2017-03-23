from base_raft import BaseRaftMessage


class ResponseMessage(BaseRaftMessage):
    def __init__(self, sender, receiver, term, data):
        BaseRaftMessage.__init__(self, sender, receiver, term, data)
