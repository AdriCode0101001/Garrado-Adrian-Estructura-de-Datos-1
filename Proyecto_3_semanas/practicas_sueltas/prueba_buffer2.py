from models.colas import ColaCircular
from models.estructura_base import EstructuraLineal
from models.excepciones import BufferLlenoError, EstructuraVaciaError

buffer = ColaCircular(4)
for nombre in ("pkt1", "pkt2", "pkt3", "pkt4"):
    buffer.encolar(nombre)
print(buffer.desencolar())
print(buffer.desencolar())
print(buffer)
buffer.encolar("pkt5")
buffer.encolar("pkt6")
print(buffer)
try:
    buffer.encolar("pkt7")
except BufferLlenoError as error:
    print("Error:", error)
print(buffer.frente())
while not buffer.esta_vacia():
    print(buffer.desencolar())
print(buffer)
try:
    buffer.desencolar()
except EstructuraVaciaError as error:
    print("Error:", error)
print(isinstance(buffer, EstructuraLineal))
buffer.insertar("a")
print(buffer.eliminar())