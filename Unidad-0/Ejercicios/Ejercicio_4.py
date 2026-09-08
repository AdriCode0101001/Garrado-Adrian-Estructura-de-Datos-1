"""Ejercicio 4 - Unidad 0: Interfaz con ABC.

Define una interfaz abstracta EstructuraLineal y la implementa con
2 clases concretas (Pila y Cola), demostrando polimorfismo mediante
una funcion que consume la interfaz sin conocer la implementacion
concreta de cada una.
"""

from abc import ABC, abstractmethod
from collections import deque
from typing import Any


class EstructuraVaciaError(Exception):
    """Se lanza al intentar eliminar de una estructura vacia."""


class EstructuraLineal(ABC):
    """Interfaz base para todas las estructuras lineales del curso:
    Pila, Cola, y otras que pudieran agregarse (Lista, Bicola, etc.).

    Cualquier clase que herede de esta interfaz esta obligada a
    implementar los 4 metodos abstractos definidos aqui.
    """

    @abstractmethod
    def insertar(self, dato: Any) -> None:
        """Inserta un elemento en la estructura."""

    @abstractmethod
    def eliminar(self) -> Any:
        """Elimina y retorna el elemento segun la politica de la
        estructura (LIFO para Pila, FIFO para Cola).
        """

    @abstractmethod
    def esta_vacia(self) -> bool:
        """Retorna True si la estructura no tiene elementos."""

    @abstractmethod
    def __len__(self) -> int:
        """Retorna la cantidad de elementos."""

    def __bool__(self) -> bool:
        """Permite usar la estructura en condiciones if."""
        return not self.esta_vacia()


class Pila(EstructuraLineal):
    """Estructura lineal LIFO (Last In, First Out)."""

    def __init__(self) -> None:
        """Inicializa la pila vacia."""
        self._datos: list[Any] = []

    def insertar(self, dato: Any) -> None:
        """Agrega un elemento al tope de la pila.

        Args:
            dato: El valor a agregar.
        """
        self._datos.append(dato)

    def eliminar(self) -> Any:
        """Elimina y retorna el elemento en el tope de la pila.

        Returns:
            El valor que estaba en el tope.

        Raises:
            EstructuraVaciaError: Si la pila esta vacia.
        """
        if self.esta_vacia():
            raise EstructuraVaciaError("Pila vacia")
        return self._datos.pop()

    def esta_vacia(self) -> bool:
        """Retorna True si la pila no tiene elementos."""
        return len(self._datos) == 0

    def __len__(self) -> int:
        """Retorna la cantidad de elementos en la pila."""
        return len(self._datos)


class Cola(EstructuraLineal):
    """Estructura lineal FIFO (First In, First Out)."""

    def __init__(self) -> None:
        """Inicializa la cola vacia."""
        self._datos: deque = deque()

    def insertar(self, dato: Any) -> None:
        """Agrega un elemento al final de la cola.

        Args:
            dato: El valor a agregar.
        """
        self._datos.append(dato)

    def eliminar(self) -> Any:
        """Elimina y retorna el elemento al frente de la cola.

        Returns:
            El valor que estaba al frente de la cola.

        Raises:
            EstructuraVaciaError: Si la cola esta vacia.
        """
        if self.esta_vacia():
            raise EstructuraVaciaError("Cola vacia")
        return self._datos.popleft()

    def esta_vacia(self) -> bool:
        """Retorna True si la cola no tiene elementos."""
        return len(self._datos) == 0

    def __len__(self) -> int:
        """Retorna la cantidad de elementos en la cola."""
        return len(self._datos)


def consumir(estructura: EstructuraLineal) -> list[Any]:
    """Vacia una estructura lineal cualquiera, sin conocer si es una
    Pila, una Cola, u otra implementacion de EstructuraLineal.

    Esto demuestra polimorfismo: la misma funcion sirve para
    cualquier clase que cumpla el "contrato" de EstructuraLineal.

    Args:
        estructura: Cualquier objeto que implemente EstructuraLineal.

    Returns:
        Lista con los elementos en el orden en que fueron eliminados.
    """
    salida = []
    while not estructura.esta_vacia():
        salida.append(estructura.eliminar())
    return salida


def main() -> None:
    """Demuestra el polimorfismo: la misma funcion consumir() trata
    a Pila y Cola de forma intercambiable.
    """
    print("=== Demo: Interfaz EstructuraLineal (ABC) ===\n")

    pila = Pila()
    cola = Cola()

    for valor in [10, 20, 30]:
        pila.insertar(valor)
        cola.insertar(valor)

    print(f"Pila antes de consumir -> len: {len(pila)}, bool: {bool(pila)}")
    print(f"Cola antes de consumir -> len: {len(cola)}, bool: {bool(cola)}")

    print(f"\nPila (LIFO): {consumir(pila)}")
    print(f"Cola (FIFO): {consumir(cola)}")

    print(f"\n¿Pila vacia despues? {pila.esta_vacia()} (bool: {bool(pila)})")

    try:
        pila.eliminar()
    except EstructuraVaciaError as error:
        print(f"Error capturado: {error}")


if __name__ == "__main__":
    main()