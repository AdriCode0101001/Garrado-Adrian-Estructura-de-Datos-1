"""Ejercicio 4 - Unidad 1: Persistencia.

Guardamos y recuperamos la lista de estudiantes en 2 formatos:
JSON y Pickle. La idea es comparar cuando conviene usar cada uno.
"""

import json
import pickle
from typing import Any

from Ejercicio_2 import ListaDinamica
from Ejercicio_3 import generar_estudiantes


def guardar_json(datos: Any, archivo: str) -> None:
    """Escribe datos (listas, dicts, numeros, texto) en un .json."""
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)


def cargar_json(archivo: str) -> Any:
    """Lee un archivo .json y devuelve la estructura de datos."""
    with open(archivo, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_pickle(objeto: Any, archivo: str) -> None:
    """Serializa cualquier objeto de Python a un archivo binario.

    A diferencia de guardar_json, esto funciona incluso con objetos
    de clases propias (por ejemplo una ListaDinamica completa).
    """
    with open(archivo, "wb") as f:
        pickle.dump(objeto, f)


def cargar_pickle(archivo: str) -> Any:
    """Reconstruye un objeto previamente guardado con pickle.dump."""
    with open(archivo, "rb") as f:
        return pickle.load(f)


def main() -> None:
    print("=== Persistencia: JSON vs Pickle ===\n")

    estudiantes = generar_estudiantes(10)

    # JSON: sirve bien para datos "planos" (listas de diccionarios)
    guardar_json(estudiantes, "estudiantes.json")
    desde_json = cargar_json("estudiantes.json")
    print(f"JSON: recargue {len(desde_json)} estudiantes")
    print(f"  primero -> {desde_json[0]}")

    # Pickle puede guardar la estructura completa, no solo los datos
    lista = ListaDinamica()
    for est in estudiantes:
        lista.insertar_al_final(est)

    guardar_pickle(lista, "estudiantes.pkl")
    desde_pickle = cargar_pickle("estudiantes.pkl")
    print(f"\nPickle: recupere un objeto de tipo {type(desde_pickle).__name__}")
    print(f"  tiene {len(desde_pickle)} elementos, con todos sus metodos")
    print(f"  primero -> {desde_pickle.obtener(0)}")

    print("\n¿Cuando usar cada uno?")
    print(
        "JSON es la opcion cuando los datos van a viajar fuera de "
        "Python: otro lenguaje, una API, o simplemente alguien que "
        "necesita abrir el archivo y leerlo. Es texto plano, asi que "
        "cualquiera lo entiende, pero solo sirve para datos basicos "
        "(no puede guardar una clase propia tal cual). Pickle en "
        "cambio guarda el objeto de Python completo, con su clase y "
        "comportamiento, ideal si despues vas a seguir usando esa "
        "misma estructura dentro de otro programa en Python. La "
        "contra es que el archivo no es legible y no deberia abrirse "
        "si no confias en quien lo genero."
    )


if __name__ == "__main__":
    main()