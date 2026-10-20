import time

from models.listas import ListaDoble, ListaSimple

TAMANOS = (1000, 2000, 5000, 10000)


def cronometrar(crear_lista, metodo, cantidad):
    """Inserta 'cantidad' números y devuelve los milisegundos que tardó."""
    lista = crear_lista()
    insertar = getattr(lista, metodo)
    inicio = time.perf_counter()
    for numero in range(cantidad):
        insertar(numero)
    return (time.perf_counter() - inicio) * 1000


def main():
    print("Tiempo total en milisegundos (ms)\n")
    print(f"{'n':>6} | {'Simple inicio':>13} | {'Simple final':>12} | "
          f"{'Doble final':>11}")
    print("-" * 52)
    for n in TAMANOS:
        inicio = cronometrar(ListaSimple, "insertar_inicio", n)
        final = cronometrar(ListaSimple, "insertar_final", n)
        doble = cronometrar(ListaDoble, "insertar_final", n)
        print(f"{n:>6} | {inicio:>13.1f} | {final:>12.1f} | "
              f"{doble:>11.1f}")
    print("\nSi n se duplica: O(1) tarda ~el doble en total;")
    print("O(n) tarda ~4 veces más (cada inserción recorre toda la lista).")


if __name__ == "__main__":
    main()
