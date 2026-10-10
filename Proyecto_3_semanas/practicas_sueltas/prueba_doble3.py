from models.excepciones import EstructuraVaciaError
from models.listas import ListaDoble

lista = ListaDoble()
try:
    lista.avanzar()
except EstructuraVaciaError as error:
    print("Error:", error)          # Error: La lista está vacía

for ruta in ("ruta1", "ruta2", "ruta3"):
    lista.insertar(ruta)

print(lista.avanzar())              # ruta1  (primer llamado: se posiciona en la cabeza)
print(lista.avanzar())              # ruta2
print(lista.avanzar())              # ruta3
print(lista.avanzar())              # ruta3  (ya es el último: no se pasa)
print(lista.retroceder())           # ruta2
print(lista.retroceder())           # ruta1
print(lista.retroceder())           # ruta1  (ya es el primero: no se pasa)

lista.avanzar()                     # cursor en ruta2
lista.avanzar()                     # cursor en ruta3 (la cola)
lista.eliminar_valor("ruta3")       # eliminamos justo el nodo donde está el cursor
print(lista)                        # None <-> ruta1 <-> ruta2 <-> None
print(lista.avanzar())              # ruta2