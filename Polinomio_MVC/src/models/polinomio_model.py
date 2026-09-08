# filepath: /polinomio-mvc-app/src/models/polinomio_model.py
"""Modelo (M de MVC) del ADT Polinomio.

Almacena los terminos del polinomio usando una lista enlazada y
sabe generar un polinomio aleatorio. El Modelo no conoce nada sobre
Tkinter ni sobre la Vista.
"""

import random
from typing import Optional


class NodoPolinomio:
    """Representa un termino individual del polinomio (nodo de la lista)."""

    def __init__(self, coeficiente: float, exponente: int):
        """Inicializa un termino con su coeficiente, exponente y enlace.

        Args:
            coeficiente: Numero que multiplica a la variable.
            exponente: Potencia a la que esta elevada la variable.
        """
        self.coeficiente = coeficiente
        self.exponente = exponente
        self.siguiente: Optional["NodoPolinomio"] = None


class PolinomioModel:
    """Modelo que almacena y genera aleatoriamente un polinomio."""

    def __init__(self):
        """Inicializa el modelo con un polinomio vacio."""
        self.cabeza: Optional[NodoPolinomio] = None

    def agregar_termino(self, coeficiente: float, exponente: int) -> None:
        """Agrega un termino al polinomio, manteniendolo ordenado por
        exponente de mayor a menor.

        Args:
            coeficiente: Numero que multiplica a la variable.
            exponente: Potencia a la que esta elevada la variable.
        """
        nuevo_nodo = NodoPolinomio(coeficiente, exponente)

        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            return

        actual = self.cabeza
        anterior = None
        while actual is not None and actual.exponente > exponente:
            anterior = actual
            actual = actual.siguiente

        if anterior is None:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza = nuevo_nodo
        else:
            anterior.siguiente = nuevo_nodo
            nuevo_nodo.siguiente = actual

    def generar_aleatorio(
        self,
        min_terminos: int = 3,
        max_terminos: int = 5,
        max_exponente: int = 5,
        rango_coeficiente: tuple = (-10, 10),
    ) -> None:
        """Genera un polinomio nuevo con terminos aleatorios, reemplazando
        el polinomio actual.

        Args:
            min_terminos: Cantidad minima de terminos a generar.
            max_terminos: Cantidad maxima de terminos a generar.
            max_exponente: Exponente maximo posible para un termino.
            rango_coeficiente: Tupla (minimo, maximo) para los coeficientes.
        """
        self.limpiar()

        cantidad = random.randint(min_terminos, max_terminos)
        exponentes_usados = random.sample(
            range(0, max_exponente + 1), k=min(cantidad, max_exponente + 1)
        )

        for exponente in exponentes_usados:
            coeficiente = random.randint(*rango_coeficiente)
            while coeficiente == 0:
                coeficiente = random.randint(*rango_coeficiente)
            self.agregar_termino(coeficiente, exponente)

    def obtener_representacion(self) -> str:
        """Obtiene el polinomio actual como texto legible.

        Returns:
            El polinomio en formato texto (ej: "-5x^2+20x+1"), o "0"
            si todavia no se genero ningun termino.
        """
        if self.cabeza is None:
            return "0"

        resultado = ""
        actual = self.cabeza
        while actual is not None:
            if actual.coeficiente != 0:
                if actual.coeficiente > 0 and len(resultado) > 0:
                    resultado += "+"
                if actual.coeficiente == -1 and actual.exponente != 0:
                    resultado += "-"
                elif actual.coeficiente != 1 or actual.exponente == 0:
                    resultado += str(actual.coeficiente)
                if actual.exponente > 0:
                    resultado += "x"
                    if actual.exponente > 1:
                        resultado += "^" + str(actual.exponente)
            actual = actual.siguiente

        return resultado if resultado else "0"

    def limpiar(self) -> None:
        """Elimina todos los terminos, dejando el polinomio vacio."""
        self.cabeza = None
