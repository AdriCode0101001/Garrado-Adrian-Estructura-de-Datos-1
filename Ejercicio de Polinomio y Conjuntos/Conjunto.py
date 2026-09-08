"""Modulo que representa un conjunto de estudiantes usando objetos (TDA Conjunto).

Ejemplo aplicado: estudiantes inscritos en distintas materias de la
carrera, usando las operaciones clasicas de union, interseccion y
diferencia entre conjuntos.
"""


class ConjuntoEstudiantes:
    """Representa un conjunto de estudiantes y sus operaciones basicas."""

    def __init__(self, elementos=None):
        """Inicializa el conjunto con una lista de elementos.

        Args:
            elementos: Lista inicial de elementos. Si es None, el
                conjunto se crea vacio.
        """
        if elementos is None:
            self.elementos = []
        else:
            self.elementos = list(elementos)

    def agregar(self, elemento):
        """Agrega un elemento al conjunto si aun no esta presente.

        Args:
            elemento: Elemento a agregar.
        """
        if elemento not in self.elementos:
            self.elementos.append(elemento)

    def quitar(self, elemento):
        """Quita un elemento del conjunto si esta presente.

        Args:
            elemento: Elemento a eliminar.
        """
        if elemento in self.elementos:
            self.elementos.remove(elemento)

    def union(self, otra_materia):
        """Calcula la union entre este conjunto y otro.

        Args:
            otra_materia: Otro objeto ConjuntoEstudiantes.

        Returns:
            ConjuntoEstudiantes: Nuevo conjunto con los elementos de
            ambos conjuntos, sin duplicados.
        """
        nueva_materia = ConjuntoEstudiantes(self.elementos.copy())
        for elemento in otra_materia.elementos:
            nueva_materia.agregar(elemento)
        return nueva_materia

    def interseccion(self, otra_materia):
        """Calcula la interseccion entre este conjunto y otro.

        Args:
            otra_materia: Otro objeto ConjuntoEstudiantes.

        Returns:
            ConjuntoEstudiantes: Nuevo conjunto con los elementos que
            estan presentes en ambos conjuntos.
        """
        nueva_materia = ConjuntoEstudiantes()
        for elemento in self.elementos:
            if elemento in otra_materia.elementos:
                nueva_materia.agregar(elemento)
        return nueva_materia

    def diferencia(self, otra_materia):
        """Calcula la diferencia entre este conjunto y otro.

        Args:
            otra_materia: Otro objeto ConjuntoEstudiantes.

        Returns:
            ConjuntoEstudiantes: Nuevo conjunto con los elementos que
            estan en este conjunto pero no en otra_materia.
        """
        nueva_materia = ConjuntoEstudiantes()
        for elemento in self.elementos:
            if elemento not in otra_materia.elementos:
                nueva_materia.agregar(elemento)
        return nueva_materia

    def __str__(self):
        """Devuelve la representacion en texto del conjunto (ej: {A, B})."""
        return "{" + ", ".join(map(str, self.elementos)) + "}"


if __name__ == "__main__":
    estructura_de_datos_1 = ConjuntoEstudiantes(
        ["Juan", "Pedro", "Jose", "Mario"]
    )
    programacion_ensamblador = ConjuntoEstudiantes(
        ["Robert", "Jhoel", "Antonio", "Mario"]
    )
    base_de_datos_1 = ConjuntoEstudiantes(
        ["Maria", "Juana", "Alejandra", "Mario"]
    )

    union_est = estructura_de_datos_1.union(programacion_ensamblador)
    print(f"Estudiantes que estan en ed1 o ensamblador: {union_est}")

    interseccion_est = programacion_ensamblador.interseccion(base_de_datos_1)
    print(f"Interseccion de ensamblador y base de datos: {interseccion_est}")

    diferencia_est = estructura_de_datos_1.diferencia(base_de_datos_1)
    print(
        "Alumnos que estan en ed1, pero no en base de datos: "
        f"{diferencia_est}"
    )

    base_de_datos_1.agregar("Rogelio")
    print(f"Nueva lista de alumnos de base de datos: {base_de_datos_1}")

    programacion_ensamblador.quitar("Robert")
    print(f"Nueva lista de alumnos de ensamblador: {programacion_ensamblador}")

    en_las_tres = (
        estructura_de_datos_1
        .interseccion(programacion_ensamblador)
        .interseccion(base_de_datos_1)
    )
    print(f"Estudiantes en las 3 materias a la vez: {en_las_tres}")