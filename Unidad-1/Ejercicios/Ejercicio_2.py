"""Ejercicio 2 - Unidad 1: Estatico vs dinamico.

Implementa ArrayEstatico (tamano fijo, con control de desbordamiento)
y ListaDinamica (enlazada, con insercion al inicio y al final), y
compara sus complejidades mediante mediciones de tiempo reales.
"""

import sys
import time
from typing import Any, Optional


class ArrayEstatico:
    """Array de tamano fijo definido al crearse.

    Complejidades:
        agregar (al final):  O(1) amortizado
        obtener por indice:  O(1)
        eliminar por indice: O(n) (debe desplazar elementos)
    """

    def __init__(self, capacidad: int) -> None:
        """Inicializa un array vacio con capacidad fija.

        Args:
            capacidad: Cantidad maxima de elementos que puede contener.
        """
        self._datos: list[Any] = [None] * capacidad
        self._capacidad = capacidad
        self._tamanio = 0

    def agregar(self, dato: Any) -> None:
        """Agrega un elemento al final del array. O(1).

        Args:
            dato: El valor a agregar.

        Raises:
            OverflowError: Si el array ya alcanzo su capacidad maxima.
        """
        if self._tamanio >= self._capacidad:
            raise OverflowError(
                f"Array lleno (capacidad maxima: {self._capacidad})"
            )
        self._datos[self._tamanio] = dato
        self._tamanio += 1

    def obtener(self, indice: int) -> Any:
        """Retorna el elemento en la posicion dada. O(1).

        Args:
            indice: Posicion a consultar (0-based).

        Returns:
            El valor en esa posicion.

        Raises:
            IndexError: Si el indice esta fuera de rango.
        """
        if indice < 0 or indice >= self._tamanio:
            raise IndexError(
                f"Indice {indice} fuera de rango [0, {self._tamanio - 1}]"
            )
        return self._datos[indice]

    def eliminar(self, indice: int) -> Any:
        """Elimina el elemento en la posicion dada, desplazando los
        elementos siguientes una posicion hacia atras. O(n).

        Args:
            indice: Posicion a eliminar (0-based).

        Returns:
            El valor eliminado.

        Raises:
            IndexError: Si el indice esta fuera de rango.
        """
        if indice < 0 or indice >= self._tamanio:
            raise IndexError(
                f"Indice {indice} fuera de rango [0, {self._tamanio - 1}]"
            )
        dato = self._datos[indice]
        for i in range(indice, self._tamanio - 1):
            self._datos[i] = self._datos[i + 1]
        self._datos[self._tamanio - 1] = None
        self._tamanio -= 1
        return dato

    def esta_lleno(self) -> bool:
        """Retorna True si el array alcanzo su capacidad maxima."""
        return self._tamanio >= self._capacidad

    def memoria_aproximada(self) -> int:
        """Devuelve un estimado de bytes usados por el almacenamiento."""
        return sys.getsizeof(self._datos)

    def __len__(self) -> int:
        """Retorna la cantidad de elementos actualmente almacenados."""
        return self._tamanio


class _NodoLista:
    """Nodo interno de ListaDinamica."""

    def __init__(self, dato: Any) -> None:
        """Inicializa el nodo con un dato y sin enlace siguiente.

        Args:
            dato: El valor que almacena este nodo.
        """
        self.dato = dato
        self.siguiente: Optional["_NodoLista"] = None


