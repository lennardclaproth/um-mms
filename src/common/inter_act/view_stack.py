from common.inter_act.page import PageInterface


class ViewStack:

    def __init__(self, max_size):
        self.value = []
        self.max_size = max_size

    def get_value(self, shift=0):
        index = len(self.value) - 1 + shift
        if index < 0 or index >= len(self.value):
            raise IndexError("Index out of range")
        return self.value[index]

    def add_value(self, new_value: PageInterface):
        if len(self.value) >= self.max_size:
            self.value.pop(0)
        self.value.append(new_value)

    def pop_value(self):
        if not self.value:
            raise IndexError("Pop from an empty stack")
        return self.value.pop()

    def is_empty(self):
        return len(self.value) == 0

    def size(self):
        return len(self.value)
