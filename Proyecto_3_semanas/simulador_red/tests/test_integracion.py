import unittest

from controllers.app_controller import AppController
from models.network_engine import Interfaz, Router, Ruta


class VistaFalsa:
    """Vista de mentira: cuenta cuántas veces se le pide redibujar."""

    def __init__(self) -> None:
        self.llamadas = 0

    def actualizar(self, router, anillo) -> None:
        self.llamadas += 1


class PruebasIntegracion(unittest.TestCase):
    """Historias completas, igual que en la app (como en main.py)."""

    def setUp(self):
        self.router = Router(capacidad_buffer=6)
        self.router.agregar_interfaz(Interfaz("eth0", 2))
        self.router.agregar_interfaz(Interfaz("eth1", 1))
        self.router.agregar_ruta(Ruta("LAN", "eth0"))
        self.router.agregar_ruta(Ruta("WAN", "eth0", 5))
        self.router.agregar_ruta(Ruta("WAN", "eth1", 2))
        self.vista = VistaFalsa()
        self.c = AppController(self.router, self.vista)

    def test_pcs_envian_y_el_router_ordena(self):
        for nombre in ("PC1", "PC2", "PC3", "PC4"):
            self.c.agregar_equipo(nombre)
        self.c.enviar_paquete("datos")
        self.c.enviar_paquete("voz", "WAN")
        self.c.avanzar_token()
        self.c.enviar_paquete("video")
        salida = self.c.procesar_ciclo()
        resumen = [(p.tipo, p.origen, p.salida) for p in salida]
        self.assertEqual(resumen, [
            ("voz", "PC1", "eth1"),
            ("video", "PC2", "eth0"),
            ("datos", "PC1", "eth0"),
        ])
        self.assertGreater(self.vista.llamadas, 0)

    def test_failover_y_deshacer(self):
        self.c.alternar_interfaz("eth1")
        self.c.enviar_paquete("voz", "WAN")
        salida = self.c.procesar_ciclo()
        self.assertEqual([p.salida for p in salida], ["eth0"])
        self.assertTrue(self.c.deshacer())
        self.assertTrue(self.router.interfaz_activa("eth1"))
        textos = [str(a) for a in self.c.acciones_rehacer()]
        self.assertEqual(textos, ["Caer eth1"])

    def test_buffer_lleno_y_destino_sin_ruta(self):
        for _ in range(6):
            self.assertTrue(self.c.enviar_paquete("datos"))
        self.assertFalse(self.c.enviar_paquete("datos"))
        self.assertEqual(self.router.descartados, 1)
        self.c.procesar_ciclo()
        self.c.enviar_paquete("voz", "Internet")
        self.c.procesar_ciclo()
        self.assertEqual(self.router.sin_ruta, 1)

    def test_fifo_respeta_el_orden_de_llegada(self):
        self.c.alternar_modo()
        self.c.enviar_paquete("datos")
        self.c.enviar_paquete("voz")
        salida = self.c.procesar_ciclo()
        self.assertEqual([p.tipo for p in salida], ["datos", "voz"])


if __name__ == "__main__":
    unittest.main()
