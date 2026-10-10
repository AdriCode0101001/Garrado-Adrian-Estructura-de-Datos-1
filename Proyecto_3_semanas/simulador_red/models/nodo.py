from typing import Any, Optional


class Nodo:
    """Unidad básica de las listas enlazadas: guarda un dato y enlaces."""

    def __init__(self, dato: Any) -> None:
        self.dato = dato
        self.siguiente: Optional["Nodo"] = None
        self.anterior: Optional["Nodo"] = None
