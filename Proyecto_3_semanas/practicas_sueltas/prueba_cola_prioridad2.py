from models.colas import ColaPrioridad
from models.estructura_base import EstructuraLineal
from models.excepciones import EstructuraVaciaError

cola = ColaPrioridad()
cola.encolar("descarga1", 1)
cola.encolar("video1", 2)
cola.encolar("voz1", 3)
cola.encolar("descarga2", 1)
cola.encolar("voz2", 3)
cola.encolar("video2", 2)
print(cola.frente())
print(cola.desencolar())
print(cola.desencolar())
print(cola.desencolar())
print(cola.desencolar())
print(cola)
print(len(cola))

iguales = ColaPrioridad()
iguales.encolar("pkt1", 2)
iguales.encolar("pkt2", 2)
iguales.encolar("pkt3", 2)
print(iguales.desencolar(), iguales.desencolar(), iguales.desencolar())

print(cola.desencolar(), cola.desencolar())
print(cola.esta_vacia())
try:
    cola.desencolar()
except EstructuraVaciaError as error:
    print("Error:", error)
cola.insertar("paquete")
print(cola)
print(cola.eliminar())
print(isinstance(cola, EstructuraLineal))