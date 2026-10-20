from typing import Optional

from models.listas import ListaSimple
from models.network_engine import Interfaz, Paquete, Router, Ruta

LIMITE_CICLOS = 100


def lote_de_prueba() -> ListaSimple:
    """El mismo lote para los dos modos: lo urgente llega al final."""
    lote = ListaSimple()
    for tipo in ("datos", "datos", "video", "datos", "voz", "voz"):
        lote.insertar_final(tipo)
    return lote


def copiar_router(original: Router) -> Router:
    """Router nuevo y vacío con la misma configuración que el original."""
    copia = Router(capacidad_buffer=original.buffer.capacidad)
    for interfaz in original.interfaces:
        nueva = Interfaz(interfaz.nombre, interfaz.capacidad)
        if not interfaz.activa:
            nueva.caer()
        copia.agregar_interfaz(nueva)
    for ruta in original.tabla:
        copia.agregar_ruta(Ruta(ruta.destino, ruta.interfaz, ruta.metrica))
    return copia


def simular(original: Router, lote: ListaSimple, qos: bool) -> Router:
    """Procesa el lote en una copia del router hasta vaciarlo."""
    router = copiar_router(original)
    if router.modo_qos != qos:
        router.alternar_modo()
    for tipo in lote:
        router.recibir(Paquete(tipo))
    while (len(router.buffer) + len(router.clasificador) > 0
           and router.ciclo < LIMITE_CICLOS):
        router.procesar_ciclo()
    return router


class Comparacion:
    """Resultado de procesar el mismo lote con QoS y con FIFO."""

    def __init__(self, original: Router,
                 lote: Optional[ListaSimple] = None) -> None:
        if lote is None:
            lote = lote_de_prueba()
        self.lote: ListaSimple = lote
        self.qos: Router = simular(original, lote, True)
        self.fifo: Router = simular(original, lote, False)
