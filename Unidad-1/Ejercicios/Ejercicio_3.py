"""Ejercicio 3 - Unidad 1: Simulacion de datos.

Genera 50 estudiantes de prueba y los carga en las 2 estructuras
del ejercicio anterior (ArrayEstatico y ListaDinamica), para
comparar tiempo de insercion, busqueda y memoria aproximada.

Nota: los nombres se arman combinando listas fijas en vez de usar
Faker, para no depender de instalar una libreria extra. La memoria
"aproximada" es justo eso, una aproximacion con sys.getsizeof(),
no el uso real y exacto del proceso.
"""

import random
import sys
import time
from typing import Any

from Ejercicio_2 import ArrayEstatico, ListaDinamica

NOMBRES = ["Ana", "Luis", "Carla", "Robert", "Marco", "Sofia", "Diego", "Elena"]
APELLIDOS = ["Gomez", "Mamani", "Quispe", "Rojas", "Fernandez", "Paz", "Vaca"]
GRUPOS = ["A", "B", "C"]


def generar_estudiante() -> dict[str, Any]:
    return {
        "nombre": f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)}",
        "nota": round(random.uniform(0, 100), 1),
        "grupo": random.choice(GRUPOS),
    }


def generar_estudiantes(cantidad: int) -> list[dict[str, Any]]:
    """Genera 'cantidad' estudiantes simulados de una vez."""
    return [generar_estudiante() for _ in range(cantidad)]


def buscar_por_nombre_array(array: ArrayEstatico, nombre: str) -> Any:
    for i in range(len(array)):
        est = array.obtener(i)
        if est["nombre"] == nombre:
            return est
    return None


def buscar_por_nombre_lista(lista: ListaDinamica, nombre: str) -> Any:
    for i in range(len(lista)):
        est = lista.obtener(i)
        if est["nombre"] == nombre:
            return est
    return None


def reportar(cantidad: int = 50) -> None:
    """Corre la comparacion completa e imprime los resultados."""
    estudiantes = generar_estudiantes(cantidad)
    nombre_buscado = estudiantes[-1]["nombre"]  # peor caso: el ultimo

    array = ArrayEstatico(cantidad)
    t0 = time.perf_counter()
    for est in estudiantes:
        array.agregar(est)
    tiempo_array = time.perf_counter() - t0

    lista = ListaDinamica()
    t0 = time.perf_counter()
    for est in estudiantes:
        lista.insertar_al_final(est)
    tiempo_lista = time.perf_counter() - t0

    t0 = time.perf_counter()
    buscar_por_nombre_array(array, nombre_buscado)
    busqueda_array = time.perf_counter() - t0

    t0 = time.perf_counter()
    buscar_por_nombre_lista(lista, nombre_buscado)
    busqueda_lista = time.perf_counter() - t0

    mem_array = array.memoria_aproximada()
    mem_lista = lista.memoria_aproximada()

    print(f"=== {cantidad} estudiantes simulados ===\n")
    print("Insercion:")
    print(f"  Array -> {tiempo_array:.6f}s")
    print(f"  Lista -> {tiempo_lista:.6f}s")

    print("\nBusqueda por nombre (peor caso, el ultimo insertado):")
    print(f"  Array -> {busqueda_array:.6f}s")
    print(f"  Lista -> {busqueda_lista:.6f}s")
    print("  Las 2 son O(n) igual, ninguna indexa por nombre.")

    print("\nMemoria aproximada:")
    print(f"  Array -> {mem_array} bytes (bloque contiguo)")
    print(f"  Lista -> {mem_lista} bytes estimado (nodos sueltos + overhead)")


if __name__ == "__main__":
    reportar(50)