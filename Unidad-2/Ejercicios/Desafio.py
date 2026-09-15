"""Desafio - Unidad 2.

Multiplicacion de polinomios y suma de matrices dispersas,
validando que las matrices tengan las mismas dimensiones.
"""

from ejercicio1_polinomio import Polinomio
from ejercicio3_matriz_dispersa import MatrizDispersa


def multiplicar_polinomios(p1, p2):
    """Multiplica 2 polinomios termino por termino y devuelve el
    resultado como un Polinomio nuevo.
    """
    resultado = Polinomio()
    actual1 = p1.cabeza
    while actual1 is not None:
        actual2 = p2.cabeza
        while actual2 is not None:
            nuevo_coef = actual1.coef * actual2.coef
            nuevo_exp = actual1.exp + actual2.exp
            resultado.agregar_termino(nuevo_coef, nuevo_exp)
            actual2 = actual2.siguiente
        actual1 = actual1.siguiente
    return resultado


def sumar_matrices_dispersas(m1, m2):
    """Suma 2 matrices dispersas celda por celda.

    Lanza ValueError si las dimensiones no coinciden - no tiene
    sentido sumar una matriz 3x3 con una 4x4.
    """
    if m1.filas != m2.filas or m1.columnas != m2.columnas:
        raise ValueError(
            f"no se pueden sumar matrices de distinto tamano: "
            f"{m1.filas}x{m1.columnas} vs {m2.filas}x{m2.columnas}"
        )

    resultado = MatrizDispersa(m1.filas, m1.columnas)
    # recorremos las celdas no-cero de ambas, sin repetir posiciones
    posiciones = set(m1.datos.keys()) | set(m2.datos.keys())
    for (i, j) in posiciones:
        resultado.establecer(i, j, m1.obtener(i, j) + m2.obtener(i, j))
    return resultado


def main():
    print("--- Multiplicacion de polinomios ---")
    p1 = Polinomio()
    p1.agregar_termino(2, 1)
    p1.agregar_termino(3, 0)  # p1 = 2x + 3

    p2 = Polinomio()
    p2.agregar_termino(1, 1)
    p2.agregar_termino(-4, 0)  # p2 = x - 4

    print(f"p1 = {p1}")
    print(f"p2 = {p2}")
    print(f"p1 * p2 = {multiplicar_polinomios(p1, p2)}")
    # (2x+3)(x-4) = 2x^2 -8x +3x -12 = 2x^2 -5x -12

    print("\n--- Suma de matrices dispersas ---")
    m1 = MatrizDispersa(3, 3)
    m1.establecer(0, 0, 5)
    m1.establecer(1, 1, 2)

    m2 = MatrizDispersa(3, 3)
    m2.establecer(1, 1, 3)
    m2.establecer(2, 2, 7)

    suma = sumar_matrices_dispersas(m1, m2)
    print("m1:")
    print(m1)
    print("\nm2:")
    print(m2)
    print("\nm1 + m2:")
    print(suma)

    print("\n--- Probando validacion de dimensiones ---")
    m3 = MatrizDispersa(4, 4)
    try:
        sumar_matrices_dispersas(m1, m3)
    except ValueError as error:
        print(f"error capturado: {error}")


if __name__ == "__main__":
    main()