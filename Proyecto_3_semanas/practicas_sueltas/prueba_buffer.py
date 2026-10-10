from models.colas import ColaCircular
from models.excepciones import BufferLlenoError

buffer = ColaCircular(4)
print(buffer)
buffer.encolar("pkt1")
buffer.encolar("pkt2")
print(buffer)
buffer.encolar("pkt3")
buffer.encolar("pkt4")
print(buffer)
print(buffer.esta_llena(), len(buffer))
try:
    buffer.encolar("pkt5")
except BufferLlenoError as error:
    print("Error:", error)