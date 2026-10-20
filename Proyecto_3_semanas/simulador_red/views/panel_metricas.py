from typing import Any

import flet as ft

from views.componentes import color_de

ANCHO_BARRA = 200
TIPOS = ("voz", "video", "datos")


def fila_espera(tipo: str, estadistica: Any, maximo: float) -> ft.Row:
    """Una barra por tipo: más larga = esperó más en promedio."""
    promedio = estadistica.promedio()
    largo = 4
    if maximo > 0:
        largo = max(4, int(ANCHO_BARRA * promedio / maximo))
    return ft.Row(
        [
            ft.Text(tipo, width=50, weight=ft.FontWeight.BOLD),
            ft.Container(width=largo, height=18,
                         bgcolor=color_de(tipo), border_radius=4),
            ft.Text(f"{promedio:.2f} ciclos ({estadistica.enviados} "
                    f"enviados)", size=13),
        ],
        spacing=8,
    )


def panel_metricas(router: Any) -> ft.Column:
    """Métricas reales calculadas con los contadores del router."""
    metricas = router.metricas
    maximo = 0.0
    for tipo in TIPOS:
        maximo = max(maximo, metricas.de(tipo).promedio())
    filas = [fila_espera(tipo, metricas.de(tipo), maximo)
             for tipo in TIPOS]
    por_ciclo = 0.0
    if router.ciclo > 0:
        por_ciclo = router.enviados / router.ciclo
    intentos = (router.enviados + router.descartados + router.sin_ruta
                + len(router.buffer) + len(router.clasificador))
    perdida = 0.0
    if intentos > 0:
        perdida = 100 * router.descartados / intentos
    return ft.Column(
        [ft.Text("Espera promedio por tipo", size=18,
                 weight=ft.FontWeight.BOLD)]
        + filas
        + [
            ft.Text(f"Paquetes por ciclo (throughput): {por_ciclo:.2f}",
                    size=15),
            ft.Text(f"Descartados (packet drop): {router.descartados} "
                    f"de {intentos} ({perdida:.1f} %)", size=15),
            ft.Text(f"Sin ruta: {router.sin_ruta}", size=15),
        ],
        spacing=6,
    )
