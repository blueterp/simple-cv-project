from collections import deque


class StreamBuffer:
    def __init__(self, max_length):
        self.queue = deque()
        self.max_length = max_length

    def __iter__(self):
        yield from list(self.queue)

    def enque(self, item):
        if len(self.queue) > self.max_length:
            self.queue.popleft()
        self.queue.append(item)

    def clear_queue(self):
        self.queue = deque()

    def dequeue(self):
        if len(self.queue) > 0:
            self.queue.popleft()
