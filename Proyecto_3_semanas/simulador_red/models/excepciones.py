class EstructuraVaciaError(Exception):
    """Excepción que se lanza cuando la estructura de datos está vacía."""


class BufferLlenoError(Exception):
    """Se lanza al encolar en un buffer circular que ya está lleno."""
