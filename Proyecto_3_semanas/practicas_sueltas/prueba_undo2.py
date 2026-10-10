from models.excepciones import EstructuraVaciaError
from models.pilas import UndoRedoManager

h = UndoRedoManager()
h.registrar("agregar ruta A")
h.registrar("agregar ruta B")
print(h.deshacer())
print(h)
print(h.rehacer())
print(h)
print(h.deshacer())
h.registrar("agregar ruta C")
print(h.puede_rehacer())
print(h)
h.deshacer()
h.deshacer()
print(h.puede_deshacer())
try:
    h.deshacer()
except EstructuraVaciaError as error:
    print("Error:", error)