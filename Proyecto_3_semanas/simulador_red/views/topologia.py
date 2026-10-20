import asyncio
from typing import Any

import flet as ft
import flet.canvas as cv

from views.componentes import color_de

ANCHO = 860
ALTO = 400
PC_X = 80
ROUTER_X = 400
ROUTER_Y = 160
ROUTER_R = 46
PUERTO_X = ROUTER_X + 80
NUBE_X = 760
NUBE = 90
SOBRE = 28
VIAJE_MS = 700
SEPARACION = 0.4
MAX_EVENTOS = 8


def y_repartida(indice: int, total: int) -> float:
    """Reparte 'total' elementos de arriba hacia abajo en el lienzo."""
    arriba, abajo = 50, ALTO - 60
    if total <= 1:
        return (arriba + abajo) / 2
    return arriba + indice * (abajo - arriba) / (total - 1)


def linea(x1: float, y1: float, x2: float, y2: float, color: Any,
          ancho: float = 2, punteada: bool = False) -> cv.Line:
    """Un cable entre dos puntos del lienzo."""
    pintura = ft.Paint(color=color, stroke_width=ancho,
                       style=ft.PaintingStyle.STROKE)
    if punteada:
        pintura.stroke_dash_pattern = [6, 6]
    return cv.Line(x1, y1, x2, y2, paint=pintura)


def luz(x: float, y: float, activa: bool) -> ft.Container:
    """Luz de enlace: verde si funciona, roja si está caído."""
    color = ft.Colors.GREEN_400 if activa else ft.Colors.RED_400
    return ft.Container(width=10, height=10, border_radius=5,
                        bgcolor=color, left=x - 5, top=y - 5)


