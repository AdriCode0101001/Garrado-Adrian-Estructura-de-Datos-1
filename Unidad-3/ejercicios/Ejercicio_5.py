"""Ejercicio 5 - Unidad 3: Tabla Hash.

TablaHash con resolucion de colisiones por encadenamiento: cada
posicion del arreglo guarda una lista de pares (clave, valor).
"""

from typing import Any


class TablaHash:
    def __init__(self, capacidad: int = 10):
        self._capacidad = capacidad
        # cada posicion arranca con una lista vacia (para encadenar)
        self._cubetas: list[list] = [[] for _ in range(capacidad)]
        self._cantidad = 0

    def _indice(self, clave: str) -> int:
        return hash(clave) % self._capacidad

    def insertar(self, clave: str, valor: Any) -> None:
        """Si la clave ya existe, actualiza su valor en vez de duplicar."""
        indice = self._indice(clave)
        cubeta = self._cubetas[indice]
        for i, (k, _) in enumerate(cubeta):
            if k == clave:
                cubeta[i] = (clave, valor)  # actualizacion de clave existente
                return
        cubeta.append((clave, valor))
        self._cantidad += 1

    def buscar(self, clave: str) -> Any:
        indice = self._indice(clave)
        for k, v in self._cubetas[indice]:
            if k == clave:
                return v
        raise KeyError(f"clave '{clave}' no encontrada")

    def eliminar(self, clave: str) -> bool:
        indice = self._indice(clave)
        cubeta = self._cubetas[indice]
        for i, (k, _) in enumerate(cubeta):
            if k == clave:
                cubeta.pop(i)
                self._cantidad -= 1
                return True
        return False

    def __len__(self) -> int:
        return self._cantidad

    def __contains__(self, clave: str) -> bool:
        indice = self._indice(clave)
        return any(k == clave for k, _ in self._cubetas[indice])


def demostrar_colision():
    """Fuerza colisiones usando una capacidad chica a proposito, para
    ver el encadenamiento en accion.
    """
    print("--- Demostrando colisiones (capacidad chica a proposito) ---")
    tabla = TablaHash(capacidad=3)
    claves = ["Bolivia", "Peru", "Chile", "Argentina", "Brasil"]
    for i, clave in enumerate(claves):
        tabla.insertar(clave, f"capital_{i}")

    for i, cubeta in enumerate(tabla._cubetas):
        print(f"  cubeta {i}: {cubeta}")
    print("(varias claves cayeron en la misma cubeta - eso es una colision,")
    print(" y se resolvio guardando varios pares en la misma lista)")


def main():
    tabla = TablaHash()
    tabla.insertar("Bolivia", "Sucre")
    tabla.insertar("Peru", "Lima")
    print(f"buscar('Bolivia'): {tabla.buscar('Bolivia')}")
    print(f"'Peru' in tabla: {'Peru' in tabla}")
    print(f"'Colombia' in tabla: {'Colombia' in tabla}")

    print("\n--- Actualizacion de clave existente ---")
    tabla.insertar("Bolivia", "La Paz (sede de gobierno)")
    print(f"buscar('Bolivia'): {tabla.buscar('Bolivia')}  (deberia ser el valor nuevo)")
    print(f"len(tabla): {len(tabla)}  (deberia seguir en 2, no duplico)")

    print("\n--- Eliminar ---")
    print(f"eliminar('Peru'): {tabla.eliminar('Peru')}")
    print(f"'Peru' in tabla: {'Peru' in tabla}")

    print("\n--- Buscar clave inexistente ---")
    try:
        tabla.buscar("Ecuador")
    except KeyError as error:
        print(f"error capturado: {error}")

    print()
    demostrar_colision()


if __name__ == "__main__":
    main()
