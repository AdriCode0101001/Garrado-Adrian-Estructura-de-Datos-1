from models.estructura_base import EstructuraLineal
from models.excepciones import EstructuraVaciaError
from models.listas import ListaCircularDoble

anillo = ListaCircularDoble()
for nombre in ("PC1", "PC2", "PC3", "PC4"):
    anillo.insertar(nombre)
print(anillo)
print(anillo.eliminar_valor("PC3"))
print(anillo)
print(anillo.eliminar_valor("PC1"))
print(anillo)
print(anillo._cabeza.anterior.dato, anillo._cabeza.siguiente.dato)
print(anillo.eliminar_valor("PCX"))
print(anillo.eliminar())
print(anillo)
print(anillo.eliminar())
print(anillo)
print(len(anillo), isinstance(anillo, EstructuraLineal))
try:
    anillo.eliminar()
except EstructuraVaciaError as error:
    print("Error:", error)