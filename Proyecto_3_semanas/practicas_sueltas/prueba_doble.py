from models.listas import ListaDoble

lista = ListaDoble()
print(lista)                            # None <-> None
lista.insertar_final("eth0")
lista.insertar_final("eth1")
lista.insertar_final("wlan0")
print(lista)                            # None <-> eth0 <-> eth1 <-> wlan0 <-> None
print(lista.mostrar_inverso())          # None <-> wlan0 <-> eth1 <-> eth0 <-> None
lista.insertar_inicio("lo0")
print(lista)                            # None <-> lo0 <-> eth0 <-> eth1 <-> wlan0 <-> None
print(lista.mostrar_inverso())          # None <-> wlan0 <-> eth1 <-> eth0 <-> lo0 <-> None
print(len(lista), lista.esta_vacia())   # 4 False