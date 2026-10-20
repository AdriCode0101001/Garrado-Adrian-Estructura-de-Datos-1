import flet as ft
import sys

from controllers.app_controller import AppController
from models.network_engine import Interfaz, Router, Ruta
from views.vista_principal import VistaPrincipal


def crear_router() -> Router:
    """Arma el router de ejemplo: dos interfaces y tres rutas."""
    router = Router(capacidad_buffer=6)
    router.agregar_interfaz(Interfaz("eth0", 2))
    router.agregar_interfaz(Interfaz("eth1", 1))
    router.agregar_ruta(Ruta("LAN", "eth0"))
    router.agregar_ruta(Ruta("WAN", "eth0", 5))
    router.agregar_ruta(Ruta("WAN", "eth1", 2))
    return router


def main(page: ft.Page) -> None:
    page.title = "Simulador de Red con QoS"
    controlador = AppController(crear_router())
    for nombre in ("PC1", "PC2", "PC3", "PC4"):
        controlador.agregar_equipo(nombre)
    vista = VistaPrincipal(page, controlador)
    controlador.conectar_vista(vista)


if __name__ == "__main__":
    if "--red" in sys.argv:
        ft.run(main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0",
               port=8550)
    elif "--web" in sys.argv:
        ft.run(main, view=ft.AppView.WEB_BROWSER, port=8550)
    else:
        ft.run(main)
