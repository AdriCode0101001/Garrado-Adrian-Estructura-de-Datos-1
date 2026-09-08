"""Modulo que representa un polinomio usando una lista enlazada (TDA dinamico).

Ejemplo aplicado: trayectoria de un objeto lanzado al aire,
h(t) = -5t^2 + 20t + 1
"""


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
        self.siguiente = None


class Polinomio:
    """Representa un polinomio completo como una lista enlazada de terminos."""

    def __init__(self):
        """Inicializa un polinomio vacio (sin terminos)."""
        self.cabeza = None

    def agregar_termino(self, coeficiente: float, exponente: int) -> None:
        """Agrega un nuevo termino al polinomio, ordenado por exponente.

        Args:
            coeficiente: Numero que multiplica a la variable.
            exponente: Potencia a la que esta elevada la variable.
        """
        nuevo_nodo = NodoPolinomio(coeficiente, exponente)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
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

    def evaluar(self, valor_t: float) -> float:
        """Evalua el polinomio para un valor especifico de la variable.

        Args:
            valor_t: Valor numerico a sustituir en la variable (ej: tiempo).

        Returns:
            El resultado numerico del polinomio evaluado en valor_t.
        """
        resultado = 0
        actual = self.cabeza
        while actual is not None:
            resultado += actual.coeficiente * (valor_t ** actual.exponente)
            actual = actual.siguiente
        return resultado

    def __str__(self) -> str:
        """Devuelve la representacion en texto del polinomio (ej: -5x^2+20x+1)."""
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
                    resultado += "t"
                    if actual.exponente > 1:
                        resultado += "^" + str(actual.exponente)
            actual = actual.siguiente
        return resultado if resultado else "0"


if __name__ == "__main__":
    # Trayectoria de un objeto lanzado al aire: h(t) = -5t^2 + 20t + 1
    trayectoria = Polinomio()
    trayectoria.agregar_termino(-5, 2)  # efecto de la gravedad
    trayectoria.agregar_termino(20, 1)  # velocidad inicial
    trayectoria.agregar_termino(1, 0)   # altura inicial (desde donde se lanza)

    print(f"Polinomio de la trayectoria: h(t) = {trayectoria}")

    # Evaluamos la altura en distintos momentos del tiempo
    for tiempo in [0, 1, 2, 3, 4]:
        altura = trayectoria.evaluar(tiempo)
        print(f"En t = {tiempo}s, la altura es: {altura}m")