import unittest

from controllers.app_controller import AppController
from models.network_engine import Interfaz, Router, Ruta


class VistaFalsa:
    """Vista de mentira: solo cuenta cuántas veces debe redibujar."""

    def __init__(self) -> None:
        self.llamadas = 0

    def actualizar(self, router, anillo) -> None:
        self.llamadas += 1


class PruebasControlador(unittest.TestCase):

    def setUp(self):
        router = Router(capacidad_buffer=4)
        router.agregar_interfaz(Interfaz("eth0", 2))
        router.agregar_ruta(Ruta("LAN", "eth0"))
        self.vista = VistaFalsa()
        self.controlador = AppController(router, self.vista)

    def test_enviar_paquete_avisa_a_la_vista(self):
        self.assertTrue(self.controlador.enviar_paquete("voz"))
        self.assertEqual(len(self.controlador.router.buffer), 1)
        self.assertEqual(self.vista.llamadas, 1)

    def test_buffer_lleno_devuelve_false(self):
        for _ in range(4):
            self.controlador.enviar_paquete("datos")
        self.assertFalse(self.controlador.enviar_paquete("datos"))

    def test_procesar_ciclo_envia_y_avisa(self):
        self.controlador.enviar_paquete("voz")
        salida = self.controlador.procesar_ciclo()
        self.assertEqual(len(salida), 1)
        self.assertEqual(self.vista.llamadas, 2)

    def test_alternar_modo(self):
        self.assertTrue(self.controlador.router.modo_qos)
        self.controlador.alternar_modo()
        self.assertFalse(self.controlador.router.modo_qos)

    def test_funciona_sin_vista(self):
        controlador = AppController(self.controlador.router)
        self.assertTrue(controlador.enviar_paquete("datos"))

    def test_deshacer_y_rehacer_el_modo(self):
        self.controlador.alternar_modo()
        self.assertFalse(self.controlador.router.modo_qos)
        self.assertTrue(self.controlador.deshacer())
        self.assertTrue(self.controlador.router.modo_qos)
        self.assertTrue(self.controlador.rehacer())
        self.assertFalse(self.controlador.router.modo_qos)

    def test_deshacer_agregar_ruta(self):
        self.controlador.agregar_ruta("WAN", "eth0", 3)
        self.assertIsNotNone(self.controlador.router.buscar_ruta("WAN"))
        self.controlador.deshacer()
        self.assertIsNone(self.controlador.router.buscar_ruta("WAN"))
        self.controlador.rehacer()
        self.assertIsNotNone(self.controlador.router.buscar_ruta("WAN"))

    def test_alternar_interfaz_y_deshacer(self):
        self.controlador.alternar_interfaz("eth0")
        self.assertIsNone(self.controlador.router.buscar_ruta("LAN"))
        self.controlador.deshacer()
        self.assertIsNotNone(self.controlador.router.buscar_ruta("LAN"))

    def test_interfaz_inexistente_no_se_registra(self):
        self.assertFalse(self.controlador.alternar_interfaz("eth9"))
        self.assertFalse(self.controlador.puede_deshacer())

    def test_deshacer_sin_historial(self):
        self.assertFalse(self.controlador.deshacer())
        self.assertFalse(self.controlador.rehacer())

    def test_una_accion_nueva_borra_el_rehacer(self):
        self.controlador.alternar_modo()
        self.controlador.deshacer()
        self.assertTrue(self.controlador.puede_rehacer())
        self.controlador.alternar_modo()
        self.assertFalse(self.controlador.puede_rehacer())

    def test_token_recorre_el_anillo(self):
        for nombre in ("PC1", "PC2", "PC3"):
            self.controlador.agregar_equipo(nombre)
        self.assertEqual(self.controlador.token_actual(), "PC1")
        self.assertEqual(self.controlador.avanzar_token(), "PC2")
        self.assertEqual(self.controlador.avanzar_token(), "PC3")
        self.assertEqual(self.controlador.avanzar_token(), "PC1")

    def test_anillo_vacio_no_rompe(self):
        self.assertIsNone(self.controlador.avanzar_token())
        self.assertIsNone(self.controlador.token_actual())

    def test_retirar_al_que_tiene_el_token(self):
        for nombre in ("PC1", "PC2", "PC3"):
            self.controlador.agregar_equipo(nombre)
        self.assertTrue(self.controlador.retirar_equipo("PC1"))
        self.assertEqual(self.controlador.token_actual(), "PC2")
        self.assertFalse(self.controlador.retirar_equipo("PCX"))

    def test_avanzar_token_avisa_a_la_vista(self):
        self.controlador.agregar_equipo("PC1")
        self.controlador.agregar_equipo("PC2")
        antes = self.vista.llamadas
        self.controlador.avanzar_token()
        self.assertEqual(self.vista.llamadas, antes + 1)

    def test_flujo_completo(self):
        for tipo in ("datos", "voz", "video"):
            self.controlador.enviar_paquete(tipo)
        salida = self.controlador.procesar_ciclo()
        self.assertEqual([p.tipo for p in salida], ["voz", "video"])
        self.controlador.alternar_modo()
        self.controlador.deshacer()
        self.assertTrue(self.controlador.router.modo_qos)


if __name__ == "__main__":
    unittest.main()
