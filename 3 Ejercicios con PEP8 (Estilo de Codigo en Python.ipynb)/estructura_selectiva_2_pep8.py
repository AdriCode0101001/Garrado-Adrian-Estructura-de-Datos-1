"""Este módulo evalúa la elegibilidad para un préstamo usando estructura selectiva."""
def evaluar_prestamo(edad: int, ingresos: float, historial_crediticio: bool) -> str:
    """Evalúa si una persona es elegible para un préstamo 
    basado en su edad, ingresos y historial crediticio.
    Args:
        edad (int): Edad de la persona.
        ingresos (float): Ingresos mensuales de la persona.
        historial_crediticio (bool): Indica si la persona tiene un buen historial crediticio.
    Returns:
        str: Mensaje indicando si la persona es elegible o no para el préstamo.
    """

    if edad < 18:
        return "No eres elegible para el préstamo debido a tu edad."
    elif ingresos < 3300:
        return "No eres elegible para el préstamo debido a tus ingresos."
    elif not historial_crediticio:
        return "No eres elegible para el préstamo debido a tu historial crediticio."
    else:
        return "Eres elegible para el préstamo."


if __name__ == "__main__":
    edad_usuario = int(input("Ingrese su edad: "))
    ingresos_usuario = float(input("Ingrese sus ingresos mensuales: "))
    # Historial obtenido de una consulta previa al sistema bancario
    resultado = evaluar_prestamo(edad_usuario, ingresos_usuario, historial_crediticio=True)
    print(resultado)
