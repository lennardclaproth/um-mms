from typing import Any, Callable, List, Tuple


class QueryBuilder():
    def __init__(self):
        self.conditions: List[Callable[[Any], bool]] = []

    def reset(self):
        self.conditions = []

    def where(self, field: str):
        self.current_field = field
        return self

    def search(self, fields: List[str], value: str):
        def condition(record):
            return any(value.lower() in str(getattr(record, field, "")).lower() for field in fields)
        self.conditions.append(condition)
        return self

    def like(self, value: str):
        def condition(record):
            field_value = getattr(record, self.current_field, "")
            return value.lower() in field_value.lower()
        self.conditions.append(condition)
        return self

    def equals(self, value: Any):
        def condition(record):
            return getattr(record, self.current_field, None) == value
        self.conditions.append(condition)
        return self

    def in_(self, values: List[Any]):
        def condition(record):
            return getattr(record, self.current_field, None) in values
        self.conditions.append(condition)
        return self

    def build(self) -> Callable[[Any], bool]:
        def combined_condition(record):
            return all(condition(record) for condition in self.conditions)
        return combined_condition
