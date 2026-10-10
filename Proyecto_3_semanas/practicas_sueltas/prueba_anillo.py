from models.listas import ListaCircularDoble

anillo = ListaCircularDoble()
print(anillo)
anillo.insertar_final("PC1")
print(anillo)
print(anillo._cabeza.siguiente.dato, anillo._cabeza.anterior.dato)
anillo.insertar_final("PC2")
anillo.insertar_final("PC3")
print(anillo)
cabeza = anillo._cabeza
print(cabeza.anterior.dato, cabeza.siguiente.siguiente.siguiente.dato)
print(len(anillo))