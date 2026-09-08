"""Este módulo calcula la lista de numeros primos desde un rango usando estructura repetitiva."""
def numeros_primos_desde_un_rango(inicio: int, fin: int) -> list:
    """Genera una lista de números primos dentro de un rango dado.
    Args:
        inicio (int): Número inicial del rango.
        fin (int): Número final del rango.
    Returns:
        list: Lista de números primos encontrados en el rango.
    """
    primos = []
    for num in range(inicio, fin + 1):
        if num > 1:  # Los números primos son mayores que 1
            es_primo = True
            for i in range(2, num - 1):
                if num % i == 0:
                    es_primo = False
                    break
            if es_primo:
                primos.append(num)
    return primos


if __name__ == "__main__":
    inicio_rango = int(input("Ingrese el número inicial del rango: "))
    fin_rango = int(input("Ingrese el número final del rango: "))
    primos_encontrados = numeros_primos_desde_un_rango(inicio_rango, fin_rango)
    print("Números primos encontrados en el rango:", primos_encontrados)
