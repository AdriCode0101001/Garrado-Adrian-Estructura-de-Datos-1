"""Ejercicio 1 - Unidad 1 ADT de Pila.

Define la interfaz abstracta ADTPila y provee 2 implementaciones
distintas (PilaArray y PilaLista)
"""

from abc import ABC, abstractmethod
from typing import Any, Optional


class PilaVaciaError(Exception):
    """Se lanza al intentar operar sobre una pila vacia."""


class ADTPila(ABC):
    """Interfaz abstracta para el Tipo de Dato Abstracto Pila (LIFO).

    Define QUE operaciones debe tener una pila, sin importar COMO
    esten implementadas por dentro (con un array o con nodos).
    """

    @abstractmethod
    def apilar(self, dato: Any) -> None:
        """Agrega un elemento al tope de la pila."""

    @abstractmethod
    def desapilar(self) -> Any:
        """Elimina y retorna el elemento en el tope de la pila."""

    @abstractmethod
    def tope(self) -> Any:
        """Retorna el elemento en el tope sin eliminarlo."""

    @abstractmethod
    def esta_vacia(self) -> bool:
        """Retorna True si la pila no tiene elementos."""


class PilaArray(ADTPila):
    """Implementacion de ADTPila usando una lista de Python como
    almacenamiento interno (arreglo dinamico).
    """

    def __init__(self) -> None:
        """Inicializa la pila vacia."""
        self._datos: list[Any] = []

    def apilar(self, dato: Any) -> None:
        """Agrega un elemento al final de la lista interna (el tope).

        Args:
            dato: El valor a agregar.
        """
        self._datos.append(dato)

    def desapilar(self) -> Any:
        """Elimina y retorna el ultimo elemento de la lista interna.

        Returns:
            El valor que estaba en el tope.

        Raises:
            PilaVaciaError: Si la pila esta vacia.
        """
        if self.esta_vacia():
            raise PilaVaciaError("Pila vacia")
        return self._datos.pop()

    def tope(self) -> Any:
        """Retorna el ultimo elemento de la lista interna sin sacarlo.

        Returns:
            El valor que esta en el tope.

        Raises:
            PilaVaciaError: Si la pila esta vacia.
        """
        if self.esta_vacia():
            raise PilaVaciaError("Pila vacia")
        return self._datos[-1]

    def esta_vacia(self) -> bool:
        """Retorna True si la lista interna no tiene elementos."""
        return len(self._datos) == 0


class _Nodo:
    """Nodo interno usado por PilaLista. No debe usarse desde afuera
    de este modulo (de ahi el guion bajo en el nombre).
    """

    def __init__(self, dato: Any, siguiente: Optional["_Nodo"] = None) -> None:
        """Inicializa el nodo con su dato y el enlace al siguiente.

        Args:
            dato: El valor que almacena este nodo.
            siguiente: El nodo que estaba antes en la pila (o None).
        """
        self.dato = dato
        self.siguiente = siguiente


class PilaLista(ADTPila):
    """Implementacion de ADTPila usando nodos enlazados dinamicamente
    en el Heap, en vez de un arreglo.
    """

    def __init__(self) -> None:
        """Inicializa la pila vacia (sin ningun nodo tope)."""
        self._tope: Optional[_Nodo] = None

    def apilar(self, dato: Any) -> None:
        """Crea un nuevo nodo que apunta al tope anterior, y lo
        convierte en el nuevo tope. O(1).

        Args:
            dato: El valor a agregar.
        """
        self._tope = _Nodo(dato, self._tope)

    def desapilar(self) -> Any:
        """Retorna el dato del nodo tope y avanza el tope al
        siguiente nodo de la cadena. O(1).

        Returns:
            El valor que estaba en el nodo tope.

        Raises:
            PilaVaciaError: Si la pila esta vacia.
        """
        if self.esta_vacia():
            raise PilaVaciaError("Pila vacia")
        dato = self._tope.dato
        self._tope = self._tope.siguiente
        return dato

    def tope(self) -> Any:
        """Retorna el dato del nodo tope sin modificar la pila.

        Returns:
            El valor que esta en el nodo tope.

        Raises:
            PilaVaciaError: Si la pila esta vacia.
        """
        if self.esta_vacia():
            raise PilaVaciaError("Pila vacia")
        return self._tope.dato

    def esta_vacia(self) -> bool:
        """Retorna True si no hay ningun nodo tope."""
        return self._tope is None


def usar_pila(pila: ADTPila) -> list[Any]:
    """Funcion cliente que opera sobre cualquier ADTPila, sin conocer
    si es una PilaArray o una PilaLista por dentro. Demuestra que el
    codigo cliente no cambia sin importar la implementacion elegida.

    Args:
        pila: Cualquier objeto que implemente ADTPila.

    Returns:
        Lista con los 3 elementos desapilados, en orden LIFO.
    """
    for valor in [1, 2, 3]:
        pila.apilar(valor)
    return [pila.desapilar(), pila.desapilar(), pila.desapilar()]


def main() -> None:
    """Demuestra que ambas implementaciones dan el mismo resultado
    al ser usadas por la misma funcion cliente (usar_pila).
    """
    print("=== Demo: ADT Pila (2 implementaciones) ===\n")

    print(f"PilaArray -> {usar_pila(PilaArray())}")
    print(f"PilaLista -> {usar_pila(PilaLista())}")

    print("\n--- Probando manejo de errores ---")
    pila_vacia = PilaArray()
    try:
        pila_vacia.desapilar()
    except PilaVaciaError as error:
        print(f"Error capturado correctamente: {error}")


if __name__ == "__main__":
    main()