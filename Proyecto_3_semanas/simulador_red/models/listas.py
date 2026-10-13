from typing import Any, Iterator, Optional

from models.estructura_base import EstructuraLineal
from models.excepciones import EstructuraVaciaError
from models.nodo import Nodo


class ListaSimple(EstructuraLineal):
    """Lista enlazada simple: cada nodo conoce solo al siguiente."""

    def __init__(self) -> None:
        self._cabeza: Optional[Nodo] = None
        self._longitud: int = 0

    def esta_vacia(self) -> bool:
        """Indica si la lista no tiene nodos."""
        return self._cabeza is None

    def __len__(self) -> int:
        """Devuelve la cantidad de nodos."""
        return self._longitud

    def insertar_inicio(self, dato: Any) -> None:
        """Agrega un dato al principio de la lista. Es O(1)."""
        nuevo = Nodo(dato)
        nuevo.siguiente = self._cabeza
        self._cabeza = nuevo
        self._longitud += 1

    def __str__(self) -> str:
        """Muestra la lista como: dato -> dato -> None."""
        texto = ""
        actual = self._cabeza
        while actual is not None:
            texto += f"{actual.dato} -> "
            actual = actual.siguiente
        return texto + "None"

    def __iter__(self) -> Iterator[Any]:
        """Recorre la lista de la cabeza hacia el final."""
        actual = self._cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def insertar_final(self, dato: Any) -> None:
        """Agrega un dato al final de la lista. Es O(n)."""
        nuevo = Nodo(dato)
        if self._cabeza is None:
            self._cabeza = nuevo
        else:
            actual = self._cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self._longitud += 1

    def buscar(self, dato: Any) -> bool:
        """Indica si el dato existe en la lista. Es O(n)."""
        actual = self._cabeza
        while actual is not None:
            if actual.dato == dato:
                return True
            actual = actual.siguiente
        return False

    def insertar(self, dato: Any) -> None:
        """Cumple el contrato: agrega al final (orden de llegada)."""
        self.insertar_final(dato)

    def eliminar_valor(self, dato: Any) -> bool:
        """Elimina la primera aparición del dato. Es O(n)."""
        anterior = None
        actual = self._cabeza
        while actual is not None:
            if actual.dato == dato:
                if anterior is None:
                    self._cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                self._longitud -= 1
                return True
            anterior = actual
            actual = actual.siguiente
        return False

    def eliminar(self) -> Any:
        """Cumple el contrato: quita y devuelve el primer dato. Es O(1)."""
        if self._cabeza is None:
            raise EstructuraVaciaError("La lista está vacía")
        dato = self._cabeza.dato
        self._cabeza = self._cabeza.siguiente
        self._longitud -= 1
        return dato


class ListaDoble(EstructuraLineal):
    """Lista doblemente enlazada: cada nodo conoce a sus dos vecinos."""

    def __init__(self) -> None:
        self._actual: Optional[Nodo] = None
        self._cabeza: Optional[Nodo] = None
        self._cola: Optional[Nodo] = None
        self._longitud: int = 0

    def esta_vacia(self) -> bool:
        """Indica si la lista no tiene nodos."""
        return self._cabeza is None

    def __len__(self) -> int:
        """Devuelve la cantidad de nodos."""
        return self._longitud

    def insertar_inicio(self, dato: Any) -> None:
        """Agrega un dato al principio de la lista. Es O(1)."""
        nuevo = Nodo(dato)
        if self._cabeza is None:
            self._cabeza = nuevo
            self._cola = nuevo
        else:
            nuevo.siguiente = self._cabeza
            self._cabeza.anterior = nuevo
            self._cabeza = nuevo
        self._longitud += 1

    def insertar_final(self, dato: Any) -> None:
        """Agrega un dato al final de la lista. Es O(1) gracias a _cola."""
        nuevo = Nodo(dato)
        if self._cola is None:
            self._cabeza = nuevo
            self._cola = nuevo
        else:
            nuevo.anterior = self._cola
            self._cola.siguiente = nuevo
            self._cola = nuevo
        self._longitud += 1

    def __str__(self) -> str:
        """Muestra la lista de izquierda a derecha."""
        texto = "None <-> "
        actual = self._cabeza
        while actual is not None:
            texto += f"{actual.dato} <-> "
            actual = actual.siguiente
        return texto + "None"

    def __iter__(self) -> Iterator[Any]:
        """Recorre la lista de la cabeza hacia el final."""
        actual = self._cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def mostrar_inverso(self) -> str:
        """Muestra la lista de derecha a izquierda, usando 'anterior'."""
        texto = "None <-> "
        actual = self._cola
        while actual is not None:
            texto += f"{actual.dato} <-> "
            actual = actual.anterior
        return texto + "None"

    def insertar(self, dato: Any) -> None:
        """Cumple el contrato: agrega al final (orden de llegada)."""
        self.insertar_final(dato)

    def _desenlazar(self, nodo: Nodo) -> None:
        """Quita de la lista un nodo ya conocido. Es O(1)."""
        if self._actual is nodo:
            if nodo.siguiente is not None:
                self._actual = nodo.siguiente
            else:
                self._actual = nodo.anterior
        if nodo.anterior is None:
            self._cabeza = nodo.siguiente
        else:
            nodo.anterior.siguiente = nodo.siguiente
        if nodo.siguiente is None:
            self._cola = nodo.anterior
        else:
            nodo.siguiente.anterior = nodo.anterior
        self._longitud -= 1

    def eliminar_valor(self, dato: Any) -> bool:
        """Elimina la primera aparición del dato. Buscarlo es O(n)."""
        actual = self._cabeza
        while actual is not None:
            if actual.dato == dato:
                self._desenlazar(actual)
                return True
            actual = actual.siguiente
        return False

    def eliminar(self) -> Any:
        """Cumple el contrato: quita y devuelve el primer dato. Es O(1)."""
        if self._cabeza is None:
            raise EstructuraVaciaError("La lista está vacía")
        dato = self._cabeza.dato
        self._desenlazar(self._cabeza)
        return dato

    def avanzar(self) -> Any:
        """Mueve el cursor un nodo adelante y devuelve su dato. O(1)."""
        if self._cabeza is None:
            raise EstructuraVaciaError("La lista está vacía")
        if self._actual is None:
            self._actual = self._cabeza
        elif self._actual.siguiente is not None:
            self._actual = self._actual.siguiente
        return self._actual.dato

    def retroceder(self) -> Any:
        """Mueve el cursor un nodo hacia atrás y devuelve su dato. Es O(1)."""
        if self._cabeza is None:
            raise EstructuraVaciaError("La lista está vacía")
        if self._actual is None:
            self._actual = self._cabeza
        elif self._actual.anterior is not None:
            self._actual = self._actual.anterior
        return self._actual.dato


