from models.network_engine import Interfaz, Paquete, Router, Ruta


def simular(nombre: str, fifo: bool) -> None:
    router = Router(capacidad_buffer=6)
    if fifo:
        router.alternar_modo()
    router.agregar_interfaz(Interfaz("eth0", 2))
    router.agregar_ruta(Ruta("LAN", "eth0"))
    for tipo in ("datos", "datos", "video", "voz", "datos"):
        router.recibir(Paquete(tipo))
    print(f"===== {nombre} =====")
    for _ in range(3):
        enviados = router.procesar_ciclo()
        print(f"Ciclo {router.ciclo}:")
        for paquete in enviados:
            print(f"  salió: {paquete}")


simular("QoS", fifo=False)
simular("FIFO", fifo=True)