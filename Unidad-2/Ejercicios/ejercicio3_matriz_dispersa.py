"""Ejercicio 3 - Unidad 2: Matriz dispersa.

MatrizDispersa usando diccionario {(fila, columna): valor} en vez
de guardar todas las celdas, incluidas las que valen 0.
"""

import sys
import time


class MatrizDispersa:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.datos = {}  # solo guarda las celdas != 0

    def establecer(self, i, j, valor):
        if not (0 <= i < self.filas and 0 <= j < self.columnas):
            raise IndexError(f"posicion ({i},{j}) fuera de la matriz {self.filas}x{self.columnas}")
        if valor == 0:
            self.datos.pop((i, j), None)  # no tiene sentido guardar un 0
        else:
            self.datos[(i, j)] = valor

    def obtener(self, i, j):
        if not (0 <= i < self.filas and 0 <= j < self.columnas):
            raise IndexError(f"posicion ({i},{j}) fuera de la matriz {self.filas}x{self.columnas}")
        return self.datos.get((i, j), 0)

    def transponer(self):
        nueva = MatrizDispersa(self.columnas, self.filas)
        for (i, j), valor in self.datos.items():
            nueva.establecer(j, i, valor)
        return nueva

    def densidad(self):
        """Porcentaje de celdas que NO son cero."""
        total_celdas = self.filas * self.columnas
        if total_celdas == 0:
            return 0.0
        return len(self.datos) / total_celdas * 100

    def __str__(self):
        filas_texto = []
        for i in range(self.filas):
            fila = [str(self.obtener(i, j)) for j in range(self.columnas)]
            filas_texto.append(" ".join(fila))
        return "\n".join(filas_texto)


def comparar_con_matriz_densa(filas, columnas, no_ceros):
    """Compara memoria aproximada entre la version dispersa y una
    matriz densa (lista de listas) con la misma cantidad de datos.
    """
    dispersa = MatrizDispersa(filas, columnas)
    for i in range(no_ceros):
        dispersa.establecer(i % filas, (i * 3) % columnas, i + 1)

    densa = [[0] * columnas for _ in range(filas)]
    for i in range(no_ceros):
        densa[i % filas][(i * 3) % columnas] = i + 1

    mem_dispersa = sys.getsizeof(dispersa.datos)
    mem_densa = sys.getsizeof(densa) + sum(sys.getsizeof(fila) for fila in densa)

    print(f"Matriz {filas}x{columnas} con {no_ceros} valores distintos de 0:")
    print(f"  densidad: {dispersa.densidad():.2f}%")
    print(f"  memoria dispersa (dict): {mem_dispersa} bytes")
    print(f"  memoria densa (listas):  {mem_densa} bytes")


def main():
    m = MatrizDispersa(4, 4)
    m.establecer(0, 0, 5)
    m.establecer(1, 2, 8)
    m.establecer(3, 3, -1)

    print("Matriz:")
    print(m)
    print(f"\nobtener(1,2) = {m.obtener(1, 2)}")
    print(f"obtener(0,1) = {m.obtener(0, 1)} (celda vacia)")
    print(f"densidad = {m.densidad():.2f}%")

    print("\nTranspuesta:")
    print(m.transponer())

    print()
    try:
        m.obtener(10, 10)
    except IndexError as error:
        print(f"error capturado: {error}")

    print()
    comparar_con_matriz_densa(1000, 1000, 20)


if __name__ == "__main__":
    main()