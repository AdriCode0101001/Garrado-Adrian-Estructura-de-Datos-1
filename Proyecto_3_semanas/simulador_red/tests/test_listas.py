import unittest

from models.excepciones import EstructuraVaciaError
from models.listas import ListaCircularDoble, ListaDoble, ListaSimple


class PruebasListaSimple(unittest.TestCase):

    def setUp(self):
        self.lista = ListaSimple()
        for nombre in ("a", "b", "c"):
            self.lista.insertar_final(nombre)

    def test_insertar_final_y_longitud(self):
        self.assertEqual(len(self.lista), 3)
        self.assertEqual(str(self.lista), "a -> b -> c -> None")

    def test_insertar_inicio(self):
        self.lista.insertar_inicio("z")
        self.assertEqual(str(self.lista), "z -> a -> b -> c -> None")

    def test_eliminar_devuelve_la_cabeza(self):
        self.assertEqual(self.lista.eliminar(), "a")
        self.assertEqual(len(self.lista), 2)

    def test_eliminar_en_lista_vacia(self):
        with self.assertRaises(EstructuraVaciaError):
            ListaSimple().eliminar()


class PruebasListaDoble(unittest.TestCase):

    def setUp(self):
        self.lista = ListaDoble()
        for nombre in ("a", "b", "c"):
            self.lista.insertar_final(nombre)

    def test_orden_normal(self):
        self.assertEqual(str(self.lista), "None <-> a <-> b <-> c <-> None")

    def test_eliminar_valor_del_medio(self):
        self.assertTrue(self.lista.eliminar_valor("b"))
        self.assertEqual(str(self.lista), "None <-> a <-> c <-> None")

    def test_eliminar_valor_inexistente(self):
        self.assertFalse(self.lista.eliminar_valor("x"))


class PruebasListaCircularDoble(unittest.TestCase):

    def setUp(self):
        self.anillo = ListaCircularDoble()
        for nombre in ("PC1", "PC2", "PC3"):
            self.anillo.insertar(nombre)

    def test_el_ultimo_apunta_al_primero(self):
        cabeza = self.anillo._cabeza
        self.assertEqual(cabeza.anterior.dato, "PC3")
        self.assertEqual(cabeza.anterior.siguiente.dato, "PC1")

    def test_token_da_la_vuelta(self):
        self.assertEqual(self.anillo.avanzar_token(), "PC2")
        self.assertEqual(self.anillo.avanzar_token(), "PC3")
        self.assertEqual(self.anillo.avanzar_token(), "PC1")

    def test_token_pasa_al_siguiente_si_el_actual_se_cae(self):
        self.anillo.avanzar_token()
        self.anillo.eliminar_valor("PC2")
        self.assertEqual(self.anillo.token(), "PC3")

    def test_anillo_vacio(self):
        with self.assertRaises(EstructuraVaciaError):
            ListaCircularDoble().avanzar_token()


if __name__ == "__main__":
    unittest.main()
