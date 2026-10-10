from models.estructura_base import EstructuraLineal
from models.excepciones import EstructuraVaciaError
from models.pilas import Pila

pila = Pila()
for capa in ("Aplicacion", "Transporte", "Red", "Enlace"):
    pila.apilar(capa)
print(pila)                           # TOPE -> Enlace -> Red -> Transporte -> Aplicacion -> None
print(pila.tope())                    # Enlace
print(len(pila))                      # 4
print(pila.desapilar())               # Enlace
print(pila.desapilar())               # Red
print(pila)                           # TOPE -> Transporte -> Aplicacion -> None
print(len(pila), pila.esta_vacia())   # 2 False
pila.desapilar()
pila.desapilar()
print(pila.esta_vacia())              # True
try:
    pila.desapilar()
except EstructuraVaciaError as error:
    print("Error:", error)            # Error: La pila está vacía
print(isinstance(pila, EstructuraLineal))   # True