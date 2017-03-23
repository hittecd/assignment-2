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
        pass