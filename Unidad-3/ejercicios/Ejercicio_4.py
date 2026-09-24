"""Ejercicio 4 - Unidad 3: Bicola (Deque).

Bicola con operaciones en ambos extremos, y demostracion de como
simular una Pila (usando solo un extremo) y una Cola (usando los
2 extremos de forma FIFO).
"""

from collections import deque
from typing import Any


class BicolaVaciaError(Exception):
    """Se lanza al intentar eliminar de una bicola vacia."""


class Bicola:
    """Usa collections.deque internamente - ya viene optimizada para
    insertar/eliminar O(1) en ambos extremos.
    """

    def __init__(self):
        self._datos: deque = deque()

    def insertar_frente(self, dato: Any) -> None:
        self._datos.appendleft(dato)

    def insertar_fondo(self, dato: Any) -> None:
        self._datos.append(dato)

    def eliminar_frente(self) -> Any:
        if self.esta_vacia():
            raise BicolaVaciaError("Bicola vacia")
        return self._datos.popleft()

    def eliminar_fondo(self) -> Any:
        if self.esta_vacia():
            raise BicolaVaciaError("Bicola vacia")
        return self._datos.pop()

    def esta_vacia(self) -> bool:
        return len(self._datos) == 0

    def __len__(self) -> int:
        return len(self._datos)

    def __str__(self) -> str:
        return " <-> ".join(str(x) for x in self._datos) if self._datos else "(vacia)"


def simular_pila_con_bicola():
    """Una pila LIFO: siempre insertar y eliminar por el MISMO extremo."""
    print("--- Simulando una Pila (LIFO) con Bicola ---")
    b = Bicola()
    b.insertar_fondo(1)
    b.insertar_fondo(2)
    b.insertar_fondo(3)
    print(f"Bicola: {b}")
    print(f"eliminar_fondo(): {b.eliminar_fondo()}  (deberia ser 3, el ultimo)")
    print(f"eliminar_fondo(): {b.eliminar_fondo()}  (deberia ser 2)")


def simular_cola_con_bicola():
    """Una cola FIFO: insertar por un extremo, eliminar por el otro."""
    print("\n--- Simulando una Cola (FIFO) con Bicola ---")
    b = Bicola()
    b.insertar_fondo(1)
    b.insertar_fondo(2)
    b.insertar_fondo(3)
    print(f"Bicola: {b}")
    print(f"eliminar_frente(): {b.eliminar_frente()}  (deberia ser 1, el primero)")
    print(f"eliminar_frente(): {b.eliminar_frente()}  (deberia ser 2)")


def main():
    simular_pila_con_bicola()
    simular_cola_con_bicola()

    print("\n--- Probando error en bicola vacia ---")
    vacia = Bicola()
    try:
        vacia.eliminar_frente()
    except BicolaVaciaError as error:
        print(f"error capturado: {error}")


if __name__ == "__main__":
    main()
