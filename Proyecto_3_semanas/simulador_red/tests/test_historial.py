import unittest

from controllers.app_controller import Accion, AppController
from models.network_engine import Interfaz, Router, Ruta
from models.pilas import UndoRedoManager


class VistaFalsa:
    """Vista de mentira: no dibuja nada."""

    def actualizar(self, router, anillo) -> None:
        pass


class PruebasHistorial(unittest.TestCase):

    def setUp(self):
        router = Router(capacidad_buffer=4)
        router.agregar_interfaz(Interfaz("eth0", 2))
        router.agregar_ruta(Ruta("LAN", "eth0"))
        self.controlador = AppController(router, VistaFalsa())

    def test_las_pilas_del_gestor_se_pueden_leer(self):
        gestor = UndoRedoManager()
        gestor.registrar("a")
        gestor.registrar("b")
        self.assertEqual(list(gestor.pila_deshacer), ["b", "a"])
        self.assertEqual(len(gestor.pila_rehacer), 0)

    def test_el_controlador_entrega_el_historial(self):
        self.controlador.agregar_ruta("WAN", "eth0", 5)
        self.controlador.alternar_modo()
        textos = [str(a) for a in self.controlador.acciones_deshacer()]
        self.assertEqual(textos[0], "Cambiar modo QoS/FIFO")
        self.assertEqual(textos[1], "Agregar ruta WAN -> eth0 (métrica 5)")
        self.controlador.deshacer()
        textos = [str(a) for a in self.controlador.acciones_rehacer()]
        self.assertEqual(textos, ["Cambiar modo QoS/FIFO"])

    def test_texto_de_cada_accion(self):
        accion = Accion("interfaz", "eth0")
        self.assertEqual(str(accion), "Caer/levantar eth0")


if __name__ == "__main__":
    unittest.main()
