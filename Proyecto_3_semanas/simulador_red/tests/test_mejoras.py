import unittest

from controllers.app_controller import AppController
from models.network_engine import Interfaz, Paquete, Router, Ruta


class VistaFalsa:
    """Vista de mentira: no dibuja nada."""

    def actualizar(self, router, anillo) -> None:
        pass


class PruebasMejoras(unittest.TestCase):

    def setUp(self):
        self.router = Router(capacidad_buffer=6)
        self.router.agregar_interfaz(Interfaz("eth0", 2))
        self.router.agregar_interfaz(Interfaz("eth1", 1))
        self.router.agregar_ruta(Ruta("LAN", "eth0"))
        self.router.agregar_ruta(Ruta("WAN", "eth0", 5))
        self.router.agregar_ruta(Ruta("WAN", "eth1", 2))
        self.controlador = AppController(self.router, VistaFalsa())

    def test_no_se_repiten_rutas(self):
        self.assertFalse(self.controlador.agregar_ruta("WAN", "eth1", 7))
        self.assertTrue(self.controlador.agregar_ruta("WAN2", "eth1", 3))
        self.assertTrue(self.router.existe_ruta("WAN2", "eth1"))

    def test_el_historial_dice_caer_o_levantar(self):
        self.controlador.alternar_interfaz("eth1")
        self.controlador.alternar_interfaz("eth1")
        textos = [str(a) for a in self.controlador.acciones_deshacer()]
        self.assertEqual(textos, ["Levantar eth1", "Caer eth1"])

    def test_estado_de_interfaz(self):
        self.assertTrue(self.router.interfaz_activa("eth0"))
        self.assertIsNone(self.router.interfaz_activa("eth9"))

    def test_la_metrica_elige_el_camino(self):
        self.router.recibir(Paquete("voz", destino="WAN"))
        salida = self.router.procesar_ciclo()
        self.assertEqual([p.salida for p in salida], ["eth1"])

    def test_si_cae_eth1_usa_eth0(self):
        self.controlador.alternar_interfaz("eth1")
        self.router.recibir(Paquete("voz", destino="WAN"))
        salida = self.router.procesar_ciclo()
        self.assertEqual([p.salida for p in salida], ["eth0"])

    def test_destino_desconocido_queda_sin_ruta(self):
        self.router.recibir(Paquete("datos", destino="Internet"))
        self.router.procesar_ciclo()
        self.assertEqual(self.router.sin_ruta, 1)


if __name__ == "__main__":
    unittest.main()
