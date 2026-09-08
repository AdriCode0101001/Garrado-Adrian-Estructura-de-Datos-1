"""Ejercicio 3 - Unidad 0: Type hints y validaciones.

Modulo de funciones para operar una lista enlazada, con type hints
completos y validacion de indices mediante excepciones claras.
"""

from typing import Any, Optional


class IndiceInvalidoError(IndexError):
    """Se lanza cuando un indice esta fuera del rango valido de la lista."""


class ListaVaciaError(Exception):
    """Se lanza al intentar operar sobre una lista enlazada vacia."""


class Nodo:
    """Nodo de una lista enlazada simple."""

    def __init__(self, dato: Any) -> None:
        """Inicializa el nodo con un dato y sin enlace siguiente.

        Args:
            dato: El valor que almacena este nodo.
        """
        self.dato: Any = dato
        self.siguiente: Optional["Nodo"] = None


def longitud(cabeza: Optional[Nodo]) -> int:
    """Cuenta la cantidad de nodos en la lista.

    Args:
        cabeza: El primer nodo de la lista (o None si esta vacia).

    Returns:
        La cantidad de nodos en la lista.
    """
    contador = 0
    actual = cabeza
    while actual is not None:
        contador += 1
        actual = actual.siguiente
    return contador


def insertar_al_inicio(cabeza: Optional[Nodo], dato: Any) -> Nodo:
    """Inserta un nuevo nodo al inicio de la lista. O(1).

    Args:
        cabeza: El primer nodo de la lista actual (o None si esta vacia).
        dato: El valor a insertar.

    Returns:
        El nodo nuevo, que pasa a ser la nueva cabeza de la lista.
    """
    nuevo_nodo = Nodo(dato)
    nuevo_nodo.siguiente = cabeza
    return nuevo_nodo


def insertar_en_indice(cabeza: Optional[Nodo], indice: int, dato: Any) -> Nodo:
    """Inserta un nuevo nodo en la posicion indicada. O(n).

    Args:
        cabeza: El primer nodo de la lista actual (o None si esta vacia).
        indice: Posicion donde insertar (0-based). Debe estar entre
            0 y la longitud actual de la lista (inclusive).
        dato: El valor a insertar.

    Returns:
        La cabeza de la lista resultante (puede cambiar si indice es 0).

    Raises:
        IndiceInvalidoError: Si el indice es negativo o mayor a la
            longitud de la lista.

    Example:
        >>> cabeza = insertar_en_indice(None, 0, "a")
        >>> cabeza = insertar_en_indice(cabeza, 1, "b")
        >>> lista_a_texto(cabeza)
        'a -> b -> None'
    """
    total = longitud(cabeza)
    if indice < 0 or indice > total:
        raise IndiceInvalidoError(
            f"Indice {indice} fuera de rango [0, {total}]"
        )

    if indice == 0:
        return insertar_al_inicio(cabeza, dato)

    nuevo_nodo = Nodo(dato)
    actual = cabeza
    for _ in range(indice - 1):
        actual = actual.siguiente
    nuevo_nodo.siguiente = actual.siguiente
    actual.siguiente = nuevo_nodo
    return cabeza


def eliminar_en_indice(cabeza: Optional[Nodo], indice: int) -> Optional[Nodo]:
    """Elimina el nodo en la posicion indicada. O(n).

    Args:
        cabeza: El primer nodo de la lista actual.
        indice: Posicion a eliminar (0-based).

    Returns:
        La cabeza de la lista resultante (puede cambiar si indice es 0).

    Raises:
        ListaVaciaError: Si la lista esta vacia.
        IndiceInvalidoError: Si el indice esta fuera de rango.

    Example:
        >>> cabeza = insertar_en_indice(None, 0, "a")
        >>> cabeza = insertar_en_indice(cabeza, 1, "b")
        >>> cabeza = eliminar_en_indice(cabeza, 0)
        >>> lista_a_texto(cabeza)
        'b -> None'
    """
    if cabeza is None:
        raise ListaVaciaError("No se puede eliminar: la lista esta vacia")

    total = longitud(cabeza)
    if indice < 0 or indice >= total:
        raise IndiceInvalidoError(
            f"Indice {indice} fuera de rango [0, {total - 1}]"
        )

    if indice == 0:
        return cabeza.siguiente

    actual = cabeza
    for _ in range(indice - 1):
        actual = actual.siguiente
    actual.siguiente = actual.siguiente.siguiente
    return cabeza


def obtener_en_indice(cabeza: Optional[Nodo], indice: int) -> Any:
    """Retorna el dato almacenado en la posicion indicada. O(n).

    Args:
        cabeza: El primer nodo de la lista.
        indice: Posicion a consultar (0-based).

    Returns:
        El dato almacenado en esa posicion.

    Raises:
        IndiceInvalidoError: Si el indice esta fuera de rango.
    """
    total = longitud(cabeza)
    if indice < 0 or indice >= total:
        raise IndiceInvalidoError(
            f"Indice {indice} fuera de rango [0, {total - 1}]"
        )

    actual = cabeza
    for _ in range(indice):
        actual = actual.siguiente
    return actual.dato


def lista_a_texto(cabeza: Optional[Nodo]) -> str:
    """Convierte la lista enlazada en una representacion de texto.

    Args:
        cabeza: El primer nodo de la lista (o None si esta vacia).

    Returns:
        Una cadena con los datos separados por " -> ", terminando
        en "None" (ej: "10 -> 20 -> None").
    """
    partes = []
    actual = cabeza
    while actual is not None:
        partes.append(str(actual.dato))
        actual = actual.siguiente
    partes.append("None")
    return " -> ".join(partes)


def main() -> None:
    """Demuestra el uso del modulo, incluyendo el manejo de errores
    por indices invalidos y lista vacia.
    """
    print("=== Demo: Funciones sobre lista enlazada ===\n")

    cabeza: Optional[Nodo] = None
    cabeza = insertar_en_indice(cabeza, 0, 10)
    cabeza = insertar_en_indice(cabeza, 1, 30)
    cabeza = insertar_en_indice(cabeza, 1, 20)
    print(f"Lista: {lista_a_texto(cabeza)}")
    print(f"Longitud: {longitud(cabeza)}")

    print(f"\nElemento en indice 1: {obtener_en_indice(cabeza, 1)}")

    cabeza = eliminar_en_indice(cabeza, 1)
    print(f"Lista despues de eliminar indice 1: {lista_a_texto(cabeza)}")

    print("\n--- Probando validaciones ---")
    try:
        obtener_en_indice(cabeza, 99)
    except IndiceInvalidoError as error:
        print(f"Error capturado (indice invalido): {error}")

    cabeza = eliminar_en_indice(cabeza, 0)
    cabeza = eliminar_en_indice(cabeza, 0)
    try:
        eliminar_en_indice(cabeza, 0)
    except ListaVaciaError as error:
        print(f"Error capturado (lista vacia): {error}")


if __name__ == "__main__":
    main()