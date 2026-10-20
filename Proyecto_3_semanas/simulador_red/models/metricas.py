from typing import Any


class Estadistica:
    """Acumula la espera de los paquetes de un tipo que ya salieron."""

    def __init__(self) -> None:
        self.enviados: int = 0
        self.espera_total: int = 0

    def registrar(self, ciclos: int) -> None:
        """Anota un paquete que salió después de esperar 'ciclos'."""
        self.enviados += 1
        self.espera_total += ciclos

    def promedio(self) -> float:
        """Espera promedio en ciclos (0 si todavía no salió ninguno)."""
        if self.enviados == 0:
            return 0.0
        return self.espera_total / self.enviados


class Metricas:
    """Estadísticas de espera separadas por tipo de tráfico."""

    def __init__(self) -> None:
        self.voz: Estadistica = Estadistica()
        self.video: Estadistica = Estadistica()
        self.datos: Estadistica = Estadistica()

    def de(self, tipo: str) -> Estadistica:
        """Devuelve la estadística del tipo pedido."""
        if tipo == "voz":
            return self.voz
        if tipo == "video":
            return self.video
        return self.datos

    def registrar(self, paquete: Any) -> None:
        """Anota la espera de un paquete que acaba de salir."""
        self.de(paquete.tipo).registrar(paquete.ciclos_esperados)
