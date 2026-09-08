# filepath: /polinomio-mvc-app/src/views/view.py
"""Vista (V de MVC) de la aplicacion de Polinomio.

Solo se encarga de mostrar la ventana y sus componentes graficos.
No conoce como se genera un polinomio: solo expone un metodo para
mostrar el resultado que le entregue el Controlador.
"""

from tkinter import Tk, Frame, Label, Button


class View:
    """Ventana principal de la aplicacion, construida con Tkinter."""

    def __init__(self, master: Tk):
        """Construye todos los widgets de la ventana.

        Args:
            master: La ventana raiz de Tkinter (tk.Tk()).
        """
        self.master = master
        master.title("MVC Tkinter App - Polinomio")

        self.frame = Frame(master, padx=25, pady=25)
        self.frame.pack()

        self.label_titulo = Label(
            self.frame, text="Generador de Polinomios", font=("Arial", 14, "bold")
        )
        self.label_titulo.pack(pady=(0, 15))

        self.boton_polinomio = Button(
            self.frame, text="Polinomio", font=("Arial", 11), width=20
        )
        self.boton_polinomio.pack()

        self.label_resultado = Label(
            self.frame, text="P(x) = 0", font=("Arial", 13, "bold")
        )
        self.label_resultado.pack(pady=(20, 0))

    def mostrar_polinomio(self, texto: str) -> None:
        """Muestra el polinomio actual en la etiqueta de resultado.

        Args:
            texto: Representacion en texto del polinomio (ej: "3x^2+1").
        """
        self.label_resultado.config(text=f"P(x) = {texto}")
