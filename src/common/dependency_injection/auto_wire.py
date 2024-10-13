from abc import ABCMeta
import inspect


class AutoWire(ABCMeta, type):
    from common.dependency_injection.container import Container
    container: Container = None

    def __call__(cls, *args, **kwargs):
        if AutoWire.container is None:
            raise ValueError(
                "Container instance must be set in AutoWireMeta before instantiating classes.")

        constructor = cls.__init__
        params = inspect.signature(constructor).parameters
        dependencies = {}
        for name, param in params.items():
            if name == 'self':
                continue
            if name not in kwargs:
                dependency_type = param.annotation
                if dependency_type == inspect.Parameter.empty:
                    raise ValueError(
                        f"Type hint missing for parameter '{name}' in {cls}")
                dependencies[name] = AutoWire.container.resolve(
                    dependency_type)

        kwargs.update(dependencies)

        instance = super(AutoWire, cls).__call__(*args, **kwargs)
        return instance
