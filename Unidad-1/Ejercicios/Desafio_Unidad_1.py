"""Desafio - Unidad 1: RepositorioEstudiantes.

Una capa de repositorio con guardar/cargar/agregar/listar, donde la
implementacion concreta es intercambiable sin tocar el codigo que usa el repositorio. 
Mismo principio que el ADTPila del ejercicio 1: el cliente solo conoce la interfaz.
"""

import json
import pickle
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class RepositorioEstudiantes(ABC):
    """Interfaz para guardar/cargar una lista de estudiantes."""

    @abstractmethod
    def agregar(self, estudiante: dict[str, Any]) -> None:
        """Agrega un estudiante a la coleccion en memoria."""

    @abstractmethod
    def guardar(self) -> None:
        """Persiste la coleccion actual en disco."""

    @abstractmethod
    def cargar(self) -> None:
        """Carga la coleccion desde disco a memoria."""

    @abstractmethod
    def listar(self) -> list[dict[str, Any]]:
        """Devuelve los estudiantes actualmente en memoria."""


class RepositorioJSON(RepositorioEstudiantes):
    """Guarda los estudiantes en un archivo .json."""

    def __init__(self, archivo: str) -> None:
        self.archivo = archivo
        self._datos: list[dict[str, Any]] = []

    def agregar(self, estudiante: dict[str, Any]) -> None:
        self._datos.append(estudiante)

    def guardar(self) -> None:
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(self._datos, f, indent=2, ensure_ascii=False)

    def cargar(self) -> None:
        if not Path(self.archivo).exists():
            self._datos = []
            return
        with open(self.archivo, "r", encoding="utf-8") as f:
            self._datos = json.load(f)

    def listar(self) -> list[dict[str, Any]]:
        return self._datos


class RepositorioPickle(RepositorioEstudiantes):
    """Guarda los estudiantes en un archivo .pkl (binario)."""

    def __init__(self, archivo: str) -> None:
        self.archivo = archivo
        self._datos: list[dict[str, Any]] = []

    def agregar(self, estudiante: dict[str, Any]) -> None:
        self._datos.append(estudiante)

    def guardar(self) -> None:
        with open(self.archivo, "wb") as f:
            pickle.dump(self._datos, f)

    def cargar(self) -> None:
        if not Path(self.archivo).exists():
            self._datos = []
            return
        with open(self.archivo, "rb") as f:
            self._datos = pickle.load(f)

    def listar(self) -> list[dict[str, Any]]:
        return self._datos


def registrar_estudiantes(repo: RepositorioEstudiantes) -> None:
    """Funcion cliente: agrega 3 estudiantes y guarda. No sabe si
    el repositorio de verdad usa JSON o Pickle por dentro.
    """
    repo.agregar({"nombre": "Ana Torrez", "nota": 85.0, "grupo": "A"})
    repo.agregar({"nombre": "Luis Choque", "nota": 72.5, "grupo": "B"})
    repo.agregar({"nombre": "Carla Mamani", "nota": 91.0, "grupo": "A"})
    repo.guardar()


def main() -> None:
    print("=== Desafio: RepositorioEstudiantes (JSON vs Pickle) ===\n")

    repo_json = RepositorioJSON("repo_estudiantes.json")
    registrar_estudiantes(repo_json)

    repo_pickle = RepositorioPickle("repo_estudiantes.pkl")
    registrar_estudiantes(repo_pickle)

    # Simulamos "reiniciar el programa": creamos repos nuevos y cargamos
    repo_json_2 = RepositorioJSON("repo_estudiantes.json")
    repo_json_2.cargar()
    print(f"Recargado desde JSON: {len(repo_json_2.listar())} estudiantes")
    for est in repo_json_2.listar():
        print(f"  {est}")

    repo_pickle_2 = RepositorioPickle("repo_estudiantes.pkl")
    repo_pickle_2.cargar()
    print(f"\nRecargado desde Pickle: {len(repo_pickle_2.listar())} estudiantes")
    for est in repo_pickle_2.listar():
        print(f"  {est}")

    print(
        "\nLa funcion registrar_estudiantes() es identica en ambos "
        "casos - solo cambia que instancia de repositorio le pasamos."
    )


if __name__ == "__main__":
    main()