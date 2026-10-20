from typing import Optional

from models.colas import ColaCircular, ColaPrioridad
from models.excepciones import BufferLlenoError
from models.listas import ListaDoble, ListaSimple
from models.pilas import Pila
from models.metricas import Metricas


def prioridad_de(tipo: str) -> int:
    """Devuelve la prioridad QoS de un tipo de tráfico."""
    if tipo == "voz":
        return 3
    if tipo == "video":
        return 2
    if tipo == "datos":
        return 1
    raise ValueError(f"Tipo de tráfico desconocido: {tipo}")


class Paquete:
    """Unidad de información que viaja por la red."""

    _contador: int = 0

    def __init__(self, tipo: str, tamano: int = 64,
                 destino: str = "LAN", origen: str = "") -> None:
        self.prioridad: int = prioridad_de(tipo)
        Paquete._contador += 1
        self.id: int = Paquete._contador
        self.tipo: str = tipo
        self.tamano: int = tamano
        self.destino: str = destino
        self.origen: str = origen
        self.salida: str = ""
        self.ciclos_esperados: int = 0
        self.capas: Pila = Pila()
        self._encapsular()

    def _encapsular(self) -> None:
        """Arma la pila OSI: Aplicación queda al fondo y Física en el tope."""
        transporte = "TCP" if self.tipo == "datos" else "UDP"
        self.capas.apilar(f"7 Aplicación: {self.tipo}")
        self.capas.apilar("6 Presentación: codificación")
        self.capas.apilar("5 Sesión: conversación abierta")
        self.capas.apilar(f"4 Transporte: {transporte}")
        self.capas.apilar(f"3 Red: IP destino {self.destino}")
        self.capas.apilar("2 Enlace: trama Ethernet")
        self.capas.apilar("1 Física: bits por el cable")

    def esperar(self) -> None:
        """Suma un ciclo de espera (no pudo salir en este ciclo)."""
        self.ciclos_esperados += 1

    def __str__(self) -> str:
        return (f"#{self.id} {self.tipo}(p{self.prioridad}, "
                f"{self.tamano}B, espera={self.ciclos_esperados})")


class Interfaz:
    """Puerto del router por donde salen los paquetes."""

    def __init__(self, nombre: str, capacidad: int = 2) -> None:
        if capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor que cero")
        self.nombre: str = nombre
        self.capacidad: int = capacidad
        self.activa: bool = True

    def caer(self) -> None:
        """Simula una falla del enlace."""
        self.activa = False

    def levantar(self) -> None:
        """Restablece el enlace."""
        self.activa = True

    def __str__(self) -> str:
        estado = "activa" if self.activa else "caída"
        return f"{self.nombre}(cap={self.capacidad}, {estado})"


class Ruta:
    """Entrada de la tabla de enrutamiento: destino y puerto de salida."""

    def __init__(self, destino: str, interfaz: str, metrica: int = 1) -> None:
        self.destino: str = destino
        self.interfaz: str = interfaz
        self.metrica: int = metrica

    def __str__(self) -> str:
        return f"{self.destino} -> {self.interfaz} (métrica {self.metrica})"


