import inspect

from common.dependency_injection.lifetimes import Lifetime
from common.dependency_injection.scope import Scope


class Container:
    def __init__(self):

        self._services = {}
        self._singletons = {}
        self._scope = Scope()

    def register_as_singleton(self, interface, implementation):
        self._services[interface] = (implementation, Lifetime.SINGLETON)

    def register_as_transient(self, interface, implementation):
        self._services[interface] = (implementation, Lifetime.TRANSIENT)

    def register_as_scoped(self, interface, implementation):
        self._services[interface] = (implementation, Lifetime.SCOPED)

    def clear_scope(self):
        self._scope.clear()

    def resolve(self, interface):
        if interface in self._services:
            implementation, lifetime = self._services[interface]
            if lifetime == Lifetime.SINGLETON:
                if interface not in self._singletons:
                    self._singletons[interface] = self._create_instance(
                        implementation)
                return self._singletons[interface]
            elif lifetime == Lifetime.TRANSIENT:
                return self._create_instance(implementation)
            elif lifetime == Lifetime.SCOPED:
                if self._scope is None:
                    raise ValueError(
                        "No active scope. Create a scope before resolving scoped services.")
                return self._scope.get_or_create(interface, lambda: self._create_instance(implementation))
        raise ValueError(f"Service {interface} not found")

    def _create_instance(self, implementation):
        from common.dependency_injection.auto_wire import AutoWire
        if not inspect.isclass(implementation):
            raise ValueError(f"{implementation} is not a class.")

        if isinstance(implementation, AutoWire):
            return implementation()

        constructor = implementation.__init__
        if constructor is object.__init__:
            return implementation()

        params = inspect.signature(constructor).parameters
        dependencies = []
        for name, param in params.items():
            if name == 'self':
                continue
            dependency_type = param.annotation
            if dependency_type == inspect.Parameter.empty:
                raise ValueError(
                    f"Type hint missing for parameter '{name}' in {implementation}")
            dependencies.append(self.resolve(dependency_type))
        return implementation(*dependencies)
