# filepath: /polinomio-mvc-app/src/main.py
"""Punto de entrada de la aplicacion MVC de Polinomio.

Arma las 3 piezas del patron (Modelo, Vista, Controlador) y arranca
el bucle principal de la interfaz grafica.
"""

import tkinter as tk

from views.view import View
from controllers.controller import Controller
from models.polinomio_model import PolinomioModel as Model


def main() -> None:
    """Crea la ventana, conecta MVC y arranca la aplicacion."""
    root = tk.Tk()
    root.title("Tkinter MVC App - Polinomio")

    model = Model()
    view = View(root)
    controller = Controller(model, view)

    # Estado inicial: se muestra "P(x) = 0" (polinomio vacio)
    controller.actualizar_vista()

    root.mainloop()


if __name__ == "__main__":
    main()
