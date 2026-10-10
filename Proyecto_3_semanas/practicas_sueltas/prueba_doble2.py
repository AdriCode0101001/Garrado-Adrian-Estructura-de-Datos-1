from models.estructura_base import EstructuraLineal
from models.excepciones import EstructuraVaciaError
from models.listas import ListaDoble

lista = ListaDoble()
for nombre in ("eth0", "eth1", "wlan0", "lo0"):
    lista.insertar(nombre)
print(lista)                           # None <-> eth0 <-> eth1 <-> wlan0 <-> lo0 <-> None
print(lista.eliminar_valor("eth1"))    # True   (intermedio)
print(lista)                           # None <-> eth0 <-> wlan0 <-> lo0 <-> None
print(lista.mostrar_inverso())         # None <-> lo0 <-> wlan0 <-> eth0 <-> None
print(lista.eliminar_valor("eth0"))    # True   (cabeza)
print(lista)                           # None <-> wlan0 <-> lo0 <-> None
print(lista.eliminar_valor("lo0"))     # True   (cola)
print(lista)                           # None <-> wlan0 <-> None
print(lista.mostrar_inverso())         # None <-> wlan0 <-> None
print(lista.eliminar_valor("xx"))      # False
print(lista.eliminar())                # wlan0
print(lista.esta_vacia())              # True
try:
    lista.eliminar()
except EstructuraVaciaError as error:
    print("Error:", error)             # Error: La lista está vacía
print(isinstance(lista, EstructuraLineal))   # True 