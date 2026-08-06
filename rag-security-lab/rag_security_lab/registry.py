from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar


T = TypeVar("T")


class Registry:
    def __init__(self, category: str) -> None:
        self.category = category
        self._items: dict[str, type[Any]] = {}

    def register(self, name: str) -> Callable[[type[T]], type[T]]:
        normalized = name.strip().lower().replace("-", "_")

        def decorator(component: type[T]) -> type[T]:
            if normalized in self._items:
                raise ValueError(f"Duplicate {self.category} component: {normalized}")
            self._items[normalized] = component
            return component

        return decorator

    def create(self, name: str, config: dict[str, Any]) -> Any:
        normalized = name.strip().lower().replace("-", "_")
        if normalized not in self._items:
            choices = ", ".join(sorted(self._items)) or "<none>"
            raise ValueError(f"Unknown {self.category} '{name}'. Available: {choices}")
        return self._items[normalized](config)

    def names(self) -> list[str]:
        return sorted(self._items)


DATASETS = Registry("dataset")
ATTACKS = Registry("attack")
RETRIEVERS = Registry("retriever")
GENERATORS = Registry("generator")

