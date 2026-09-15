"""Ejercicio 1 - Unidad 2: ADT Polinomio.

Clase Polinomio con agregar_termino, evaluar, sumar, restar,
derivar y representacion en texto.
"""

from typing import Optional


class _Nodo:
    def __init__(self, coef: float, exp: int):
        self.coef = coef
        self.exp = exp
        self.siguiente: Optional["_Nodo"] = None


class Polinomio:
    """Polinomio representado como lista enlazada de terminos,
    ordenados de mayor a menor exponente.
    """

    def __init__(self):
        self.cabeza: Optional[_Nodo] = None

    def agregar_termino(self, coef: float, exp: int) -> None:
        """Agrega un termino, manteniendo el orden por exponente.
        Si ya existe un termino con ese exponente, suma el coeficiente.
        """
        if coef == 0:
            return

        if self.cabeza is None or exp > self.cabeza.exp:
            nuevo = _Nodo(coef, exp)
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo
            return

        actual = self.cabeza
        while actual.siguiente is not None and actual.siguiente.exp > exp:
            actual = actual.siguiente

        if actual.exp == exp:
            actual.coef += coef
            return
        if actual.siguiente is not None and actual.siguiente.exp == exp:
            actual.siguiente.coef += coef
            return

        nuevo = _Nodo(coef, exp)
        nuevo.siguiente = actual.siguiente
        actual.siguiente = nuevo

    def evaluar(self, x: float) -> float:
        """Evalua el polinomio para un valor de x."""
        resultado = 0
        actual = self.cabeza
        while actual is not None:
            resultado += actual.coef * (x ** actual.exp)
            actual = actual.siguiente
        return resultado

    def sumar(self, otro: "Polinomio") -> "Polinomio":
        """Devuelve un polinomio nuevo con la suma de ambos."""
        resultado = Polinomio()
        actual = self.cabeza
        while actual is not None:
            resultado.agregar_termino(actual.coef, actual.exp)
            actual = actual.siguiente
        actual = otro.cabeza
        while actual is not None:
            resultado.agregar_termino(actual.coef, actual.exp)
            actual = actual.siguiente
        return resultado

    def restar(self, otro: "Polinomio") -> "Polinomio":
        """Devuelve un polinomio nuevo con self - otro."""
        resultado = Polinomio()
        actual = self.cabeza
        while actual is not None:
            resultado.agregar_termino(actual.coef, actual.exp)
            actual = actual.siguiente
        actual = otro.cabeza
        while actual is not None:
            resultado.agregar_termino(-actual.coef, actual.exp)
            actual = actual.siguiente
        return resultado

    def derivar(self) -> "Polinomio":
        """Devuelve la derivada del polinomio como un Polinomio nuevo."""
        resultado = Polinomio()
        actual = self.cabeza
        while actual is not None:
            if actual.exp > 0:
                resultado.agregar_termino(actual.coef * actual.exp, actual.exp - 1)
            actual = actual.siguiente
        return resultado

    def __str__(self) -> str:
        if self.cabeza is None:
            return "0"

        texto = ""
        actual = self.cabeza
        while actual is not None:
            if actual.coef != 0:
                if actual.coef > 0 and texto:
                    texto += "+"
                if actual.coef == -1 and actual.exp != 0:
                    texto += "-"
                elif actual.coef != 1 or actual.exp == 0:
                    texto += str(actual.coef)
                if actual.exp > 0:
                    texto += "x"
                    if actual.exp > 1:
                        texto += f"^{actual.exp}"
            actual = actual.siguiente
        return texto if texto else "0"


def main():
    p1 = Polinomio()
    p1.agregar_termino(3, 2)
    p1.agregar_termino(2, 1)
    p1.agregar_termino(-5, 0)

    p2 = Polinomio()
    p2.agregar_termino(1, 2)
    p2.agregar_termino(-4, 0)

    p3 = Polinomio()
    p3.agregar_termino(7, 3)
    p3.agregar_termino(-1, 1)

    print(f"p1 = {p1}")
    print(f"p2 = {p2}")
    print(f"p3 = {p3}")

    print(f"\np1(2) = {p1.evaluar(2)}")
    print(f"p2(2) = {p2.evaluar(2)}")

    print(f"\np1 + p2 = {p1.sumar(p2)}")
    print(f"p1 - p2 = {p1.restar(p2)}")
    print(f"derivada de p1 = {p1.derivar()}")
    print(f"derivada de p3 = {p3.derivar()}")


if __name__ == "__main__":
    main()