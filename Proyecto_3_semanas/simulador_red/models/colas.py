from typing import Any, Optional

from models.estructura_base import EstructuraLineal
from models.excepciones import EstructuraVaciaError
from models.nodo import Nodo
from models.excepciones import BufferLlenoError, EstructuraVaciaError


class NodoPrioridad(Nodo):
    """Nodo que además guarda la prioridad de su dato."""

    def __init__(self, dato: Any, prioridad: int) -> None:
        super().__init__(dato)
        self.prioridad = prioridad


class ColaPrioridad(EstructuraLineal):
    """Cola de prioridad estable.

    Sale primero el de mayor prioridad; si empatan, el que llegó antes.
    """
    def __init__(self) -> None:
        self._cabeza: Optional[NodoPrioridad] = None
        self._longitud: int = 0

    def esta_vacia(self) -> bool:
        """Indica si la cola no tiene elementos."""
        return self._cabeza is None

    def __len__(self) -> int:
        """Devuelve la cantidad de elementos."""
        return self._longitud

    def encolar(self, dato: Any, prioridad: int) -> None:
        """Inserta el dato en su posición según la prioridad. Es O(n)."""
        nuevo = NodoPrioridad(dato, prioridad)
        if self._cabeza is None or prioridad > self._cabeza.prioridad:
            nuevo.siguiente = self._cabeza
            self._cabeza = nuevo
        else:
            actual = self._cabeza
            while (actual.siguiente is not None
                   and actual.siguiente.prioridad >= prioridad):
                actual = actual.siguiente
            nuevo.siguiente = actual.siguiente
            actual.siguiente = nuevo
        self._longitud += 1

    def __str__(self) -> str:
        """Muestra la cola desde el frente: dato[pN] -> dato[pN] -> None."""
        texto = "FRENTE -> "
        actual = self._cabeza
        while actual is not None:
            texto += f"{actual.dato}[p{actual.prioridad}] -> "
            actual = actual.siguiente
        return texto + "None"

    def desencolar(self) -> Any:
        """Quita y devuelve el dato más urgente (el del frente). Es O(1)."""
        if self._cabeza is None:
            raise EstructuraVaciaError("La cola está vacía")
        dato = self._cabeza.dato
        self._cabeza = self._cabeza.siguiente
        self._longitud -= 1
        return dato

    def frente(self) -> Any:
        """Devuelve el dato del frente sin quitarlo. Es O(1)."""
        if self._cabeza is None:
            raise EstructuraVaciaError("La cola está vacía")
        return self._cabeza.dato

    def insertar(self, dato: Any, prioridad: int = 1) -> None:
        """Cumple el contrato: encola con prioridad 1 si no se indica otra."""
        self.encolar(dato, prioridad)

    def eliminar(self) -> Any:
        """Cumple el contrato: eliminar en una cola es desencolar."""
        return self.desencolar()


class ColaCircular(EstructuraLineal):
    """Buffer circular de tamaño fijo con aritmética modular.

    Es la única estructura que usa un arreglo: un buffer es por definición
    una memoria preasignada que no crece. Solo se escribe en posiciones con
    índices; nunca se usa append, pop ni insert.
    """

    def __init__(self, capacidad: int) -> None:
        if capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor que cero")
        self._capacidad: int = capacidad
        self._datos: list[Any] = [None] * capacidad
        self._frente: int = 0
        self._fondo: int = 0
        self._cantidad: int = 0

    def esta_vacia(self) -> bool:
        """Indica si el buffer no tiene elementos."""
        return self._cantidad == 0

    def esta_llena(self) -> bool:
        """Indica si el buffer no tiene celdas libres."""
        return self._cantidad == self._capacidad

    def __len__(self) -> int:
        """Devuelve la cantidad de elementos."""
        return self._cantidad

    def encolar(self, dato: Any) -> None:
        """Agrega un dato al fondo. Lanza BufferLlenoError si no cabe. O(1)."""
        if self.esta_llena():
            raise BufferLlenoError("El buffer está lleno")
        self._datos[self._fondo] = dato
        self._fondo = (self._fondo + 1) % self._capacidad
        self._cantidad += 1

    def __str__(self) -> str:
        """Muestra las celdas y la posición de frente y fondo."""
        texto = ""
        for i in range(self._capacidad):
            valor = "-" if self._datos[i] is None else self._datos[i]
            texto += f"[{i}:{valor}] "
        return (f"{texto}| frente={self._frente} fondo={self._fondo} "
                f"cantidad={self._cantidad}")

    def insertar(self, dato: Any) -> None:
        """Cumple el contrato: insertar equivale a encolar."""
        self.encolar(dato)

    def eliminar(self) -> Any:
        """Cumple el contrato: eliminar equivale a desencolar."""
        return self.desencolar()

    def desencolar(self) -> Any:
        """Saca y devuelve el dato del frente. O(1)."""
        if self.esta_vacia():
            raise EstructuraVaciaError("El buffer está vacío")
        dato = self._datos[self._frente]
        self._datos[self._frente] = None
        self._frente = (self._frente + 1) % self._capacidad
        self._cantidad -= 1
        return dato

    def frente(self) -> Any:
        """Consulta el dato del frente sin sacarlo."""
        if self.esta_vacia():
            raise EstructuraVaciaError("El buffer está vacío")
        return self._datos[self._frente]
