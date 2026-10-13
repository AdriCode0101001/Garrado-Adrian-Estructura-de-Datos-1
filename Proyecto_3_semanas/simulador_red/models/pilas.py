from typing import Any, Optional, Iterator

from models.estructura_base import EstructuraLineal
from models.excepciones import EstructuraVaciaError
from models.nodo import Nodo


class Pila(EstructuraLineal):
    """Pila LIFO: el último en entrar es el primero en salir."""

    def __init__(self) -> None:
        self._tope: Optional[Nodo] = None
        self._longitud: int = 0

    def esta_vacia(self) -> bool:
        """Indica si la pila no tiene elementos."""
        return self._tope is None

    def __len__(self) -> int:
        """Devuelve la cantidad de elementos."""
        return self._longitud

    def apilar(self, dato: Any) -> None:
        """Pone un dato encima de la pila. Es O(1)."""
        nuevo = Nodo(dato)
        nuevo.siguiente = self._tope
        self._tope = nuevo
        self._longitud += 1

    def desapilar(self) -> Any:
        """Quita y devuelve el dato del tope. Es O(1)."""
        if self._tope is None:
            raise EstructuraVaciaError("La pila está vacía")
        dato = self._tope.dato
        self._tope = self._tope.siguiente
        self._longitud -= 1
        return dato

    def tope(self) -> Any:
        """Devuelve el dato del tope sin quitarlo. Es O(1)."""
        if self._tope is None:
            raise EstructuraVaciaError("La pila está vacía")
        return self._tope.dato

    def insertar(self, dato: Any) -> None:
        """Cumple el contrato: insertar en una pila es apilar."""
        self.apilar(dato)

    def eliminar(self) -> Any:
        """Cumple el contrato: eliminar en una pila es desapilar."""
        return self.desapilar()

    def __str__(self) -> str:
        """Muestra la pila de arriba (tope) hacia abajo."""
        texto = "TOPE -> "
        actual = self._tope
        while actual is not None:
            texto += f"{actual.dato} -> "
            actual = actual.siguiente
        return texto + "None"

    def __iter__(self) -> Iterator[Any]:
        """Recorre la pila desde el tope hacia el fondo."""
        actual = self._tope
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente


class UndoRedoManager:
    """Historial de acciones con deshacer y rehacer, usando dos pilas."""

    def __init__(self) -> None:
        self._deshacer: Pila = Pila()
        self._rehacer: Pila = Pila()

    def registrar(self, accion: Any) -> None:
        """Guarda una acción nueva; ya no se podrá rehacer lo anterior."""
        self._deshacer.apilar(accion)
        self._rehacer = Pila()

    def deshacer(self) -> Any:
        """Revierte la última acción y la deja para rehacer. Es O(1)."""
        if self._deshacer.esta_vacia():
            raise EstructuraVaciaError("No hay acciones para deshacer")
        accion = self._deshacer.desapilar()
        self._rehacer.apilar(accion)
        return accion

    def rehacer(self) -> Any:
        """Reaplica la última acción deshecha. Es O(1)."""
        if self._rehacer.esta_vacia():
            raise EstructuraVaciaError("No hay acciones para rehacer")
        accion = self._rehacer.desapilar()
        self._deshacer.apilar(accion)
        return accion

    def puede_deshacer(self) -> bool:
        """Indica si hay acciones para deshacer."""
        return not self._deshacer.esta_vacia()

    def puede_rehacer(self) -> bool:
        """Indica si hay acciones para rehacer."""
        return not self._rehacer.esta_vacia()

    def __str__(self) -> str:
        """Muestra las dos pilas."""
        return f"DESHACER: {self._deshacer}\nREHACER:  {self._rehacer}"

    @property
    def pila_deshacer(self) -> Pila:
        """Acciones que se pueden deshacer (solo lectura)."""
        return self._deshacer

    @property
    def pila_rehacer(self) -> Pila:
        """Acciones que se pueden rehacer (solo lectura)."""
        return self._rehacer
