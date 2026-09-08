"""Ejercicio 2 - Unidad 0: Docstrings completos.

Implementacion de una Pila (TDA LIFO) con docstrings completos que
incluyen descripcion, argumentos, retorno, excepciones y ejemplo de
uso en cada metodo publico.
"""

from typing import Any


class EstructuraVaciaError(Exception):
    """Se lanza al intentar operar sobre una estructura vacia."""


class Pila:
    """Implementacion de una Pila (TDA LIFO - Last In, First Out).

    Los elementos se agregan y se retiran siempre por el mismo
    extremo, llamado "tope" de la pila.
    """

    def __init__(self) -> None:
        """Inicializa una pila vacia.

        Example:
            >>> pila = Pila()
            >>> pila.esta_vacia()
            True
        """
        self._datos: list[Any] = []

    def apilar(self, dato: Any) -> None:
        """Agrega un elemento al tope de la pila.

        Args:
            dato: El valor a agregar. Puede ser de cualquier tipo.

        Returns:
            None.

        Example:
            >>> pila = Pila()
            >>> pila.apilar(10)
            >>> pila.apilar(20)
            >>> len(pila)
            2
        """
        self._datos.append(dato)

    def desapilar(self) -> Any:
        """Elimina y retorna el elemento en el tope de la pila.

        Returns:
            El valor que estaba en el tope de la pila.

        Raises:
            EstructuraVaciaError: Si la pila esta vacia.

        Example:
            >>> pila = Pila()
            >>> pila.apilar(10)
            >>> pila.apilar(20)
            >>> pila.desapilar()
            20
        """
        if self.esta_vacia():
            raise EstructuraVaciaError(
                "No se puede desapilar: la pila esta vacia"
            )
        return self._datos.pop()

    def tope(self) -> Any:
        """Retorna el elemento en el tope sin eliminarlo de la pila.

        Returns:
            El valor que esta en el tope de la pila.

        Raises:
            EstructuraVaciaError: Si la pila esta vacia.

        Example:
            >>> pila = Pila()
            >>> pila.apilar(10)
            >>> pila.tope()
            10
            >>> len(pila)
            1
        """
        if self.esta_vacia():
            raise EstructuraVaciaError(
                "No se puede consultar el tope: la pila esta vacia"
            )
        return self._datos[-1]

    def esta_vacia(self) -> bool:
        """Indica si la pila no tiene elementos.

        Returns:
            True si la pila esta vacia, False en caso contrario.

        Example:
            >>> pila = Pila()
            >>> pila.esta_vacia()
            True
            >>> pila.apilar(1)
            >>> pila.esta_vacia()
            False
        """
        return len(self._datos) == 0

    def __len__(self) -> int:
        """Retorna la cantidad de elementos en la pila.

        Returns:
            El numero de elementos actualmente en la pila.

        Example:
            >>> pila = Pila()
            >>> pila.apilar(1)
            >>> pila.apilar(2)
            >>> len(pila)
            2
        """
        return len(self._datos)

    def __bool__(self) -> bool:
        """Permite usar la pila en expresiones booleanas (if pila:).

        Returns:
            True si la pila tiene elementos, False si esta vacia.
        """
        return not self.esta_vacia()


def main() -> None:
    """Demuestra el uso de la clase Pila, incluyendo el manejo de
    la excepcion al operar sobre una pila vacia.
    """
    print("=== Demo: Pila (TDA LIFO) ===\n")

    pila = Pila()
    print(f"¿Vacia al crearla? {pila.esta_vacia()}")

    for valor in [10, 20, 30]:
        pila.apilar(valor)
    print(f"Despues de apilar 10, 20, 30 -> tamano: {len(pila)}")
    print(f"Tope actual: {pila.tope()}")

    print(f"Desapilado: {pila.desapilar()}")
    print(f"Tamano despues de desapilar: {len(pila)}")

    if pila:
        print("La pila todavia tiene elementos (uso de __bool__).")

    pila.desapilar()
    pila.desapilar()
    print(f"\n¿Vacia ahora? {pila.esta_vacia()}")

    try:
        pila.desapilar()
    except EstructuraVaciaError as error:
        print(f"Error capturado correctamente: {error}")


if __name__ == "__main__":
    main()