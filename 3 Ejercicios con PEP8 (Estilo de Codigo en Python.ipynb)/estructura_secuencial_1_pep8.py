"""Este módulo calcula el imc de una persona usando estructura secuencial."""
def calculadora_de_imc(peso: float, altura: float) -> float:
    """Calcula el Índice de Masa Corporal (IMC) dado el peso y la altura.
    Args:
        peso (float): Peso en kilogramos.
        altura (float): Altura en metros.
    Returns:
        float: El IMC calculado.
    """
    imc = peso / (altura ** 2)
    return imc


if __name__ == "__main__":
    peso_usuario = float(input("Ingrese su peso en kilogramos: "))
    altura_usuario = float(input("Ingrese su altura en metros: "))
    imc_usuario = calculadora_de_imc(peso_usuario, altura_usuario)
    print("Su índice de masa corporal (IMC) es: ", round(imc_usuario, 2))
