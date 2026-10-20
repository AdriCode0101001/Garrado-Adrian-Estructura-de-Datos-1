import unittest

from models.metricas import Estadistica, Metricas
from models.network_engine import Interfaz, Paquete, Router, Ruta


class PruebasMetricas(unittest.TestCase):

    def crear_router(self):
        router = Router(capacidad_buffer=6)
        router.agregar_interfaz(Interfaz("eth0", 2))
        router.agregar_ruta(Ruta("LAN", "eth0"))
        for tipo in ("datos", "datos", "video", "voz"):
            router.recibir(Paquete(tipo))
        return router

    def test_promedio_sin_paquetes_es_cero(self):
        self.assertEqual(Estadistica().promedio(), 0.0)

    def test_promedio(self):
        estadistica = Estadistica()
        estadistica.registrar(0)
        estadistica.registrar(2)
        self.assertEqual(estadistica.promedio(), 1.0)

    def test_metricas_separa_por_tipo(self):
        metricas = Metricas()
        metricas.registrar(Paquete("voz"))
        metricas.registrar(Paquete("datos"))
        self.assertEqual(metricas.voz.enviados, 1)
        self.assertEqual(metricas.datos.enviados, 1)
        self.assertEqual(metricas.video.enviados, 0)

    def test_con_qos_la_voz_no_espera(self):
        router = self.crear_router()
        router.procesar_ciclo()
        router.procesar_ciclo()
        self.assertEqual(router.metricas.voz.promedio(), 0.0)
        self.assertEqual(router.metricas.datos.promedio(), 1.0)

    def test_con_fifo_la_voz_espera(self):
        router = self.crear_router()
        router.alternar_modo()
        router.procesar_ciclo()
        router.procesar_ciclo()
        self.assertEqual(router.metricas.voz.promedio(), 1.0)
        self.assertEqual(router.metricas.datos.promedio(), 0.0)


if __name__ == "__main__":
    unittest.main()
