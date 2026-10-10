from abc import ABC, abstractmethod
from typing import Any


class EstructuraLineal(ABC):
    """Contrato que deben cumplir todas las estructuras lineales."""

    @abstractmethod
    def insertar(self, dato: Any) -> None:
        """Agrega un dato a la estructura."""

    @abstractmethod
    def eliminar(self) -> Any:
        """Quita y devuelve un dato de la estructura."""

    @abstractmethod
    def esta_vacia(self) -> bool:
        """Indica si la estructura no tiene elementos."""

    @abstractmethod
    def __len__(self) -> int:
        """Devuelve la cantidad de elementos."""
