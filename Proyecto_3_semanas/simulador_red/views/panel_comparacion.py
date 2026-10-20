from typing import Any

import flet as ft

from views.componentes import color_de

TIPOS = ("voz", "video", "datos")


def celda(texto: str, negrita: bool = False) -> ft.DataCell:
    """Una celda de la tabla con texto."""
    peso = ft.FontWeight.BOLD if negrita else None
    return ft.DataCell(ft.Text(texto, weight=peso))


def fila_tipo(tipo: str, qos: Any, fifo: Any) -> ft.DataRow:
    """Fila con la espera promedio de un tipo en los dos modos."""
    espera_qos = qos.metricas.de(tipo).promedio()
    espera_fifo = fifo.metricas.de(tipo).promedio()
    return ft.DataRow(cells=[
        ft.DataCell(ft.Text(tipo, weight=ft.FontWeight.BOLD,
                            color=color_de(tipo))),
        celda(f"{espera_qos:.2f}", espera_qos < espera_fifo),
        celda(f"{espera_fifo:.2f}", espera_fifo < espera_qos),
    ])


def fila_dato(nombre: str, valor_qos: Any, valor_fifo: Any) -> ft.DataRow:
    """Fila con un contador general (ciclos, enviados, descartados)."""
    return ft.DataRow(cells=[celda(nombre), celda(str(valor_qos)),
                             celda(str(valor_fifo))])


def panel_comparacion(comparacion: Any) -> ft.Column:
    """Tabla FIFO vs QoS con el mismo lote de paquetes."""
    if comparacion is None:
        return ft.Column([ft.Text("Aprieta el botón para comparar.",
                                  italic=True)])
    qos = comparacion.qos
    fifo = comparacion.fifo
    lote = ", ".join(str(tipo) for tipo in comparacion.lote)
    filas = [fila_tipo(tipo, qos, fifo) for tipo in TIPOS]
    filas.append(fila_dato("ciclos", qos.ciclo, fifo.ciclo))
    filas.append(fila_dato("enviados", qos.enviados, fifo.enviados))
    filas.append(fila_dato("descartados", qos.descartados,
                           fifo.descartados))
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Espera promedio (ciclos)")),
            ft.DataColumn(ft.Text("QoS"), numeric=True),
            ft.DataColumn(ft.Text("FIFO"), numeric=True),
        ],
        rows=filas,
    )
    voz_qos = qos.metricas.voz.promedio()
    voz_fifo = fifo.metricas.voz.promedio()
    return ft.Column(
        [
            ft.Text("Comparación FIFO vs QoS (mismo lote)", size=18,
                    weight=ft.FontWeight.BOLD),
            ft.Text(f"Lote: {lote}", size=13),
            tabla,
            ft.Text(f"La voz esperó {voz_qos:.2f} ciclos con QoS y "
                    f"{voz_fifo:.2f} con FIFO.", size=15),
        ],
        spacing=6,
    )
