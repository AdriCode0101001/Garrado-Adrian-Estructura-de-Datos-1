from models.colas import ColaPrioridad

cola = ColaPrioridad()
print(cola)
cola.encolar("descarga1", 1)
cola.encolar("video1", 2)
cola.encolar("voz1", 3)
print(cola)
cola.encolar("descarga2", 1)
cola.encolar("voz2", 3)
cola.encolar("video2", 2)
print(cola)
print(len(cola), cola.esta_vacia())