from models.nodo import Nodo

a = Nodo("eth0")
b = Nodo("eth1")
c = Nodo("wlan0")

a.siguiente = b   # a apunta a b 
b.siguiente = c   # b apunta a c

b.anterior = a    # b apunta a a
c.anterior = b    # c apunta a b 


print(a.dato)  # Salida: eth0   
print(a.siguiente.dato)  # Salida: eth1
print(a.siguiente.siguiente.dato)  # Salida: wlan0
print(b.anterior.dato)  # Salida: eth0
print(c.anterior.dato)    # Salida: eth1
print(c.siguiente)  # Salida: None
