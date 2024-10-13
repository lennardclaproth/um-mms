class Scope:
    def __init__(self):
        self._scoped_instances = {}

    def get_or_create(self, key, factory):
        if key not in self._scoped_instances:
            self._scoped_instances[key] = factory()
        return self._scoped_instances[key]

    def clear(self):
        self._scoped_instances.clear()
