"""Ejercicio 4 - Unidad 2: Integracion.

Problema aplicado: inventario de una tienda con varias sucursales.
Usa Conjunto para las categorias de productos, Polinomio para
estimar el crecimiento de ventas, y Matriz dispersa para el stock
(donde la mayoria de sucursales no tiene todos los productos).
"""

from ejercicio1_polinomio import Polinomio
from ejercicio2_conjunto import ConjuntoADT
from ejercicio3_matriz_dispersa import MatrizDispersa


def main():
    # --- Conjunto: categorias que maneja cada sucursal ---
    categorias_sucursal_a = ConjuntoADT(["Electronica", "Hogar", "Ropa"])
    categorias_sucursal_b = ConjuntoADT(["Hogar", "Juguetes"])

    print("--- Categorias por sucursal ---")
    print(f"Sucursal A: {categorias_sucursal_a}")
    print(f"Sucursal B: {categorias_sucursal_b}")
    print(f"Categorias en comun: {categorias_sucursal_a.interseccion(categorias_sucursal_b)}")
    print(f"Todas las categorias del negocio: {categorias_sucursal_a.union(categorias_sucursal_b)}")

    # --- Polinomio: estimacion simple de ventas segun el mes ---
    # ventas(mes) = 2*mes^2 + 10*mes + 50  (una estimacion inventada
    # a modo de ejemplo, no datos reales)
    ventas = Polinomio()
    ventas.agregar_termino(2, 2)
    ventas.agregar_termino(10, 1)
    ventas.agregar_termino(50, 0)

    print(f"\n--- Estimacion de ventas: {ventas} ---")
    for mes in [1, 3, 6]:
        print(f"  mes {mes}: {ventas.evaluar(mes)} unidades estimadas")

    # --- Matriz dispersa: stock por sucursal (filas) y producto (columnas) ---
    # la mayoria de sucursales no tiene todos los productos, de ahi
    # que tenga sentido usar la version dispersa en vez de una tabla
    # completa llena de ceros
    productos = ["TV", "Microondas", "Camisa", "Pelota"]
    stock = MatrizDispersa(2, len(productos))
    stock.establecer(0, 0, 5)   # sucursal A: 5 TVs
    stock.establecer(0, 2, 12)  # sucursal A: 12 camisas
    stock.establecer(1, 3, 8)   # sucursal B: 8 pelotas

    print("\n--- Stock (filas = sucursal, columnas = producto) ---")
    print("      " + "  ".join(f"{p:>10}" for p in productos))
    for i, nombre_sucursal in enumerate(["A", "B"]):
        fila = [stock.obtener(i, j) for j in range(len(productos))]
        print(f"  {nombre_sucursal}:  " + "  ".join(f"{v:>10}" for v in fila))

    print(f"\ndensidad del stock: {stock.densidad():.1f}% (la mayoria son 0,")
    print("por eso conviene una matriz dispersa en vez de una tabla completa)")


if __name__ == "__main__":
    main()