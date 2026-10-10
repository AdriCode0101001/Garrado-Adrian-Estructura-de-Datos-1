from models.pilas import UndoRedoManager

historial = UndoRedoManager()
print(historial.puede_deshacer(), historial.puede_rehacer())   # False False
historial.registrar("agregar ruta 10.0.0.0/8")
historial.registrar("cambiar QoS a voz")
historial.registrar("agregar ruta 192.168.1.0/24")
print(historial)
print(historial.puede_deshacer(), historial.puede_rehacer())   # True False