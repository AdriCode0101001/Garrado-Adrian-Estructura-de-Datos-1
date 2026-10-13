from typing import Any, Optional

import flet as ft


def color_de(tipo: str) -> ft.Colors:
    """Color de la tarjeta según el tipo de tráfico."""
    if tipo == "voz":
        return ft.Colors.RED_400
    if tipo == "video":
        return ft.Colors.AMBER_700
    return ft.Colors.GREY_700


def salida_de(paquete: Any) -> str:
    """Texto con la interfaz por la que salió (o si sigue esperando)."""
    if paquete.salida:
        return f"salió por {paquete.salida}"
    return "en espera"


def tarjeta_paquete(paquete: Any) -> ft.Container:
    """Dibuja un paquete como una tarjeta de color."""
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(f"#{paquete.id} {paquete.tipo}",
                        weight=ft.FontWeight.BOLD),
                ft.Text(f"prioridad {paquete.prioridad}", size=12),
                ft.Text(f"espera {paquete.ciclos_esperados}", size=12),
                ft.Text(f"desde {paquete.origen}", size=12),
                ft.Text(salida_de(paquete), size=12),
            ],
            spacing=2,
        ),
        bgcolor=color_de(paquete.tipo),
        padding=10,
        border_radius=8,
        width=120,
    )


def panel_paquetes(titulo: str, paquetes: Any) -> ft.Column:
    """Dibuja un título y una fila de tarjetas, una por paquete."""
    fila = ft.Row(wrap=True, spacing=8, run_spacing=8)
    for paquete in paquetes:
        fila.controls.append(tarjeta_paquete(paquete))
    if not fila.controls:
        fila.controls.append(ft.Text("(vacío)", italic=True))
    return ft.Column(
        [ft.Text(titulo, size=18, weight=ft.FontWeight.BOLD), fila],
        spacing=6,
    )


def celda_buffer(indice: int, paquete: Any, marca: str) -> ft.Container:
    """Dibuja una celda del buffer: su número, su contenido y su marca."""
    if paquete is None:
        contenido = ft.Text("libre", size=12, italic=True)
        fondo = None
    else:
        contenido = ft.Text(f"#{paquete.id} {paquete.tipo}", size=12,
                            weight=ft.FontWeight.BOLD)
        fondo = color_de(paquete.tipo)
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(f"[{indice}]", size=11),
                contenido,
                ft.Text(marca, size=11, color=ft.Colors.BLUE_300),
            ],
            spacing=2,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=fondo,
        border=ft.Border.all(1, ft.Colors.OUTLINE),
        border_radius=8,
        padding=6,
        width=90,
    )


def panel_buffer(buffer: Any) -> ft.Column:
    """Dibuja el buffer circular celda por celda, con frente y fondo."""
    fila = ft.Row(wrap=True, spacing=6, run_spacing=6)
    for i in range(buffer.capacidad):
        marca = ""
        if i == buffer.indice_frente:
            marca += "frente "
        if i == buffer.indice_fondo:
            marca += "fondo"
        fila.controls.append(celda_buffer(i, buffer.celda(i), marca))
    titulo = f"Buffer circular ({len(buffer)} de {buffer.capacidad})"
    return ft.Column(
        [ft.Text(titulo, size=18, weight=ft.FontWeight.BOLD), fila],
        spacing=6,
    )


def panel_tabla(tabla: Any) -> ft.Column:
    """Dibuja la tabla de rutas como la lista doble que es."""
    fila = ft.Row(wrap=True, spacing=6, run_spacing=6,
                  vertical_alignment=ft.CrossAxisAlignment.CENTER)
    fila.controls.append(ft.Text("None"))
    for ruta in tabla:
        fila.controls.append(ft.Text("⟺"))
        fila.controls.append(ft.Container(
            content=ft.Text(str(ruta), size=13),
            border=ft.Border.all(1, ft.Colors.OUTLINE),
            border_radius=8,
            padding=8,
        ))
    fila.controls.append(ft.Text("⟺ None"))
    return ft.Column(
        [ft.Text("Tabla de rutas (ListaDoble)", size=18,
                 weight=ft.FontWeight.BOLD), fila],
        spacing=6,
    )


def panel_osi(paquete: Any, visibles: Optional[int] = None) -> ft.Column:
    """Dibuja la pila OSI de un paquete: arriba el tope.

    visibles: cuántas capas mostrar desde el fondo (None = todas).
    """
    titulo = ft.Text("Pila OSI del último paquete enviado", size=18,
                     weight=ft.FontWeight.BOLD)
    if paquete is None:
        aviso = ft.Text("(todavía no salió ningún paquete)", italic=True)
        return ft.Column([titulo, aviso], spacing=6)
    total = len(paquete.capas)
    if visibles is None:
        visibles = total
    saltar = total - visibles
    bloques = ft.Column(spacing=4)
    for indice, capa in enumerate(paquete.capas):
        if indice < saltar:
            continue
        es_tope = indice == saltar
        texto = f"TOPE → {capa}" if es_tope else capa
        bloques.controls.append(ft.Container(
            content=ft.Text(texto, size=13),
            bgcolor=color_de(paquete.tipo) if es_tope else None,
            border=ft.Border.all(1, ft.Colors.OUTLINE),
            border_radius=6,
            padding=8,
            width=340,
        ))
    if visibles == total:
        estado = "Encapsulado completo: la capa 1 quedó en el tope."
    else:
        estado = f"Paso {visibles} de {total}: la capa de arriba es el tope."
    detalle = ft.Text(
        f"Paquete #{paquete.id} {paquete.tipo} desde {paquete.origen}",
        size=13)
    return ft.Column(
        [titulo, detalle, ft.Text(estado, size=13, italic=True), bloques],
        spacing=6,
    )


def columna_pila(titulo: str, acciones: Any) -> ft.Column:
    """Dibuja una pila de acciones: arriba la más reciente (el tope)."""
    filas = ft.Column(spacing=4)
    for indice, accion in enumerate(acciones):
        texto = f"TOPE → {accion}" if indice == 0 else str(accion)
        filas.controls.append(ft.Container(
            content=ft.Text(texto, size=13),
            border=ft.Border.all(1, ft.Colors.OUTLINE),
            border_radius=6,
            padding=6,
            width=300,
        ))
    if not filas.controls:
        filas.controls.append(ft.Text("(vacía)", italic=True))
    return ft.Column(
        [ft.Text(titulo, size=15, weight=ft.FontWeight.BOLD), filas],
        spacing=4,
    )


def panel_historial(deshacer: Any, rehacer: Any) -> ft.Column:
    """Dibuja las dos pilas del historial, una al lado de la otra."""
    pilas = ft.Row(
        [
            columna_pila("Pila deshacer", deshacer),
            columna_pila("Pila rehacer", rehacer),
        ],
        wrap=True,
        spacing=16,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )
    return ft.Column(
        [ft.Text("Historial de cambios (dos pilas)", size=18,
                 weight=ft.FontWeight.BOLD), pilas],
        spacing=6,
    )


def seccion(titulo: str, controles: list) -> ft.Container:
    """Agrupa varios controles en un recuadro con título."""
    return ft.Container(
        content=ft.Column(
            [ft.Text(titulo, size=20, weight=ft.FontWeight.BOLD)]
            + controles,
            spacing=10,
        ),
        border=ft.Border.all(1, ft.Colors.OUTLINE),
        border_radius=12,
        padding=14,
    )
