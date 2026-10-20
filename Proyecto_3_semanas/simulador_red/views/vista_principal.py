from typing import Any

import flet as ft

from views.anillo_visual import AnilloVisual
from views.componentes import (panel_buffer, panel_historial, panel_osi,
                               panel_paquetes, panel_tabla, seccion)
from views.panel_comparacion import panel_comparacion
from views.panel_metricas import panel_metricas

ANCHO_MOVIL = 700
RAFAGA = 10  # NUEVO 19B


def boton(texto: str, accion: Any, principal: bool = False) -> ft.Button:
    """Botón alto (48 px) para que sea cómodo de tocar con el dedo."""
    if principal:
        return ft.FilledButton(texto, on_click=lambda e: accion(),
                               height=48)
    return ft.Button(texto, on_click=lambda e: accion(), height=48)


class VistaPrincipal:
    """Pantalla principal: muestra el estado y reenvía las órdenes."""

    def __init__(self, page: ft.Page, controlador: Any) -> None:
        self.page: ft.Page = page
        self.controlador: Any = controlador
        self.page.scroll = ft.ScrollMode.AUTO
        self.interruptor = ft.Switch(
            label="Modo QoS (apagado = FIFO)",
            value=True,
            on_change=lambda e: self.controlador.alternar_modo(),
        )
        self.destino_paquete = ft.Dropdown(label="Destino del paquete",
                                           value="LAN", width=200)
        self.campo_destino = ft.TextField(
            label="Destino de la ruta", value="WAN2", width=170,
            helper="Red nueva o existente")
        self.interfaz = ft.Dropdown(label="Interfaz", value="eth0",
                                    width=130)
        self.campo_metrica = ft.TextField(label="Métrica", value="3",
                                          width=100)
        self.boton_deshacer = boton("Deshacer", self.controlador.deshacer)
        self.boton_rehacer = boton("Rehacer", self.controlador.rehacer)
        self.estado = ft.Text(size=16)
        self.colas = ft.Text(size=16)
        self.interfaces = ft.Text(size=16)
        self.anillo = ft.Text(size=16)
        self.aviso = ft.Text(size=16, color=ft.Colors.RED)
        self.panel_buffer = ft.Container()
        self.panel_cola = ft.Container()
        self.panel_salida = ft.Container()
        self.boton_osi = boton("Ver encapsulamiento paso a paso",
                               self._paso_osi)
        self.panel_osi = ft.Container()
        self.panel_metricas = ft.Container()
        self.panel_comparacion = ft.Container(
            content=panel_comparacion(None))
        self.panel_tabla = ft.Container()
        self.panel_historial = ft.Container()
        self.anillo_visual = AnilloVisual()
        self.paquete_osi: Any = None
        self.capas_visibles: Any = None
        self._armar()

    def _armar(self) -> None:
        """Coloca los controles en la página, agrupados en secciones."""
        trafico = ft.Row(
            [
                self.destino_paquete,
                boton("Enviar voz", lambda: self._enviar("voz")),
                boton("Enviar video", lambda: self._enviar("video")),
                boton("Enviar datos", lambda: self._enviar("datos")),
                boton("Siguiente ciclo", self._ciclo, principal=True),
                boton("Pasar token", self._pasar_token),
                boton(f"Congestión ({RAFAGA} paquetes)",  # NUEVO 19B
                      self._congestion),
            ],
            wrap=True,
        )
        configuracion = ft.Row(
            [
                self.campo_destino,
                self.interfaz,
                self.campo_metrica,
                boton("Agregar ruta", self._agregar_ruta),
                boton("Caer/levantar interfaz", self._alternar_interfaz),
                self.boton_deshacer,
                self.boton_rehacer,
            ],
            wrap=True,
        )
        self.grupo_controles = ft.Column([
            seccion("Controles", [
                trafico,
                self.interruptor,
                configuracion,
                self.aviso,
            ]),
            seccion("Estado", [
                self.estado,
                self.colas,
                self.interfaces,
                self.anillo,
            ]),
        ])
        self.grupo_trafico = ft.Container(
            content=seccion("Tráfico", [
                self.panel_buffer,
                self.panel_cola,
                self.panel_salida,
                self.panel_metricas,
                boton("Comparar FIFO vs QoS", self._comparar),
                self.panel_comparacion,
                self.boton_osi,
                self.panel_osi,
            ]),
            col={"sm": 12, "md": 6},
        )
        self.grupo_red = ft.Container(
            content=seccion("Red y configuración", [
                self.anillo_visual.control,
                boton("Pasar token", self._pasar_token),
                self.panel_tabla,
                self.panel_historial,
            ]),
            col={"sm": 12, "md": 6},
        )
        self.navegacion = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.DASHBOARD,
                                            label="Todo"),
                ft.NavigationBarDestination(icon=ft.Icons.TUNE,
                                            label="Controles"),
                ft.NavigationBarDestination(icon=ft.Icons.SWAP_HORIZ,
                                            label="Tráfico"),
                ft.NavigationBarDestination(icon=ft.Icons.HUB,
                                            label="Red"),
            ],
            selected_index=0,
            on_change=lambda e: self._mostrar(
                self.navegacion.selected_index),
        )
        self.page.navigation_bar = self.navegacion
        self.page.on_resize = lambda e: self._ajustar_ancho()
        self.page.add(
            ft.Text("Simulador de Red con QoS", size=24,
                    weight=ft.FontWeight.BOLD),
            self.grupo_controles,
            ft.ResponsiveRow([self.grupo_trafico, self.grupo_red]),
        )
        self._ajustar_ancho()

    def _mostrar(self, pestana: int) -> None:
        """Muestra todo (0) o solo una sección (1, 2 o 3)."""
        self.navegacion.selected_index = pestana
        self.grupo_controles.visible = pestana in (0, 1)
        self.grupo_trafico.visible = pestana in (0, 2)
        self.grupo_red.visible = pestana in (0, 3)
        self.page.update()

    def _ajustar_ancho(self) -> None:
        """En pantallas angostas, cambia de 'Todo' a una sola sección."""
        ancho = self.page.width or ANCHO_MOVIL
        if ancho < ANCHO_MOVIL and self.navegacion.selected_index == 0:
            self._mostrar(1)

    def _enviar(self, tipo: str) -> None:
        destino = self.destino_paquete.value or "LAN"
        recibido = self.controlador.enviar_paquete(tipo, destino)
        if recibido:
            self.aviso.value = ""
        else:
            self.aviso.value = "Buffer lleno: paquete descartado"
        self.page.update()

    def _congestion(self) -> None:  # NUEVO 19B
        """Manda una ráfaga de paquetes de golpe para llenar el buffer."""
        aceptados = self.controlador.simular_congestion(RAFAGA)
        perdidos = RAFAGA - aceptados
        self.aviso.value = (
            f"Congestión: entraron {aceptados} de {RAFAGA}; "
            f"{perdidos} descartados por buffer lleno"
        )
        self.page.update()

    def _ciclo(self) -> None:
        self.controlador.procesar_ciclo()

    def _pasar_token(self) -> None:
        self.controlador.avanzar_token()

    def _agregar_ruta(self) -> None:
        """Lee el formulario y pide al controlador agregar la ruta."""
        destino = (self.campo_destino.value or "").strip()
        metrica = (self.campo_metrica.value or "").strip()
        interfaz = self.interfaz.value or "eth0"
        if destino == "" or not metrica.isdigit() or int(metrica) < 1:
            self.aviso.value = "Escribe un destino y una métrica entera >= 1"
            self.page.update()
            return
        if not self.controlador.agregar_ruta(destino, interfaz,
                                             int(metrica)):
            self.aviso.value = f"Ya existe una ruta a {destino} por {interfaz}"
            self.page.update()

    def _alternar_interfaz(self) -> None:
        self.controlador.alternar_interfaz(self.interfaz.value or "eth0")

    def _comparar(self) -> None:
        """Pide la comparación al controlador y la muestra en la tabla."""
        comparacion = self.controlador.comparar_modos()
        self.panel_comparacion.content = panel_comparacion(comparacion)
        self.page.update()

    def _paso_osi(self) -> None:
        """Muestra una capa más de la pila OSI (solo es un efecto visual)."""
        if self.paquete_osi is None:
            return
        total = len(self.paquete_osi.capas)
        if self.capas_visibles is None or self.capas_visibles >= total:
            self.capas_visibles = 1
        else:
            self.capas_visibles += 1
        self.panel_osi.content = panel_osi(self.paquete_osi,
                                           self.capas_visibles)
        self.page.update()

    def _actualizar_opciones(self, router: Any) -> None:
        """Llena los menús con los destinos y las interfaces actuales."""
        destinos = []
        for ruta in router.tabla:
            if ruta.destino not in destinos:
                destinos.append(ruta.destino)
        destinos.append("Internet")
        self.destino_paquete.options = [
            ft.DropdownOption(d) for d in destinos]
        if self.destino_paquete.value not in destinos:
            self.destino_paquete.value = destinos[0]
        nombres = [i.nombre for i in router.interfaces]
        self.interfaz.options = [ft.DropdownOption(n) for n in nombres]

    def actualizar(self, router: Any, anillo: Any) -> None:
        """Redibuja la pantalla con el estado actual (solo lectura)."""
        self.aviso.value = ""
        self._actualizar_opciones(router)
        modo = "QoS" if router.modo_qos else "FIFO"
        self.interruptor.value = router.modo_qos
        self.estado.value = (
            f"Modo: {modo} | Ciclo: {router.ciclo} | "
            f"Enviados: {router.enviados} | "
            f"Descartados: {router.descartados} | "
            f"Sin ruta: {router.sin_ruta}"
        )
        self.colas.value = (
            f"En el buffer: {len(router.buffer)} | "
            f"En el clasificador: {len(router.clasificador)}"
        )
        puertos = ", ".join(str(i) for i in router.interfaces)
        self.interfaces.value = f"Interfaces: {puertos}"
        self.panel_buffer.content = panel_buffer(router.buffer)
        self.panel_cola.content = panel_paquetes(
            "Clasificador (sale primero el de la izquierda)",
            router.clasificador)
        self.panel_salida.content = panel_paquetes(
            "Salieron en el último ciclo", router.ultima_salida)
        self.panel_metricas.content = panel_metricas(router)
        ultimo = None
        for paquete in router.ultima_salida:
            ultimo = paquete
        self.paquete_osi = ultimo
        self.capas_visibles = None
        self.panel_osi.content = panel_osi(ultimo)
        self.panel_tabla.content = panel_tabla(router.tabla)
        self.panel_historial.content = panel_historial(
            self.controlador.acciones_deshacer(),
            self.controlador.acciones_rehacer())
        self.boton_deshacer.disabled = not self.controlador.puede_deshacer()
        self.boton_rehacer.disabled = not self.controlador.puede_rehacer()
        equipos = " ⟳ ".join(str(e) for e in anillo)
        dueno = self.controlador.token_actual()
        self.anillo_visual.actualizar(anillo, dueno)
        self.anillo.value = (
            f"Anillo: {equipos or 'vacío'} | "
            f"Token (envía): {dueno or 'nadie'}"
        )
        self.page.update()
