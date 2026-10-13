import unittest

from models.network_engine import Interfaz, Paquete, Router, Ruta


class PruebasPaquete(unittest.TestCase):

    def test_prioridades_por_tipo(self):
        self.assertEqual(Paquete("voz").prioridad, 3)
        self.assertEqual(Paquete("video").prioridad, 2)
        self.assertEqual(Paquete("datos").prioridad, 1)

    def test_tipo_invalido(self):
        with self.assertRaises(ValueError):
            Paquete("correo")

    def test_ids_crecen(self):
        primero = Paquete("voz")
        segundo = Paquete("datos")
        self.assertEqual(segundo.id, primero.id + 1)

    def test_esperar_suma_ciclos(self):
        paquete = Paquete("video")
        paquete.esperar()
        paquete.esperar()
        self.assertEqual(paquete.ciclos_esperados, 2)

    def test_str(self):
        paquete = Paquete("voz", 100)
        esperado = f"#{paquete.id} voz(p3, 100B, espera=0)"
        self.assertEqual(str(paquete), esperado)

    def test_destino(self):
        self.assertEqual(Paquete("voz").destino, "LAN")
        self.assertEqual(Paquete("voz", destino="WAN").destino, "WAN")

    def test_pila_osi(self):
        paquete = Paquete("voz", destino="WAN")
        capas = list(paquete.capas)
        self.assertEqual(len(paquete.capas), 7)
        self.assertEqual(paquete.capas.tope(), "1 Física: bits por el cable")
        self.assertEqual(capas[-1], "7 Aplicación: voz")
        self.assertIn("3 Red: IP destino WAN", capas)
        self.assertIn("4 Transporte: UDP", capas)

    def test_datos_usan_tcp(self):
        self.assertIn("4 Transporte: TCP", list(Paquete("datos").capas))


class PruebasInterfaz(unittest.TestCase):

    def test_valores_por_defecto(self):
        interfaz = Interfaz("eth0")
        self.assertEqual(interfaz.capacidad, 2)
        self.assertTrue(interfaz.activa)

    def test_capacidad_invalida(self):
        with self.assertRaises(ValueError):
            Interfaz("eth0", 0)

    def test_caer_y_levantar(self):
        interfaz = Interfaz("eth0")
        interfaz.caer()
        self.assertFalse(interfaz.activa)
        interfaz.levantar()
        self.assertTrue(interfaz.activa)

    def test_str(self):
        interfaz = Interfaz("eth0", 3)
        self.assertEqual(str(interfaz), "eth0(cap=3, activa)")
        interfaz.caer()
        self.assertEqual(str(interfaz), "eth0(cap=3, caída)")


class PruebasRuta(unittest.TestCase):

    def test_datos_de_la_ruta(self):
        ruta = Ruta("10.0.0.0/24", "eth0", 5)
        self.assertEqual(ruta.destino, "10.0.0.0/24")
        self.assertEqual(ruta.interfaz, "eth0")
        self.assertEqual(ruta.metrica, 5)

    def test_metrica_por_defecto(self):
        self.assertEqual(Ruta("10.0.0.0/24", "eth0").metrica, 1)

    def test_str(self):
        ruta = Ruta("10.0.0.0/24", "eth0", 5)
        self.assertEqual(str(ruta), "10.0.0.0/24 -> eth0 (métrica 5)")


class PruebasRouter(unittest.TestCase):

    def setUp(self):
        self.router = Router(capacidad_buffer=4)
        self.router.agregar_interfaz(Interfaz("eth0", 2))
        self.router.agregar_ruta(Ruta("LAN", "eth0"))

    def cargar_trafico(self):
        for tipo in ("datos", "datos", "video", "voz"):
            self.router.recibir(Paquete(tipo))

    def test_buffer_lleno_descarta(self):
        for _ in range(4):
            self.assertTrue(self.router.recibir(Paquete("datos")))
        self.assertFalse(self.router.recibir(Paquete("datos")))
        self.assertEqual(self.router.descartados, 1)

    def test_qos_envia_primero_la_voz(self):
        self.cargar_trafico()
        salida = self.router.procesar_ciclo()
        self.assertEqual([p.tipo for p in salida], ["voz", "video"])
        self.assertEqual(len(self.router.clasificador), 2)
        self.assertEqual(self.router.ciclo, 1)

    def test_fifo_respeta_el_orden_de_llegada(self):
        self.router.alternar_modo()
        self.cargar_trafico()
        salida = self.router.procesar_ciclo()
        self.assertEqual([p.tipo for p in salida], ["datos", "datos"])

    def test_los_que_esperan_suman_ciclos(self):
        self.cargar_trafico()
        self.router.procesar_ciclo()
        segundo = self.router.procesar_ciclo()
        self.assertEqual(len(segundo), 2)
        for paquete in segundo:
            self.assertEqual(paquete.ciclos_esperados, 1)

    def test_paquete_sin_ruta(self):
        self.router.recibir(Paquete("voz", destino="WAN"))
        salida = self.router.procesar_ciclo()
        self.assertEqual(len(salida), 0)
        self.assertEqual(self.router.sin_ruta, 1)

    def test_interfaz_caida_deja_esperando(self):
        for interfaz in self.router.interfaces:
            interfaz.caer()
        self.router.recibir(Paquete("voz"))
        salida = self.router.procesar_ciclo()
        self.assertEqual(len(salida), 0)
        self.assertEqual(len(self.router.clasificador), 1)

    def test_buscar_ruta_elige_la_menor_metrica(self):
        eth1 = Interfaz("eth1")
        self.router.agregar_interfaz(eth1)
        self.router.agregar_ruta(Ruta("WAN", "eth0", 5))
        self.router.agregar_ruta(Ruta("WAN", "eth1", 2))
        self.assertEqual(self.router.buscar_ruta("WAN").interfaz, "eth1")
        eth1.caer()
        self.assertEqual(self.router.buscar_ruta("WAN").interfaz, "eth0")


if __name__ == "__main__":
    unittest.main()
