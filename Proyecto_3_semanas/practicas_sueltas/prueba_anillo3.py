from models.excepciones import EstructuraVaciaError
from models.listas import ListaCircularDoble

anillo = ListaCircularDoble()
for nombre in ("PC1", "PC2", "PC3"):
    anillo.insertar(nombre)
print("Token inicial:", anillo.token())
for _ in range(5):
    print("Pasa a:", anillo.avanzar_token())
print("Se cae:", anillo.eliminar_valor("PC3"))
print("Token ahora:", anillo.token())
print(anillo)
for _ in range(3):
    print("Pasa a:", anillo.avanzar_token())
try:
    ListaCircularDoble().avanzar_token()
except EstructuraVaciaError as error:
    print("Error:", error)