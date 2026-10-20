from typing import Any, Optional

from models.comparador import Comparacion
from models.listas import ListaCircularDoble, ListaSimple
from models.network_engine import Paquete, Router, Ruta
from models.pilas import Pila, UndoRedoManager


class AppController:
    """Mediador entre la vista y el modelo."""

    def __init__(self, router: Router, vista: Any = None,
                 anillo: Optional[ListaCircularDoble] = None) -> None:
        if anillo is None:
            anillo = ListaCircularDoble()
        self.router: Router = router
        self.vista: Any = vista
        self.anillo: ListaCircularDoble = anillo
        self.historial: UndoRedoManager = UndoRedoManager()

    def conectar_vista(self, vista: Any) -> None:
        """Registra la vista y la dibuja por primera vez."""
        self.vista = vista
        self.actualizar_vista()

    def actualizar_vista(self) -> None:
        """Le avisa a la vista que redibuje (si hay una conectada)."""
        if self.vista is not None:
            self.vista.actualizar(self.router, self.anillo)

    def enviar_paquete(self, tipo: str, destino: str = "LAN") -> bool:
        """La PC que tiene el token envía un paquete al router."""
        origen = self.token_actual()
        if origen is None:
            origen = "externo"
        paquete = Paquete(tipo, destino=destino, origen=origen)
        recibido = self.router.recibir(paquete)
        self.actualizar_vista()
        return recibido

    def procesar_ciclo(self) -> ListaSimple:
        """Ejecuta un ciclo del router y devuelve los paquetes enviados."""
        salida = self.router.procesar_ciclo()
        self.actualizar_vista()
        return salida

    def _aplicar(self, accion: Accion) -> bool:
        """Ejecuta una acción sobre el router. False si no se pudo."""
        if accion.tipo == "modo":
            self.router.alternar_modo()
            return True
        if accion.tipo == "ruta":
            self.router.agregar_ruta(accion.detalle)
            return True
        if accion.tipo == "interfaz":
            return self.router.alternar_interfaz(accion.detalle)
        return False

    def _revertir(self, accion: Accion) -> None:
        """Hace lo contrario de la acción."""
        if accion.tipo == "modo":
            self.router.alternar_modo()
        elif accion.tipo == "ruta":
            self.router.quitar_ruta(accion.detalle)
        elif accion.tipo == "interfaz":
            self.router.alternar_interfaz(accion.detalle)

    def _ejecutar(self, accion: Accion) -> bool:
        """Aplica un cambio nuevo, lo anota en el historial y redibuja."""
        if not self._aplicar(accion):
            return False
        self.historial.registrar(accion)
        self.actualizar_vista()
        return True

    def alternar_modo(self) -> bool:
        """Cambia entre QoS y FIFO."""
        return self._ejecutar(Accion("modo"))

    def agregar_ruta(self, destino: str, interfaz: str,
                     metrica: int = 1) -> bool:
        """Agrega una ruta. False si ya existe una igual."""
        if self.router.existe_ruta(destino, interfaz):
            return False
        ruta = Ruta(destino, interfaz, metrica)
        return self._ejecutar(Accion("ruta", ruta))

    def alternar_interfaz(self, nombre: str) -> bool:
        """Cae o levanta una interfaz y lo anota con el verbo correcto."""
        activa = self.router.interfaz_activa(nombre)
        if activa is None:
            return False
        verbo = "Caer" if activa else "Levantar"
        descripcion = f"{verbo} {nombre}"
        return self._ejecutar(Accion("interfaz", nombre, descripcion))

    def puede_deshacer(self) -> bool:
        return self.historial.puede_deshacer()

    def puede_rehacer(self) -> bool:
        return self.historial.puede_rehacer()

    def deshacer(self) -> bool:
        """Revierte la última acción. False si no hay nada que deshacer."""
        if not self.historial.puede_deshacer():
            return False
        self._revertir(self.historial.deshacer())
        self.actualizar_vista()
        return True

    def rehacer(self) -> bool:
        """Vuelve a aplicar la última acción deshecha."""
        if not self.historial.puede_rehacer():
            return False
        self._aplicar(self.historial.rehacer())
        self.actualizar_vista()
        return True

    def agregar_equipo(self, nombre: str) -> None:
        """Conecta un equipo al anillo."""
        self.anillo.insertar_final(nombre)
        self.actualizar_vista()

    def retirar_equipo(self, nombre: str) -> bool:
        """Desconecta un equipo del anillo. False si no estaba."""
        retirado = self.anillo.eliminar_valor(nombre)
        if retirado:
            self.actualizar_vista()
        return retirado

    def token_actual(self) -> Optional[Any]:
        """Dice qué equipo tiene el token (None si el anillo está vacío)."""
        if self.anillo.esta_vacia():
            return None
        return self.anillo.token()

    def avanzar_token(self) -> Optional[Any]:
        """Pasa el token al siguiente equipo y dice quién lo recibió."""
        if self.anillo.esta_vacia():
            return None
        dueno = self.anillo.avanzar_token()
        self.actualizar_vista()
        return dueno

    def acciones_deshacer(self) -> Pila:
        """Acciones que se pueden deshacer (la más reciente primero)."""
        return self.historial.pila_deshacer

    def acciones_rehacer(self) -> Pila:
        """Acciones que se pueden rehacer (la más reciente primero)."""
        return self.historial.pila_rehacer

    def comparar_modos(self) -> Comparacion:
        """Simula el mismo lote con QoS y con FIFO sin tocar el router."""
        return Comparacion(self.router)

    def simular_congestion(self, cantidad: int = 20) -> int:
        """Envía 'cantidad' paquetes de golpe; devuelve cuántos entraron."""
        tipos = ("datos", "video", "voz")
        aceptados = 0
        for numero in range(cantidad):
            if self.enviar_paquete(tipos[numero % 3]):
                aceptados += 1
        return aceptados


class Accion:
    """Un cambio de configuración que se puede deshacer y rehacer."""

    def __init__(self, tipo: str, detalle: Any = None,
                 descripcion: str = "") -> None:
        self.tipo: str = tipo
        self.detalle: Any = detalle
        self.descripcion: str = descripcion

    def __str__(self) -> str:
        if self.descripcion:
            return self.descripcion
        if self.tipo == "modo":
            return "Cambiar modo QoS/FIFO"
        if self.tipo == "ruta":
            return f"Agregar ruta {self.detalle}"
        if self.tipo == "interfaz":
            return f"Caer/levantar {self.detalle}"
        return self.tipo
