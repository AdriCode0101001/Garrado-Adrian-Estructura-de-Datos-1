import unittest

from controllers.app_controller import AppController
from models.network_engine import Interfaz, Paquete, Router, Ruta


class VistaFalsa:
    """Vista de mentira: no dibuja nada."""

    def actualizar(self, router, anillo) -> None:
        pass


class PruebasToken(unittest.TestCase):

    def setUp(self):
        router = Router(capacidad_buffer=4)
        router.agregar_interfaz(Interfaz("eth0", 2))
        router.agregar_ruta(Ruta("LAN", "eth0"))
        self.controlador = AppController(router, VistaFalsa())

    def test_origen(self):
        self.assertEqual(Paquete("voz").origen, "")
        self.assertEqual(Paquete("voz", origen="PC3").origen, "PC3")

    def test_el_paquete_sale_de_la_pc_con_el_token(self):
        for nombre in ("PC1", "PC2"):
            self.controlador.agregar_equipo(nombre)
        self.controlador.enviar_paquete("voz")
        self.controlador.avanzar_token()
        self.controlador.enviar_paquete("datos")
        salida = self.controlador.procesar_ciclo()
        self.assertEqual([p.origen for p in salida], ["PC1", "PC2"])

    def test_sin_anillo_el_origen_es_externo(self):
        self.controlador.enviar_paquete("voz")
        salida = self.controlador.procesar_ciclo()
        self.assertEqual([p.origen for p in salida], ["externo"])


if __name__ == "__main__":
    unittest.main()
