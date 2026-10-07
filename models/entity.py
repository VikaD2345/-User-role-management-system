"""Базовый класс сущностей предметной области."""


class Entity:
    """Общая сущность с идентификатором и именем."""

    def __init__(self, entity_id: int, name: str) -> None:
        self.id = entity_id
        self.name = name

    def __str__(self) -> str:
        """Вернуть общее строковое представление сущности."""
        return f"{self.name} (id={self.id})"
