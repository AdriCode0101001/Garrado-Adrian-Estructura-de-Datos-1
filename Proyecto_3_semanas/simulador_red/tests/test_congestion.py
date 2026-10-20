import unittest

from controllers.app_controller import AppController
from models.network_engine import Interfaz, Router, Ruta


class PruebasCongestion(unittest.TestCase):

    def crear_controlador(self):
        router = Router(capacidad_buffer=6)
        router.agregar_interfaz(Interfaz("eth0", 2))
        router.agregar_ruta(Ruta("LAN", "eth0"))
        return AppController(router)

    def test_solo_entran_los_que_caben(self):
        controlador = self.crear_controlador()
        self.assertEqual(controlador.simular_congestion(20), 6)
        self.assertEqual(controlador.router.descartados, 14)
        self.assertEqual(len(controlador.router.buffer), 6)

    def test_sin_congestion_no_hay_descartes(self):
        controlador = self.crear_controlador()
        self.assertEqual(controlador.simular_congestion(4), 4)
        self.assertEqual(controlador.router.descartados, 0)

    def test_mezcla_los_tres_tipos(self):
        controlador = self.crear_controlador()
        controlador.simular_congestion(3)
        buffer = controlador.router.buffer
        self.assertEqual(buffer.desencolar().tipo, "datos")
        self.assertEqual(buffer.desencolar().tipo, "video")
        self.assertEqual(buffer.desencolar().tipo, "voz")


if __name__ == "__main__":
    unittest.main()
