"""Ejercicio 3 - Unidad 3: Cola circular.

ColaCircular sobre un arreglo de tamano fijo, usando indices
circulares para reutilizar los espacios que quedan libres al
desencolar (en vez de desperdiciarlos como una cola lineal).
"""

from typing import Any


class ColaLlenaError(Exception):
    """Se lanza al intentar encolar en una cola circular ya llena."""


class ColaVaciaError(Exception):
    """Se lanza al intentar desencolar de una cola vacia."""


class ColaCircular:
    def __init__(self, capacidad: int):
        self._datos: list[Any] = [None] * capacidad
        self._capacidad = capacidad
        self._frente = 0
        self._fondo = 0
        self._cantidad = 0

    def encolar(self, dato: Any) -> None:
        if self._cantidad >= self._capacidad:
            raise ColaLlenaError(f"Cola llena (capacidad {self._capacidad})")
        self._datos[self._fondo] = dato
        # el modulo es lo que hace que el indice "de la vuelta" al llegar al final
        self._fondo = (self._fondo + 1) % self._capacidad
        self._cantidad += 1

    def desencolar(self) -> Any:
        if self.esta_vacia():
            raise ColaVaciaError("Cola vacia")
        dato = self._datos[self._frente]
        self._frente = (self._frente + 1) % self._capacidad
        self._cantidad -= 1
        return dato

    def frente(self) -> Any:
        if self.esta_vacia():
            raise ColaVaciaError("Cola vacia")
        return self._datos[self._frente]

    def esta_vacia(self) -> bool:
        return self._cantidad == 0

    def __len__(self) -> int:
        return self._cantidad

    def __str__(self) -> str:
        if self.esta_vacia():
            return "(cola vacia)"
        elementos = []
        indice = self._frente
        for _ in range(self._cantidad):
            elementos.append(str(self._datos[indice]))
            indice = (indice + 1) % self._capacidad
        return " <- ".join(elementos)


def demostrar_reutilizacion_circular():
    """Prueba especifica: llena la cola, saca algunos, y vuelve a
    encolar - demostrando que reutiliza los espacios liberados.
    """
    print("--- Demostrando reutilizacion de espacios (indices circulares) ---")
    cola = ColaCircular(5)

    cola.encolar(10)
    cola.encolar(20)
    cola.encolar(30)
    print(f"Encolados 10,20,30: {cola} (frente={cola._frente}, fondo={cola._fondo})")

    print(f"desencolar(): {cola.desencolar()}")
    print(f"desencolar(): {cola.desencolar()}")
    print(f"Cola ahora: {cola} (frente={cola._frente}, fondo={cola._fondo})")

    # en una cola LINEAL (no circular) esto ya no cabria sin desperdiciar espacio
    cola.encolar(40)
    cola.encolar(50)
    cola.encolar(60)
    print(f"Encolados 40,50,60 (fondo dio la vuelta): {cola}")
    print(f"(frente={cola._frente}, fondo={cola._fondo}) - fondo volvio a 0/1, no crecio el array")

    try:
        cola.encolar(70)
    except ColaLlenaError as error:
        print(f"error capturado al intentar encolar de mas: {error}")


def main():
    demostrar_reutilizacion_circular()


if __name__ == "__main__":
    main()