class ListaDinamica:
    """Lista enlazada que crece y se reduce en tiempo de ejecucion.

    Complejidades:
        insertar al inicio:  O(1)
        insertar al final:   O(n) (se recorre hasta el ultimo nodo)
        obtener por indice:  O(n)
        eliminar por indice: O(n)
    """

    def __init__(self) -> None:
        """Inicializa la lista vacia."""
        self._cabeza: Optional[_NodoLista] = None
        self._tamanio = 0

    def insertar_al_inicio(self, dato: Any) -> None:
        """Inserta un elemento al inicio de la lista. O(1).

        Args:
            dato: El valor a insertar.
        """
        nuevo_nodo = _NodoLista(dato)
        nuevo_nodo.siguiente = self._cabeza
        self._cabeza = nuevo_nodo
        self._tamanio += 1

    def insertar_al_final(self, dato: Any) -> None:
        """Inserta un elemento al final de la lista. O(n).

        Args:
            dato: El valor a insertar.
        """
        nuevo_nodo = _NodoLista(dato)
        if self._cabeza is None:
            self._cabeza = nuevo_nodo
        else:
            actual = self._cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self._tamanio += 1

    def obtener(self, indice: int) -> Any:
        """Retorna el elemento en la posicion dada. O(n).

        Args:
            indice: Posicion a consultar (0-based).

        Returns:
            El valor en esa posicion.

        Raises:
            IndexError: Si el indice esta fuera de rango.
        """
        if indice < 0 or indice >= self._tamanio:
            raise IndexError(
                f"Indice {indice} fuera de rango [0, {self._tamanio - 1}]"
            )
        actual = self._cabeza
        for _ in range(indice):
            actual = actual.siguiente
        return actual.dato

    def eliminar(self, indice: int) -> Any:
        """Elimina el elemento en la posicion dada. O(n).

        Args:
            indice: Posicion a eliminar (0-based).

        Returns:
            El valor eliminado.

        Raises:
            IndexError: Si el indice esta fuera de rango.
        """
        if indice < 0 or indice >= self._tamanio:
            raise IndexError(
                f"Indice {indice} fuera de rango [0, {self._tamanio - 1}]"
            )
        if indice == 0:
            dato = self._cabeza.dato
            self._cabeza = self._cabeza.siguiente
        else:
            anterior = self._cabeza
            for _ in range(indice - 1):
                anterior = anterior.siguiente
            dato = anterior.siguiente.dato
            anterior.siguiente = anterior.siguiente.siguiente
        self._tamanio -= 1
        return dato

    def memoria_aproximada(self) -> int:
        """Devuelve un estimado de bytes usados por los nodos de la lista."""
        total = 0
        actual = self._cabeza
        while actual is not None:
            total += sys.getsizeof(actual)
            total += sys.getsizeof(actual.dato)
            actual = actual.siguiente
        return total

    def __len__(self) -> int:
        """Retorna la cantidad de elementos en la lista."""
        return self._tamanio


def comparar_insercion(cantidad: int) -> None:
    """Mide y compara el tiempo de insercion de N elementos en un
    ArrayEstatico (al final) vs una ListaDinamica (al inicio y al final).

    Args:
        cantidad: Cantidad de elementos a insertar en cada prueba.
    """
    array = ArrayEstatico(cantidad)
    inicio = time.perf_counter()
    for i in range(cantidad):
        array.agregar(i)
    tiempo_array = time.perf_counter() - inicio

    lista_inicio = ListaDinamica()
    inicio = time.perf_counter()
    for i in range(cantidad):
        lista_inicio.insertar_al_inicio(i)
    tiempo_lista_inicio = time.perf_counter() - inicio

    lista_final = ListaDinamica()
    inicio = time.perf_counter()
    for i in range(cantidad):
        lista_final.insertar_al_final(i)
    tiempo_lista_final = time.perf_counter() - inicio

    print(f"Insertar {cantidad} elementos:")
    print(f"  ArrayEstatico.agregar (O(1)):            {tiempo_array:.5f}s")
    print(f"  ListaDinamica.insertar_al_inicio (O(1)): {tiempo_lista_inicio:.5f}s")
    print(f"  ListaDinamica.insertar_al_final (O(n)):  {tiempo_lista_final:.5f}s")


def main() -> None:
    """Demuestra ambas estructuras y compara sus tiempos de insercion."""
    print("=== Demo: ArrayEstatico vs ListaDinamica ===\n")

    array = ArrayEstatico(3)
    array.agregar("a")
    array.agregar("b")
    array.agregar("c")
    print(f"ArrayEstatico lleno: {array.esta_lleno()}")
    try:
        array.agregar("d")
    except OverflowError as error:
        print(f"Error capturado (desbordamiento): {error}")

    array.eliminar(0)
    print(f"Despues de eliminar indice 0: {[array.obtener(i) for i in range(len(array))]}")

    print()
    lista = ListaDinamica()
    lista.insertar_al_final(1)
    lista.insertar_al_final(2)
    lista.insertar_al_inicio(0)
    print(f"ListaDinamica: {[lista.obtener(i) for i in range(len(lista))]}")

    print()
    comparar_insercion(20_000)


if __name__ == "__main__":
    main()