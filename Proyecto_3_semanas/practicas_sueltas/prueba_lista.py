from models.listas import ListaSimple

lista = ListaSimple()
print(lista)                            # None
lista.insertar_inicio("eth0")
print(lista)                            # eth0 -> None
lista.insertar_inicio("eth1")
lista.insertar_inicio("wlan0")
print(lista)                            # wlan0 -> eth1 -> eth0 -> None
print(len(lista), lista.esta_vacia())   # 3 False


lista2 = ListaSimple()
lista2.insertar_final("eth0")
lista2.insertar_final("eth1")
lista2.insertar_final("wlan0")
print(lista2)                   # eth0 -> eth1 -> wlan0 -> None
print(lista2.buscar("eth1"))    # True
print(lista2.buscar("lo0"))     # False
print(len(lista2))              # 3