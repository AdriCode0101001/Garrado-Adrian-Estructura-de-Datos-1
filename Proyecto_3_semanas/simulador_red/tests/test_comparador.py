import unittest

from models.comparador import Comparacion, copiar_router, lote_de_prueba
from models.network_engine import Interfaz, Router, Ruta


class PruebasComparador(unittest.TestCase):

    def crear_router(self):
        router = Router(capacidad_buffer=6)
        router.agregar_interfaz(Interfaz("eth0", 3))
        router.agregar_ruta(Ruta("LAN", "eth0"))
        return router

    def test_lote_tiene_seis_paquetes(self):
        self.assertEqual(len(lote_de_prueba()), 6)

    def test_copia_tiene_la_misma_configuracion(self):
        original = self.crear_router()
        copia = copiar_router(original)
        self.assertIsNot(copia, original)
        self.assertEqual(len(copia.interfaces), 1)
        self.assertEqual(len(copia.tabla), 1)

    def test_no_modifica_el_router_real(self):
        original = self.crear_router()
        Comparacion(original)
        self.assertEqual(original.ciclo, 0)
        self.assertEqual(original.enviados, 0)
        self.assertEqual(len(original.buffer), 0)

    def test_los_dos_modos_envian_todo(self):
        comparacion = Comparacion(self.crear_router())
        self.assertEqual(comparacion.qos.enviados, 6)
        self.assertEqual(comparacion.fifo.enviados, 6)

    def test_qos_la_voz_no_espera(self):
        metricas = Comparacion(self.crear_router()).qos.metricas
        self.assertEqual(metricas.voz.promedio(), 0.0)
        self.assertEqual(metricas.datos.promedio(), 1.0)

    def test_fifo_la_voz_espera(self):
        metricas = Comparacion(self.crear_router()).fifo.metricas
        self.assertEqual(metricas.voz.promedio(), 1.0)
        self.assertAlmostEqual(metricas.datos.promedio(), 1 / 3)


if __name__ == "__main__":
    unittest.main()
