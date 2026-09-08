"""Ejercicio 1 - Unidad 0: Refactor de estilo segun PEP 8.

Version corregida de una lista enlazada simple, aplicando
convenciones de nombres, espaciado y estructura de PEP 8.
"""

TAMANO_MAXIMO = 20


class ListaEnlazada:
    """Lista enlazada simple con insercion al inicio y busqueda."""

    def __init__(self):
        """Inicializa la lista vacia."""
        self.cabeza = None
        self.tamano = 0

    def insertar(self, dato):
        """Inserta un dato al inicio de la lista.

        Args:
            dato: El valor a insertar.
        """
        nodo = self.Nodo(dato)
        nodo.siguiente = self.cabeza
        self.cabeza = nodo
        self.tamano = self.tamano + 1

    def buscar_elemento(self, valor_buscado):
        """Busca un elemento en la lista.

        Args:
            valor_buscado: El valor a buscar.

        Returns:
            True si el elemento existe, False en caso contrario.
        """
        actual = self.cabeza
        while actual is not None:
            if actual.dato == valor_buscado:
                return True
            actual = actual.siguiente
        return False

    class Nodo:
        """Nodo interno de la lista enlazada."""

        def __init__(self, dato):
            """Inicializa el nodo con un dato y sin enlace siguiente.

            Args:
                dato: El valor que almacena este nodo.
            """
            self.dato = dato
            self.siguiente = None


def calcular_promedio(lista):
    """Calcula el promedio de una lista de numeros.

    Args:
        lista: Lista de numeros.

    Returns:
        El promedio de los elementos de la lista.
    """
    suma = 0
    for numero in lista:
        suma = suma + numero
    return suma / len(lista)