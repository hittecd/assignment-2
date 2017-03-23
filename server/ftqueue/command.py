COMMAND_KEY_KEY = "command_key"
ARGS_LIST_KEY = "args_list"


class Command(object):
    def __init__(self, func, args_list):
        self._func = func
        self._args_list = args_list
