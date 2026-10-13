import unittest

from models.colas import ColaCircular, ColaPrioridad
from models.estructura_base import EstructuraLineal
from models.excepciones import BufferLlenoError, EstructuraVaciaError
from models.listas import ListaCircularDoble, ListaDoble, ListaSimple
from models.pilas import Pila, UndoRedoManager


class PruebasPila(unittest.TestCase):

    def test_sale_primero_el_ultimo_que_entro(self):
        pila = Pila()
        for numero in (1, 2, 3):
            pila.apilar(numero)
        self.assertEqual(pila.desapilar(), 3)
        self.assertEqual(pila.desapilar(), 2)
        self.assertEqual(pila.desapilar(), 1)
        self.assertTrue(pila.esta_vacia())

    def test_tope_no_elimina(self):
        pila = Pila()
        pila.apilar("x")
        self.assertEqual(pila.tope(), "x")
        self.assertEqual(len(pila), 1)

    def test_desapilar_en_pila_vacia(self):
        with self.assertRaises(EstructuraVaciaError):
            Pila().desapilar()

    def test_se_recorre_desde_el_tope(self):
        pila = Pila()
        for numero in (1, 2, 3):
            pila.apilar(numero)
        self.assertEqual(list(pila), [3, 2, 1])
        self.assertEqual(len(pila), 3)


class PruebasUndoRedo(unittest.TestCase):

    def setUp(self):
        self.gestor = UndoRedoManager()
        self.gestor.registrar("mover PC1")
        self.gestor.registrar("borrar enlace")

    def test_deshacer_devuelve_la_ultima_accion(self):
        self.assertEqual(self.gestor.deshacer(), "borrar enlace")
        self.assertEqual(self.gestor.deshacer(), "mover PC1")

    def test_rehacer_vuelve_a_aplicar(self):
        self.gestor.deshacer()
        self.assertTrue(self.gestor.puede_rehacer())
        self.assertEqual(self.gestor.rehacer(), "borrar enlace")

    def test_registrar_borra_el_rehacer(self):
        self.gestor.deshacer()
        self.gestor.registrar("accion nueva")
        self.assertFalse(self.gestor.puede_rehacer())

    def test_deshacer_sin_acciones(self):
        with self.assertRaises(EstructuraVaciaError):
            UndoRedoManager().deshacer()


class PruebasColaPrioridad(unittest.TestCase):

    def test_sale_el_mas_urgente(self):
        cola = ColaPrioridad()
        cola.encolar("datos", 1)
        cola.encolar("voz", 3)
        cola.encolar("video", 2)
        self.assertEqual(cola.desencolar(), "voz")
        self.assertEqual(cola.desencolar(), "video")
        self.assertEqual(cola.desencolar(), "datos")

    def test_en_empate_sale_el_primero_que_llego(self):
        cola = ColaPrioridad()
        cola.encolar("datos1", 1)
        cola.encolar("datos2", 1)
        self.assertEqual(cola.desencolar(), "datos1")
        self.assertEqual(cola.desencolar(), "datos2")

    def test_desencolar_en_cola_vacia(self):
        with self.assertRaises(EstructuraVaciaError):
            ColaPrioridad().desencolar()

    def test_se_recorre_en_orden_de_salida(self):
        cola = ColaPrioridad()
        cola.encolar("datos", 1)
        cola.encolar("voz", 3)
        cola.encolar("video", 2)
        self.assertEqual(list(cola), ["voz", "video", "datos"])
        self.assertEqual(len(cola), 3)


class PruebasColaCircular(unittest.TestCase):

    def test_sale_primero_el_que_llego_primero(self):
        buffer = ColaCircular(3)
        for nombre in ("a", "b", "c"):
            buffer.encolar(nombre)
        self.assertEqual(buffer.desencolar(), "a")
        self.assertEqual(buffer.desencolar(), "b")

    def test_reutiliza_las_celdas_liberadas(self):
        buffer = ColaCircular(3)
        for nombre in ("a", "b", "c"):
            buffer.encolar(nombre)
        buffer.desencolar()
        buffer.encolar("d")
        self.assertTrue(buffer.esta_llena())
        self.assertEqual(buffer.desencolar(), "b")
        self.assertEqual(buffer.desencolar(), "c")
        self.assertEqual(buffer.desencolar(), "d")

    def test_encolar_en_buffer_lleno(self):
        buffer = ColaCircular(1)
        buffer.encolar("a")
        with self.assertRaises(BufferLlenoError):
            buffer.encolar("b")

    def test_desencolar_en_buffer_vacio(self):
        with self.assertRaises(EstructuraVaciaError):
            ColaCircular(2).desencolar()

    def test_capacidad_invalida(self):
        with self.assertRaises(ValueError):
            ColaCircular(0)

    def test_lectura_para_la_vista(self):
        buffer = ColaCircular(3)
        buffer.encolar("a")
        buffer.encolar("b")
        buffer.desencolar()
        self.assertEqual(buffer.capacidad, 3)
        self.assertEqual(buffer.indice_frente, 1)
        self.assertEqual(buffer.indice_fondo, 2)
        self.assertIsNone(buffer.celda(0))
        self.assertEqual(buffer.celda(1), "b")
        with self.assertRaises(AttributeError):
            buffer.capacidad = 10


class PruebasContrato(unittest.TestCase):

    def test_todas_cumplen_estructura_lineal(self):
        estructuras = (
            ListaSimple(), ListaDoble(), ListaCircularDoble(),
            Pila(), ColaPrioridad(), ColaCircular(2),
        )
        for estructura in estructuras:
            self.assertIsInstance(estructura, EstructuraLineal)


if __name__ == "__main__":
    unittest.main()