class Router:
    """Router con QoS: une buffer, clasificador, tabla e interfaces."""

    def __init__(self, capacidad_buffer: int = 8) -> None:
        self.buffer: ColaCircular = ColaCircular(capacidad_buffer)
        self.clasificador: ColaPrioridad = ColaPrioridad()
        self.tabla: ListaDoble = ListaDoble()
        self.interfaces: ListaSimple = ListaSimple()
        self.modo_qos: bool = True
        self.ciclo: int = 0
        self.enviados: int = 0
        self.descartados: int = 0
        self.sin_ruta: int = 0
        self.ultima_salida: ListaSimple = ListaSimple()
        self.metricas: Metricas = Metricas()

    def agregar_interfaz(self, interfaz: Interfaz) -> None:
        """Conecta un puerto al router."""
        self.interfaces.insertar_final(interfaz)

    def agregar_ruta(self, ruta: Ruta) -> None:
        """Agrega una ruta a la tabla de enrutamiento."""
        self.tabla.insertar_final(ruta)

    def quitar_ruta(self, ruta: Ruta) -> bool:
        """Quita una ruta de la tabla. Devuelve si existía."""
        return self.tabla.eliminar_valor(ruta)

    def alternar_interfaz(self, nombre: str) -> bool:
        """Cae o levanta una interfaz. Devuelve si la encontró."""
        interfaz = self._buscar_interfaz(nombre)
        if interfaz is None:
            return False
        if interfaz.activa:
            interfaz.caer()
        else:
            interfaz.levantar()
        return True

    def existe_ruta(self, destino: str, interfaz: str) -> bool:
        """Indica si ya hay una ruta a ese destino por esa interfaz."""
        for ruta in self.tabla:
            if ruta.destino == destino and ruta.interfaz == interfaz:
                return True
        return False

    def interfaz_activa(self, nombre: str) -> Optional[bool]:
        """Estado de una interfaz: True/False, o None si no existe."""
        interfaz = self._buscar_interfaz(nombre)
        if interfaz is None:
            return None
        return interfaz.activa

    def alternar_modo(self) -> None:
        """Cambia entre QoS y FIFO."""
        self.modo_qos = not self.modo_qos

    def recibir(self, paquete: Paquete) -> bool:
        """Mete un paquete al buffer. Devuelve False si se descartó."""
        try:
            self.buffer.encolar(paquete)
        except BufferLlenoError:
            self.descartados += 1
            return False
        return True

    def _buscar_interfaz(self, nombre: str) -> Optional[Interfaz]:
        for interfaz in self.interfaces:
            if interfaz.nombre == nombre:
                return interfaz
        return None

    def buscar_ruta(self, destino: str) -> Optional[Ruta]:
        """Mejor ruta activa (menor métrica) hacia el destino."""
        mejor = None
        for ruta in self.tabla:
            if ruta.destino != destino:
                continue
            interfaz = self._buscar_interfaz(ruta.interfaz)
            if interfaz is None or not interfaz.activa:
                continue
            if mejor is None or ruta.metrica < mejor.metrica:
                mejor = ruta
        return mejor

    def _capacidad_por_ciclo(self) -> int:
        total = 0
        for interfaz in self.interfaces:
            if interfaz.activa:
                total += interfaz.capacidad
        return total

    def _clasificar(self) -> None:
        """Pasa todo el buffer al clasificador, según el modo."""
        while not self.buffer.esta_vacia():
            paquete = self.buffer.desencolar()
            prioridad = paquete.prioridad if self.modo_qos else 1
            self.clasificador.encolar(paquete, prioridad)

    def _despachar(self) -> ListaSimple:
        """Envía paquetes mientras haya cupo. Devuelve los enviados."""
        salida = ListaSimple()
        cupo = self._capacidad_por_ciclo()
        while cupo > 0 and not self.clasificador.esta_vacia():
            paquete = self.clasificador.desencolar()
            ruta = self.buscar_ruta(paquete.destino)
            if ruta is None:
                self.sin_ruta += 1
                continue
            paquete.salida = ruta.interfaz
            salida.insertar_final(paquete)
            self.enviados += 1
            self.metricas.registrar(paquete)
            cupo -= 1
        return salida

    def _envejecer(self) -> None:
        """Suma un ciclo de espera a los paquetes que no salieron."""
        for paquete in self.clasificador:
            paquete.esperar()

    def procesar_ciclo(self) -> ListaSimple:
        """Ejecuta un ciclo: clasifica, despacha y envejece a los demás."""
        self.ciclo += 1
        self._clasificar()
        salida = self._despachar()
        self._envejecer()
        self.ultima_salida = salida
        return salida
