"""Ejercicio 2 - Unidad 2: ADT Conjunto.

ConjuntoADT con union, interseccion, diferencia,
diferencia_simetrica y es_subconjunto.
"""


class ConjuntoADT:
    def __init__(self, elementos=None):
        self.elementos = list(elementos) if elementos else []
        # evitar duplicados desde el inicio
        vistos = []
        for e in self.elementos:
            if e not in vistos:
                vistos.append(e)
        self.elementos = vistos

    def agregar(self, elemento):
        if elemento not in self.elementos:
            self.elementos.append(elemento)

    def union(self, otro):
        nuevo = ConjuntoADT(self.elementos)
        for e in otro.elementos:
            nuevo.agregar(e)
        return nuevo

    def interseccion(self, otro):
        return ConjuntoADT([e for e in self.elementos if e in otro.elementos])

    def diferencia(self, otro):
        return ConjuntoADT([e for e in self.elementos if e not in otro.elementos])

    def diferencia_simetrica(self, otro):
        # esta en uno u otro pero no en ambos
        parte1 = self.diferencia(otro)
        parte2 = otro.diferencia(self)
        return parte1.union(parte2)

    def es_subconjunto(self, otro):
        # True si todos los elementos de self estan en otro
        for e in self.elementos:
            if e not in otro.elementos:
                return False
        return True

    def __str__(self):
        return "{" + ", ".join(str(e) for e in self.elementos) + "}"


def main():
    print("--- Caso 1: numeros ---")
    a = ConjuntoADT([1, 2, 3, 4])
    b = ConjuntoADT([3, 4, 5, 6])
    print(f"A = {a}")
    print(f"B = {b}")
    print(f"union: {a.union(b)}")
    print(f"interseccion: {a.interseccion(b)}")
    print(f"diferencia A-B: {a.diferencia(b)}")
    print(f"diferencia simetrica: {a.diferencia_simetrica(b)}")

    print("\n--- Caso 2: numeros, subconjunto ---")
    c = ConjuntoADT([2, 3])
    print(f"C = {c}, C es subconjunto de A? {c.es_subconjunto(a)}")
    print(f"B es subconjunto de A? {b.es_subconjunto(a)}")

    print("\n--- Caso 3: cadenas ---")
    materias1 = ConjuntoADT(["Calculo", "Fisica", "Redes"])
    materias2 = ConjuntoADT(["Redes", "Assembler"])
    print(f"materias1 = {materias1}")
    print(f"materias2 = {materias2}")
    print(f"union: {materias1.union(materias2)}")
    print(f"diferencia simetrica: {materias1.diferencia_simetrica(materias2)}")


if __name__ == "__main__":
    main()