class Topologia:
    """Dibujo de la red al estilo Packet Tracer: PCs, router y nubes."""

    def __init__(self) -> None:
        self.lienzo = ft.Stack(width=ANCHO, height=ALTO)
        self.pos_pc: dict = {}
        self.pos_puerto: dict = {}
        self.pos_nube: dict = {}
        self.viajeros: list = []
        self.eventos = ft.Column(spacing=2)
        self.control = ft.Column(
            [
                ft.Text("Como en Packet Tracer: cada sobre es un paquete "
                        "que viaja PC → Router → interfaz → red destino",
                        size=13),
                ft.Row([self.lienzo], scroll=ft.ScrollMode.AUTO),
                self._leyenda(),
                ft.Text("Eventos (como la Event List de Packet Tracer)",
                        size=16, weight=ft.FontWeight.BOLD),
                self._fila_evento("Ciclo", None, "Paquete", "De", "A",
                                  "Resultado", encabezado=True),
                self.eventos,
            ],
            spacing=6,
        )

    def _leyenda(self) -> ft.Row:
        """Explica los colores de los sobres."""
        fila = ft.Row(wrap=True, spacing=16)
        for tipo, prioridad in (("voz", 3), ("video", 2), ("datos", 1)):
            fila.controls.append(ft.Row([
                ft.Icon(ft.Icons.EMAIL, color=color_de(tipo), size=20),
                ft.Text(f"{tipo} ({prioridad})", size=13),
            ], spacing=4, tight=True))
        fila.controls.append(ft.Row([
            ft.Container(width=10, height=10, border_radius=5,
                         bgcolor=ft.Colors.GREEN_400),
            ft.Text("enlace activo", size=13),
        ], spacing=4, tight=True))
        return fila

    def _pc(self, nombre: str, x: float, y: float,
            tiene_token: bool) -> ft.Container:
        """Ícono de computadora; resaltado si tiene el token."""
        texto = f"{nombre} 🔑" if tiene_token else nombre
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.DESKTOP_WINDOWS, size=40,
                            color=ft.Colors.LIGHT_BLUE_300),
                    ft.Text(texto, size=13, weight=ft.FontWeight.BOLD),
                ],
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=90, padding=4, border_radius=10,
            bgcolor=ft.Colors.AMBER_900 if tiene_token else None,
            border=(ft.Border.all(3, ft.Colors.AMBER_400)
                    if tiene_token else None),
            left=x - 45, top=y - 34,
        )

    def _router(self) -> ft.Container:
        """Router redondo con cuatro flechas, como en Packet Tracer."""
        return ft.Container(
            content=ft.Icon(ft.Icons.OPEN_WITH, size=52,
                            color=ft.Colors.WHITE),
            width=2 * ROUTER_R, height=2 * ROUTER_R,
            border_radius=ROUTER_R, bgcolor=ft.Colors.BLUE_800,
            border=ft.Border.all(3, ft.Colors.BLUE_200),
            alignment=ft.Alignment.CENTER,
            left=ROUTER_X - ROUTER_R, top=ROUTER_Y - ROUTER_R,
        )

    def _estado_router(self, router: Any) -> ft.Container:
        """Debajo del router: celdas del buffer y orden del clasificador."""
        celdas = ft.Row(spacing=3)
        for i in range(router.buffer.capacidad):
            paquete = router.buffer.celda(i)
            celdas.controls.append(ft.Container(
                width=18, height=14, border_radius=3,
                bgcolor=color_de(paquete.tipo) if paquete else None,
                border=ft.Border.all(1, ft.Colors.OUTLINE),
            ))
        cola = ft.Row(spacing=2)
        for paquete in router.clasificador:
            cola.controls.append(ft.Icon(ft.Icons.EMAIL, size=18,
                                         color=color_de(paquete.tipo)))
        lleno = len(router.buffer)
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Router", size=15, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Buffer {lleno}/{router.buffer.capacidad}",
                            size=11),
                    celdas,
                    ft.Text("Clasificador (sale primero ←)", size=11),
                    cola,
                ],
                spacing=3,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=170,
            left=ROUTER_X - 85, top=ROUTER_Y + ROUTER_R + 4,
        )

    def _nube(self, nombre: str, x: float, y: float,
              alcanzable: bool) -> ft.Container:
        """Nube de red destino; apagada si no hay ruta hacia ella."""
        color = (ft.Colors.BLUE_GREY_700 if alcanzable
                 else ft.Colors.with_opacity(0.3, ft.Colors.BLUE_GREY_700))
        texto = nombre if alcanzable else f"{nombre} ?"
        return ft.Container(
            content=ft.Stack([
                ft.Icon(ft.Icons.CLOUD, size=NUBE, color=color),
                ft.Container(
                    content=ft.Text(texto, size=14,
                                    weight=ft.FontWeight.BOLD),
                    width=NUBE, height=NUBE,
                    alignment=ft.Alignment(0, 0.25),
                ),
            ]),
            width=NUBE, height=NUBE,
            left=x - NUBE / 2, top=y - NUBE / 2,
        )

    def _etiqueta(self, texto: str, x: float, y: float,
                  color: Any) -> ft.Text:
        """Texto pequeño en una posición del lienzo."""
        return ft.Text(texto, size=12, weight=ft.FontWeight.BOLD,
                       color=color, left=x, top=y)

    def actualizar(self, router: Any, anillo: Any, dueno: Any) -> None:
        """Redibuja la topología con el estado actual del router."""
        cables = []
        nodos = []
        # PCs del anillo, en columna a la izquierda
        nombres = [str(equipo) for equipo in anillo]
        self.pos_pc = {}
        for i, nombre in enumerate(nombres):
            y = y_repartida(i, len(nombres))
            self.pos_pc[nombre] = (PC_X + 45, y)
            cables.append(linea(PC_X + 45, y, ROUTER_X - ROUTER_R,
                                ROUTER_Y, ft.Colors.GREY_500))
            nodos.append(luz(PC_X + 52, y, True))
            nodos.append(self._pc(nombre, PC_X, y, nombre == dueno))
        # Puertos del router (una interfaz debajo de la otra)
        interfaces = [interfaz for interfaz in router.interfaces]
        self.pos_puerto = {}
        for i, interfaz in enumerate(interfaces):
            y = ROUTER_Y - 30 + i * 60
            self.pos_puerto[interfaz.nombre] = (PUERTO_X, y)
            color = (ft.Colors.GREEN_300 if interfaz.activa
                     else ft.Colors.RED_300)
            cables.append(linea(ROUTER_X, ROUTER_Y, PUERTO_X, y,
                                ft.Colors.GREY_500, 3))
            nodos.append(luz(PUERTO_X, y, interfaz.activa))
            nodos.append(self._etiqueta(interfaz.nombre, PUERTO_X - 10,
                                        y - 24, color))
        # Nubes: un destino por cada red de la tabla, más Internet
        destinos = []
        for ruta in router.tabla:
            if ruta.destino not in destinos:
                destinos.append(ruta.destino)
        sin_ruta = "Internet" not in destinos
        if sin_ruta:
            destinos.append("Internet")
        self.pos_nube = {}
        for i, destino in enumerate(destinos):
            y = y_repartida(i, len(destinos))
            self.pos_nube[destino] = (NUBE_X, y)
            alcanzable = not (sin_ruta and destino == "Internet")
            nodos.append(self._nube(destino, NUBE_X, y, alcanzable))
        # Un cable por cada ruta: puerto de la interfaz -> nube
        activas = {i.nombre: i.activa for i in interfaces}
        for ruta in router.tabla:
            px, py = self.pos_puerto[ruta.interfaz]
            nx, ny = self.pos_nube[ruta.destino]
            activa = activas.get(ruta.interfaz, False)
            cables.append(linea(px, py, nx - NUBE / 2, ny,
                                ft.Colors.GREY_400 if activa
                                else ft.Colors.RED_300,
                                2, punteada=not activa))
            nodos.append(luz(nx - NUBE / 2 - 6, ny, activa))
        if sin_ruta:
            nx, ny = self.pos_nube["Internet"]
            cables.append(linea(ROUTER_X, ROUTER_Y + ROUTER_R,
                                nx - NUBE / 2, ny, ft.Colors.GREY_700,
                                1, punteada=True))
        lienzo_cables = cv.Canvas(shapes=cables, width=ANCHO, height=ALTO,
                                  left=0, top=0)
        self.lienzo.controls = ([lienzo_cables] + nodos
                                + [self._router(),
                                   self._estado_router(router)]
                                + self.viajeros)

    def _sobre(self, tipo: str, x: float, y: float) -> ft.Container:
        """Un paquete dibujado como sobre; se desliza al cambiar left/top."""
        return ft.Container(
            content=ft.Icon(ft.Icons.EMAIL, size=SOBRE,
                            color=color_de(tipo)),
            left=x - SOBRE / 2, top=y - SOBRE / 2,
            animate_position=ft.Animation(
                VIAJE_MS, ft.AnimationCurve.EASE_IN_OUT),
            animate_opacity=300,
        )

    async def _mover(self, sobre: ft.Container, x: float, y: float) -> None:
        """Desliza el sobre hasta (x, y) y espera a que llegue."""
        sobre.left = x - SOBRE / 2
        sobre.top = y - SOBRE / 2
        self.lienzo.update()
        await asyncio.sleep(VIAJE_MS / 1000 + 0.05)

    async def _quitar(self, sobre: ft.Container) -> None:
        """Desvanece el sobre y lo saca del lienzo."""
        sobre.opacity = 0
        self.lienzo.update()
        await asyncio.sleep(0.35)
        if sobre in self.viajeros:
            self.viajeros.remove(sobre)
        if sobre in self.lienzo.controls:
            self.lienzo.controls.remove(sobre)
        self.lienzo.update()

    def _agregar(self, sobre: ft.Container) -> None:
        """Pone un sobre nuevo en el lienzo y lo recuerda como viajero."""
        self.viajeros.append(sobre)
        self.lienzo.controls.append(sobre)
        self.lienzo.update()

    def _fila_evento(self, ciclo: str, tipo: Any, paquete: str, de: str,
                     a: str, resultado: str, encabezado: bool = False,
                     error: bool = False) -> ft.Row:
        """Una fila de la lista de eventos (o su encabezado)."""
        peso = ft.FontWeight.BOLD if encabezado else None
        color = ft.Colors.RED_300 if error else None
        icono = (ft.Icon(ft.Icons.EMAIL, size=16, color=color_de(tipo))
                 if tipo else ft.Container(width=16))
        return ft.Row(
            [
                ft.Text(ciclo, width=50, size=13, weight=peso),
                ft.Row([icono, ft.Text(paquete, size=13, weight=peso)],
                       width=120, spacing=4),
                ft.Text(de, width=70, size=13, weight=peso),
                ft.Text(a, width=80, size=13, weight=peso),
                ft.Text(resultado, size=13, weight=peso, color=color),
            ],
            spacing=8,
        )

    def registrar_evento(self, ciclo: int, tipo: str, paquete: str,
                         de: str, a: str, resultado: str,
                         error: bool = False) -> None:
        """Agrega un evento arriba de la lista (los más nuevos primero)."""
        fila = self._fila_evento(str(ciclo), tipo, paquete, de, a,
                                 resultado, error=error)
        self.eventos.controls.insert(0, fila)
        del self.eventos.controls[MAX_EVENTOS:]
        self.eventos.update()

    async def animar_envio(self, origen: str, tipo: str, entro: bool,
                           ciclo: int, espera: float = 0) -> None:
        """Paso T2: el sobre viaja de la PC al router."""
        await asyncio.sleep(espera)
        x, y = self.pos_pc.get(origen, (0, ROUTER_Y))
        sobre = self._sobre(tipo, x, y)
        self._agregar(sobre)
        await asyncio.sleep(0.05)
        await self._mover(sobre, ROUTER_X - ROUTER_R - 14, ROUTER_Y)
        if entro:
            self.registrar_evento(ciclo, tipo, tipo, origen, "Router",
                                  "entró al buffer")
        else:
            sobre.content = ft.Icon(ft.Icons.CANCEL, size=SOBRE,
                                    color=ft.Colors.RED_ACCENT_400)
            self.lienzo.update()
            self.registrar_evento(ciclo, tipo, tipo, origen, "Router",
                                  "descartado: buffer lleno", error=True)
            await asyncio.sleep(0.6)
        await self._quitar(sobre)

    # ---------- T3: salida de los paquetes en cada ciclo ----------

    async def _viaje_salida(self, espera: float, ident: int, tipo: str,
                            interfaz: str, destino: str,
                            ciclo: int) -> None:
        """Un sobre sale del router, pasa por su interfaz y llega a la red."""
        await asyncio.sleep(espera)
        sobre = self._sobre(tipo, ROUTER_X, ROUTER_Y)
        self._agregar(sobre)
        await asyncio.sleep(0.05)
        px, py = self.pos_puerto.get(interfaz, (PUERTO_X, ROUTER_Y))
        await self._mover(sobre, px, py)
        nx, ny = self.pos_nube.get(destino, (NUBE_X, ROUTER_Y))
        await self._mover(sobre, nx - NUBE / 2 + 12, ny)
        self.registrar_evento(ciclo, tipo, f"#{ident} {tipo}", "Router",
                              destino, f"salió por {interfaz}")
        await self._quitar(sobre)

    async def _viaje_sin_ruta(self, espera: float, ciclo: int) -> None:
        """Un paquete sin ruta: intenta salir hacia Internet y se pierde."""
        await asyncio.sleep(espera)
        sobre = ft.Container(
            content=ft.Icon(ft.Icons.HELP, size=SOBRE,
                            color=ft.Colors.GREY_400),
            left=ROUTER_X - SOBRE / 2, top=ROUTER_Y + ROUTER_R,
            animate_position=ft.Animation(
                VIAJE_MS, ft.AnimationCurve.EASE_IN_OUT),
            animate_opacity=300,
        )
        self._agregar(sobre)
        await asyncio.sleep(0.05)
        await self._mover(sobre, ROUTER_X + 120, ROUTER_Y + ROUTER_R + 60)
        self.registrar_evento(ciclo, None, "?", "Router", "Internet",
                              "sin ruta: descartado", error=True)
        await self._quitar(sobre)

    async def animar_ciclo(self, viajes: list, perdidos: int,
                           ciclo: int) -> None:
        """Paso T3: anima, en orden de salida, los paquetes del ciclo."""
        tareas = []
        for orden, (ident, tipo, interfaz, destino) in enumerate(viajes):
            tareas.append(self._viaje_salida(orden * SEPARACION, ident,
                                             tipo, interfaz, destino,
                                             ciclo))
        for extra in range(perdidos):
            tareas.append(self._viaje_sin_ruta(
                (len(viajes) + extra) * SEPARACION, ciclo))
        await asyncio.gather(*tareas)