class ListaCircularDoble(EstructuraLineal):
    """Anillo: el último nodo apunta al primero y viceversa."""

    def __init__(self) -> None:
        self._cabeza: Optional[Nodo] = None
        self._longitud: int = 0
        self._actual: Optional[Nodo] = None

    def esta_vacia(self) -> bool:
        """Indica si el anillo no tiene nodos."""
        return self._cabeza is None

    def __len__(self) -> int:
        """Devuelve la cantidad de nodos."""
        return self._longitud

    def insertar_final(self, dato: Any) -> None:
        """Agrega un nodo antes de la cabeza, o sea al final. O(1)."""
        nuevo = Nodo(dato)
        if self._cabeza is None:
            nuevo.siguiente = nuevo
            nuevo.anterior = nuevo
            self._cabeza = nuevo
            self._actual = nuevo
        else:
            ultimo = self._cabeza.anterior
            nuevo.anterior = ultimo
            nuevo.siguiente = self._cabeza
            ultimo.siguiente = nuevo
            self._cabeza.anterior = nuevo
        self._longitud += 1

    def __str__(self) -> str:
        """Muestra el anillo y a quién vuelve al llegar al final."""
        if self._cabeza is None:
            return "(anillo vacío)"
        texto = ""
        actual = self._cabeza
        for _ in range(self._longitud):
            texto += f"{actual.dato} <-> "
            actual = actual.siguiente
        return texto + f"(vuelve a {self._cabeza.dato})"

    def __iter__(self) -> Iterator[Any]:
        """Recorre el anillo una sola vuelta, desde la cabeza."""
        actual = self._cabeza
        for _ in range(self._longitud):
            yield actual.dato
            actual = actual.siguiente

    def insertar(self, dato: Any) -> None:
        """Cumple el contrato: insertar equivale a insertar_final."""
        self.insertar_final(dato)

    def _desenlazar(self, nodo: Nodo) -> None:
        """Saca un nodo del anillo y reconecta a sus vecinos."""
        if self._longitud == 1:
            self._cabeza = None
            self._actual = None
        else:
            nodo.anterior.siguiente = nodo.siguiente
            nodo.siguiente.anterior = nodo.anterior
            if nodo is self._cabeza:
                self._cabeza = nodo.siguiente
            if nodo is self._actual:
                self._actual = nodo.siguiente
        self._longitud -= 1

    def eliminar_valor(self, dato: Any) -> bool:
        """Elimina el primer nodo con ese dato. Devuelve si existía."""
        actual = self._cabeza
        for _ in range(self._longitud):
            if actual.dato == dato:
                self._desenlazar(actual)
                return True
            actual = actual.siguiente
        return False

    def eliminar(self) -> Any:
        """Elimina la cabeza y devuelve su dato."""
        if self._cabeza is None:
            raise EstructuraVaciaError("El anillo está vacío")
        dato = self._cabeza.dato
        self._desenlazar(self._cabeza)
        return dato

    def token(self) -> Any:
        """Devuelve quién tiene el token, sin moverlo."""
        if self._actual is None:
            raise EstructuraVaciaError("El anillo está vacío")
        return self._actual.dato

    def avanzar_token(self) -> Any:
        """Pasa el token al siguiente nodo y devuelve su dato. O(1)."""
        if self._actual is None:
            raise EstructuraVaciaError("El anillo está vacío")
        self._actual = self._actual.siguiente
        return self._actual.dato
