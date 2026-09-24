"""Ejercicio 2 - Unidad 3: Pila estatica y dinamica.

PilaEstatica (capacidad fija) y PilaDinamica (nodos enlazados),
comparando su comportamiento ante desbordamiento y uso intensivo.
"""

import time
from typing import Any, Optional


class PilaLlenaError(Exception):
    """Se lanza al intentar apilar en una pila estatica ya llena."""


class PilaVaciaError(Exception):
    """Se lanza al intentar desapilar de una pila vacia."""


class PilaEstatica:
    """Pila con capacidad fija, implementada sobre una lista."""

    def __init__(self, capacidad: int):
        self._datos: list[Any] = [None] * capacidad
        self._capacidad = capacidad
        self._tope = -1  # -1 significa vacia

    def apilar(self, dato: Any) -> None:
        if self._tope + 1 >= self._capacidad:
            raise PilaLlenaError(f"Pila llena (capacidad {self._capacidad})")
        self._tope += 1
        self._datos[self._tope] = dato

    def desapilar(self) -> Any:
        if self.esta_vacia():
            raise PilaVaciaError("Pila vacia")
        dato = self._datos[self._tope]
        self._tope -= 1
        return dato

    def tope(self) -> Any:
        if self.esta_vacia():
            raise PilaVaciaError("Pila vacia")
        return self._datos[self._tope]

    def esta_vacia(self) -> bool:
        return self._tope == -1


class _Nodo:
    def __init__(self, dato: Any, siguiente: Optional["_Nodo"] = None):
        self.dato = dato
        self.siguiente = siguiente


class PilaDinamica:
    """Pila sin limite de tamano, implementada con nodos enlazados."""

    def __init__(self):
        self._tope_nodo: Optional[_Nodo] = None

    def apilar(self, dato: Any) -> None:
        # nunca se llena - crece mientras haya memoria disponible
        self._tope_nodo = _Nodo(dato, self._tope_nodo)

    def desapilar(self) -> Any:
        if self.esta_vacia():
            raise PilaVaciaError("Pila vacia")
        dato = self._tope_nodo.dato
        self._tope_nodo = self._tope_nodo.siguiente
        return dato

    def tope(self) -> Any:
        if self.esta_vacia():
            raise PilaVaciaError("Pila vacia")
        return self._tope_nodo.dato

    def esta_vacia(self) -> bool:
        return self._tope_nodo is None


def comparar_desbordamiento():
    print("--- Comportamiento ante desbordamiento ---")
    estatica = PilaEstatica(3)
    for i in range(3):
        estatica.apilar(i)
    print("PilaEstatica llena con 3 elementos, intentando apilar un 4to...")
    try:
        estatica.apilar(99)
    except PilaLlenaError as error:
        print(f"  error capturado: {error}")

    dinamica = PilaDinamica()
    for i in range(1000):
        dinamica.apilar(i)
    print(f"PilaDinamica con 1000 elementos, sin error (no tiene limite fijo)")


def comparar_uso_intensivo(cantidad: int):
    print(f"\n--- Uso intensivo: {cantidad} apilar/desapilar ---")

    estatica = PilaEstatica(cantidad)
    inicio = time.perf_counter()
    for i in range(cantidad):
        estatica.apilar(i)
    for _ in range(cantidad):
        estatica.desapilar()
    tiempo_estatica = time.perf_counter() - inicio

    dinamica = PilaDinamica()
    inicio = time.perf_counter()
    for i in range(cantidad):
        dinamica.apilar(i)
    for _ in range(cantidad):
        dinamica.desapilar()
    tiempo_dinamica = time.perf_counter() - inicio

    print(f"  PilaEstatica:  {tiempo_estatica:.5f}s")
    print(f"  PilaDinamica:  {tiempo_dinamica:.5f}s")
    print("  (ambas son O(1) por operacion, la diferencia es por overhead")
    print("   de crear objetos _Nodo vs usar un arreglo precreado)")


def main():
    comparar_desbordamiento()
    comparar_uso_intensivo(50_000)


if __name__ == "__main__":
    main()
