Q_CREATE_COMMAND_STR = 'qcreate'
Q_ID_COMMAND_STR = 'qid'
Q_POP_COMMAND_STR = 'qpop'
Q_PUSH_COMMAND_STR = 'qpush'
Q_TOP_COMMAND_STR = 'qtop'
Q_SIZE_COMMAND_STR = 'qsize'


class FTQueue(object):
    def __init__(self):
        self._queue_count = -1
        self._queue_id_index = {}
        self._queue_table = {}

    def q_create(self, label):
        self._queue_count += 1
        self._queue_id_index[label] = self._queue_count
        self._queue_table[self._queue_count] = []

    def q_id(self, label):
        return self._queue_id_index[label]

    def q_push(self, queue_id, item):
        if queue_id in self._queue_table:
            queue = self._queue_table[queue_id]
            queue.append(item)

    def q_pop(self, queue_id):
        if queue_id not in self._queue_table:
            return

        queue = self._queue_table[queue_id]

        if len(queue) > 0:
            return list.pop()

    def q_top(self, queue_id):
        if queue_id not in self._queue_table:
            return

        queue = self._queue_table[queue_id]

        if len(queue) > 0:
            return list[len(list) - 1]

    def q_size(self, queue_id):
        if queue_id not in self._queue_table:
            return

        queue = self._queue_table[queue_id]

        return len(queue)

    def execute_command(self, command):
        func = command._func
        args_list = command._args_list

        if func == Q_CREATE_COMMAND_STR:
            label = args_list[0]

            return self.q_create(label)

        elif func == Q_ID_COMMAND_STR:
            label = args_list[0]

            return self.q_id(label)

        elif func == Q_PUSH_COMMAND_STR:
            queue_id = args_list[0]
            item = args_list[1]

            self.q_push(queue_id, item)

        elif func == Q_POP_COMMAND_STR:
            queue_id = args_list[0]

            return self.q_pop(queue_id)

        elif func == Q_TOP_COMMAND_STR:
            queue_id = args_list[0]

            return self.q_top(queue_id)

        elif func == Q_SIZE_COMMAND_STR:
            queue_id = args_list[0]

            return self.q_size(queue_id)