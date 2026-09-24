"""Desafio - Unidad 3: Mini sistema de turnos.

Combina una Cola (atencion en orden de llegada) con una Tabla Hash
(busqueda rapida de un turno por su codigo), y ofrece persistencia
opcional en JSON al finalizar la sesion.
"""

import json
from collections import deque
from pathlib import Path
from typing import Any


class SistemaTurnos:
    def __init__(self):
        self._cola_espera: deque = deque()  # orden de atencion (FIFO)
        self._indice_por_codigo: dict[str, dict] = {}  # busqueda O(1) por codigo
        self._siguiente_numero = 1

    def generar_turno(self, nombre_cliente: str) -> str:
        """Crea un turno nuevo, lo pone al final de la cola de espera,
        y lo indexa en la tabla hash para busqueda rapida.
        """
        codigo = f"T{self._siguiente_numero:03d}"
        self._siguiente_numero += 1

        turno = {"codigo": codigo, "cliente": nombre_cliente, "estado": "esperando"}
        self._cola_espera.append(codigo)
        self._indice_por_codigo[codigo] = turno
        return codigo

    def atender_siguiente(self) -> dict | None:
        """Saca el proximo turno de la cola (FIFO) y lo marca atendido."""
        if not self._cola_espera:
            return None
        codigo = self._cola_espera.popleft()
        turno = self._indice_por_codigo[codigo]
        turno["estado"] = "atendido"
        return turno

    def buscar_por_codigo(self, codigo: str) -> dict | None:
        """Busqueda O(1) gracias a la tabla hash (el dict de Python)."""
        return self._indice_por_codigo.get(codigo)

    def turnos_en_espera(self) -> list[str]:
        return list(self._cola_espera)

    def guardar(self, archivo: str) -> None:
        datos = {
            "siguiente_numero": self._siguiente_numero,
            "cola_espera": list(self._cola_espera),
            "turnos": self._indice_por_codigo,
        }
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)

    def cargar(self, archivo: str) -> None:
        if not Path(archivo).exists():
            return
        with open(archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
        self._siguiente_numero = datos["siguiente_numero"]
        self._cola_espera = deque(datos["cola_espera"])
        self._indice_por_codigo = datos["turnos"]


def main():
    sistema = SistemaTurnos()

    c1 = sistema.generar_turno("Ana")
    c2 = sistema.generar_turno("Luis")
    c3 = sistema.generar_turno("Carla")
    print(f"Turnos generados: {c1}, {c2}, {c3}")
    print(f"En espera: {sistema.turnos_en_espera()}")

    print(f"\nbuscar_por_codigo('{c2}'): {sistema.buscar_por_codigo(c2)}")

    print("\n--- Atendiendo turnos (orden FIFO) ---")
    atendido = sistema.atender_siguiente()
    print(f"Atendido: {atendido}  (deberia ser Ana, la primera en llegar)")
    print(f"En espera ahora: {sistema.turnos_en_espera()}")

    print(f"\nbuscar_por_codigo('{c1}') despues de atendido: {sistema.buscar_por_codigo(c1)}")
    print("(sigue en el indice, solo cambio su estado - no se borro el registro)")

    print("\n--- Persistencia ---")
    sistema.guardar("turnos.json")
    print("Guardado en turnos.json")

    sistema_recargado = SistemaTurnos()
    sistema_recargado.cargar("turnos.json")
    print(f"Recargado - en espera: {sistema_recargado.turnos_en_espera()}")
    print(f"Recargado - buscar('{c3}'): {sistema_recargado.buscar_por_codigo(c3)}")


if __name__ == "__main__":
    main()
