import math
from typing import Any

import flet as ft

TAMANO = 300
CENTRO = TAMANO / 2
RADIO = 110
NODO = 64
FICHA = 22


def posicion(indice: int, total: int, radio: float) -> tuple:
    """Coordenadas (x, y) del punto número indice repartido en un círculo."""
    angulo = -math.pi / 2 + 2 * math.pi * indice / total
    return (CENTRO + radio * math.cos(angulo),
            CENTRO + radio * math.sin(angulo))


class AnilloVisual:
    """Dibuja el anillo Token Ring: PCs en círculo y una ficha que viaja."""

    def __init__(self) -> None:
        self.circulo = ft.Container(
            width=2 * RADIO, height=2 * RADIO, border_radius=RADIO,
            border=ft.Border.all(2, ft.Colors.OUTLINE),
            left=CENTRO - RADIO, top=CENTRO - RADIO,
        )
        self.ficha = ft.Container(
            width=FICHA, height=FICHA, border_radius=FICHA / 2,
            bgcolor=ft.Colors.AMBER_400,
            left=CENTRO - FICHA / 2, top=CENTRO - FICHA / 2,
            animate_position=ft.Animation(
                500, ft.AnimationCurve.EASE_IN_OUT),
        )
        self.lienzo = ft.Stack(width=TAMANO, height=TAMANO)
        self.leyenda = ft.Text(size=14)
        self.control = ft.Column(
            [
                ft.Text("Anillo Token Ring (ListaCircularDoble)", size=18,
                        weight=ft.FontWeight.BOLD),
                self.lienzo,
                self.leyenda,
            ],
            spacing=6,
        )

    def _nodo(self, nombre: str, x: float, y: float,
              tiene_token: bool) -> ft.Container:
        """Un círculo con el nombre de la PC; resaltado si tiene el token."""
        if tiene_token:
            fondo = ft.Colors.AMBER_700
            borde = ft.Border.all(3, ft.Colors.AMBER_300)
        else:
            fondo = ft.Colors.BLUE_GREY_800
            borde = ft.Border.all(1, ft.Colors.OUTLINE)
        return ft.Container(
            content=ft.Text(nombre, size=14, weight=ft.FontWeight.BOLD),
            width=NODO, height=NODO, border_radius=NODO / 2,
            alignment=ft.Alignment.CENTER,
            bgcolor=fondo, border=borde,
            left=x - NODO / 2, top=y - NODO / 2,
        )

    def actualizar(self, anillo: Any, dueno: Any) -> None:
        """Redibuja las PCs y mueve la ficha hasta la que tiene el token."""
        nombres = [str(equipo) for equipo in anillo]
        total = len(nombres)
        nodos = []
        for indice, nombre in enumerate(nombres):
            x, y = posicion(indice, total, RADIO)
            tiene_token = nombre == dueno
            nodos.append(self._nodo(nombre, x, y, tiene_token))
            if tiene_token:
                fx, fy = posicion(indice, total, RADIO - 52)
                self.ficha.left = fx - FICHA / 2
                self.ficha.top = fy - FICHA / 2
        self.ficha.visible = dueno is not None
        self.lienzo.controls = [self.circulo] + nodos + [self.ficha]
        if dueno is None:
            self.leyenda.value = "Anillo vacío: nadie puede transmitir."
        else:
            self.leyenda.value = (f"Token en {dueno}: solo {dueno} puede "
                                  "transmitir; las demás esperan su turno.")
