from models.estructura_base import EstructuraLineal
from models.excepciones import EstructuraVaciaError
from models.listas import ListaSimple

lista = ListaSimple()
for nombre in ("eth0", "eth1", "wlan0", "lo0"):
    lista.insertar_final(nombre)
print(lista)                          # eth0 -> eth1 -> wlan0 -> lo0 -> None
print(lista.eliminar_valor("eth1"))   # True   (intermedio)
print(lista)                          # eth0 -> wlan0 -> lo0 -> None
print(lista.eliminar_valor("eth0"))   # True   (cabeza)
print(lista)                          # wlan0 -> lo0 -> None
print(lista.eliminar_valor("lo0"))    # True   (último)
print(lista)                          # wlan0 -> None
print(lista.eliminar_valor("xx"))     # False  (no existe)
print(lista.eliminar())               # wlan0
print(lista.esta_vacia())             # True
try:
    lista.eliminar()
except EstructuraVaciaError as error:
    print("Error:", error)            # Error: La lista está vacía
print(isinstance(lista, EstructuraLineal))   # True