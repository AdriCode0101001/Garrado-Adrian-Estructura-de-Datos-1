"""Ejercicio 1 - Unidad 3: Lista Simple.

ListaSimple con insertar al inicio y al final, buscar, eliminar
por valor, y recorrido/impresion. Control de lista vacia.
"""

from typing import Any, Optional


class _Nodo:
    def __init__(self, dato: Any):
        self.dato = dato
        self.siguiente: Optional["_Nodo"] = None


class ListaSimple:
    def __init__(self):
        self._cabeza: Optional[_Nodo] = None
        self._tamanio = 0

    def insertar_inicio(self, dato: Any) -> None:
        """O(1)."""
        nuevo = _Nodo(dato)
        nuevo.siguiente = self._cabeza
        self._cabeza = nuevo
        self._tamanio += 1

    def insertar_final(self, dato: Any) -> None:
        """O(n)."""
        nuevo = _Nodo(dato)
        if self._cabeza is None:
            self._cabeza = nuevo
        else:
            actual = self._cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self._tamanio += 1

    def buscar(self, dato: Any) -> bool:
        """O(n)."""
        actual = self._cabeza
        while actual is not None:
            if actual.dato == dato:
                return True
            actual = actual.siguiente
        return False

    def eliminar(self, dato: Any) -> bool:
        """Elimina la primera aparicion del dato. O(n)."""
        if self._cabeza is None:
            return False
        if self._cabeza.dato == dato:
            self._cabeza = self._cabeza.siguiente
            self._tamanio -= 1
            return True
        anterior = self._cabeza
        actual = self._cabeza.siguiente
        while actual is not None:
            if actual.dato == dato:
                anterior.siguiente = actual.siguiente
                self._tamanio -= 1
                return True
            anterior = actual
            actual = actual.siguiente
        return False

    def esta_vacia(self) -> bool:
        return self._cabeza is None

    def __str__(self) -> str:
        if self._cabeza is None:
            return "(lista vacia)"
        partes = []
        actual = self._cabeza
        while actual is not None:
            partes.append(str(actual.dato))
            actual = actual.siguiente
        return " -> ".join(partes) + " -> None"

    def __len__(self) -> int:
        return self._tamanio


def main():
    lista = ListaSimple()
    print(f"Lista vacia: {lista}")
    print(f"esta_vacia(): {lista.esta_vacia()}")

    lista.insertar_final(10)
    lista.insertar_final(20)
    lista.insertar_inicio(5)
    print(f"\nDespues de insertar: {lista}")
    print(f"tamanio: {len(lista)}")

    print(f"\nbuscar(20): {lista.buscar(20)}")
    print(f"buscar(99): {lista.buscar(99)}")

    lista.eliminar(20)
    print(f"\nDespues de eliminar 20: {lista}")

    # probando eliminar algo que no existe
    print(f"eliminar(99): {lista.eliminar(99)} (no deberia encontrarlo)")


if __name__ == "__main__":
    main()
