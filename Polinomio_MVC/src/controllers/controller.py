# filepath: /polinomio-mvc-app/src/controllers/controller.py
"""Controlador (C de MVC) de la aplicacion de Polinomio.

Es el unico que conoce tanto al Modelo como a la Vista: conecta el
boton de la Vista con la generacion aleatoria del Modelo, sin que
ninguno de los dos se conozca directamente entre si.
"""

from models.polinomio_model import PolinomioModel
from views.view import View


class Controller:
    """Coordina la interaccion entre el PolinomioModel y la View."""

    def __init__(self, model: PolinomioModel, view: View):
        """Conecta el boton de la vista con el metodo de este controlador.

        Args:
            model: Instancia de PolinomioModel (los datos del polinomio).
            view: Instancia de View (la ventana de Tkinter).
        """
        self.model = model
        self.view = view

        # Bind: conectamos el boton "Polinomio" a generar_polinomio()
        self.view.boton_polinomio.config(command=self.generar_polinomio)

    def generar_polinomio(self) -> None:
        """Le pide al modelo un polinomio nuevo y aleatorio, y actualiza
        la vista para mostrarlo.
        """
        self.model.generar_aleatorio()
        self.actualizar_vista()

    def actualizar_vista(self) -> None:
        """Sincroniza la vista con el estado actual del modelo."""
        texto = self.model.obtener_representacion()
        self.view.mostrar_polinomio(texto)
