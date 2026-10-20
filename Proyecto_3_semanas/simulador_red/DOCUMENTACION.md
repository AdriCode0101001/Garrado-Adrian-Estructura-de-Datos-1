# Documentación técnica — Simulador de Red con QoS

## 1. Diagrama de clases: estructuras de datos

```mermaid
classDiagram
    class Nodo {
        +dato
        +siguiente
        +anterior
    }
    class NodoPrioridad {
        +prioridad
    }
    class EstructuraLineal {
        <<abstract>>
        +esta_vacia() bool
        +__len__() int
    }
    class EstructuraVaciaError {
        <<exception>>
    }
    class BufferLlenoError {
        <<exception>>
    }
    class ListaSimple {
        -cabeza
        +insertar_inicio(dato)
        +insertar_final(dato)
        +eliminar(dato)
        +__iter__()
    }
    class ListaDoble {
        -cabeza
        -cola
        +insertar_inicio(dato)
        +insertar_final(dato)
        +eliminar(dato)
        +__iter__()
    }
    class ListaCircularDoble {
        -cabeza
        -actual
        +insertar_final(dato)
        +eliminar_valor(dato) bool
        +token()
        +avanzar_token()
    }
    class Pila {
        -tope
        +apilar(dato)
        +desapilar()
        +tope()
        +__iter__()
    }
    class UndoRedoManager {
        +registrar(accion)
        +deshacer()
        +rehacer()
        +puede_deshacer() bool
        +puede_rehacer() bool
    }
    class ColaPrioridad {
        -cabeza
        +encolar(dato, prioridad)
        +desencolar()
        +__iter__()
    }
    class ColaCircular {
        -datos[capacidad]
        -frente
        -fondo
        -cantidad
        +encolar(dato)
        +desencolar()
        +frente()
        +esta_llena() bool
        +celda(i)
    }

    Nodo <|-- NodoPrioridad
    EstructuraLineal <|-- ListaSimple
    EstructuraLineal <|-- ListaDoble
    EstructuraLineal <|-- ListaCircularDoble
    EstructuraLineal <|-- Pila
    EstructuraLineal <|-- ColaPrioridad
    EstructuraLineal <|-- ColaCircular
    ListaSimple o-- Nodo
    ListaDoble o-- Nodo
    ListaCircularDoble o-- Nodo
    Pila o-- Nodo
    ColaPrioridad o-- NodoPrioridad
    UndoRedoManager *-- "2" Pila : deshacer y rehacer
    EstructuraLineal ..> EstructuraVaciaError : lanza
    ColaCircular ..> BufferLlenoError : lanza
```

## 2. Diagrama de clases: dominio y MVC

```mermaid
classDiagram
    class Paquete {
        +id
        +tipo
        +prioridad
        +origen
        +salida
        +ciclos_esperados
        +capas: Pila
        +esperar()
    }
    class Interfaz {
        +nombre
        +capacidad
        +activa
        +caer()
        +levantar()
    }
    class Ruta {
        +destino
        +interfaz
        +metrica
    }
    class Router {
        +buffer: ColaCircular
        +clasificador: ColaPrioridad
        +tabla: ListaDoble
        +interfaces: ListaSimple
        +metricas: Metricas
        +modo_qos
        +recibir(paquete) bool
        +procesar_ciclo()
        +buscar_ruta(destino)
        +alternar_modo()
    }
    class Metricas {
        +voz: Estadistica
        +video: Estadistica
        +datos: Estadistica
        +registrar(paquete)
    }
    class Estadistica {
        +enviados
        +espera_total
        +promedio() float
    }
    class Comparacion {
        +qos: Router
        +fifo: Router
    }
    class AppController {
        +router: Router
        +anillo: ListaCircularDoble
        +historial: UndoRedoManager
        +enviar_paquete(tipo)
        +procesar_ciclo()
        +deshacer()
        +rehacer()
        +comparar_modos()
        +simular_congestion(cantidad)
    }
    class VistaPrincipal {
        +actualizar(router, anillo)
    }
    class AnilloVisual {
        +actualizar(anillo, dueno)
    }

    Router *-- Metricas
    Metricas *-- "3" Estadistica
    Router o-- Paquete : en buffer y clasificador
    Router o-- Ruta : en la tabla
    Router o-- Interfaz : en interfaces
    Comparacion --> "2" Router : gemelos
    AppController --> Router : modelo
    AppController --> VistaPrincipal : vista
    VistaPrincipal ..> AppController : ordenes del usuario
    VistaPrincipal *-- AnilloVisual
```

**Regla MVC:** el modelo (`Router`, estructuras) no conoce Flet; la vista
(`VistaPrincipal`) no importa el modelo. Solo el `AppController` conoce a los
dos.

## 3. Tabla de complejidad temporal

n = cantidad de elementos de la estructura.

| Estructura | Operación | Complejidad | Por qué |
|---|---|---|---|
| ListaSimple | insertar_inicio | **O(1)** | El nuevo nodo apunta a la cabeza |
| ListaSimple | insertar_final | **O(n)** | Recorre hasta el último nodo |
| ListaSimple | buscar / eliminar | O(n) | Recorre nodo por nodo |
| ListaDoble | insertar_inicio | O(1) | Usa la cabeza |
| ListaDoble | insertar_final | **O(1)** | Usa el puntero `cola` |
| ListaDoble | buscar / eliminar | O(n) | Recorre; al borrar reconecta 2 punteros |
| ListaCircularDoble | insertar_final | O(1) | El último es `cabeza.anterior` |
| ListaCircularDoble | avanzar_token / token | O(1) | Mueve o lee el puntero `actual` |
| ListaCircularDoble | eliminar_valor | O(n) | Recorre la vuelta completa |
| Pila | apilar / desapilar / tope | O(1) | Todo ocurre en el tope |
| UndoRedoManager | deshacer / rehacer | O(1) | Pasa un elemento de una pila a otra |
| ColaPrioridad | encolar | **O(n)** | Recorre hasta su lugar según prioridad |
| ColaPrioridad | desencolar | **O(1)** | Siempre saca la cabeza |
| ColaCircular | encolar / desencolar | O(1) | Índices con `% capacidad` |
| ColaCircular | celda(i) / frente | O(1) | Acceso directo al arreglo |
| Router | buscar_ruta | O(r) | Recorre la tabla de r rutas |
| Router | procesar_ciclo | O(b · n) | Clasifica b paquetes del buffer, cada uno O(n) en la cola de prioridad |

**Complejidad espacial:** todas las estructuras enlazadas ocupan O(n), un nodo
por elemento. La ColaCircular ocupa O(capacidad) fija desde el inicio: es la
única que usa un arreglo, porque un buffer de router tiene tamaño fijo y
necesita acceso O(1) por índice.

## 4. Verificación empírica (O(1) vs O(n))

Medido con `medicion_complejidad.py`, tiempo total en ms:

| n | ListaSimple.insertar_inicio | ListaSimple.insertar_final | ListaDoble.insertar_final |
|---|---|---|---|
| 1 000 | 0.8 | 14.7 | 0.3 |
| 10 000 | 9.7 | 1210.1 | 3.0 |

Al multiplicar n por 10, las operaciones O(1) tardan unas 10 veces más en
total (crecimiento lineal), mientras que `insertar_final` de la lista simple
tarda unas 82 veces más (crecimiento cuadrático: O(n) por cada inserción).

## 5. Pruebas

101 pruebas unitarias con `unittest` (`python -m unittest discover tests`):
casos límite de cada estructura (vacía, un elemento, llena), motor de red,
controlador, historial, token, métricas, comparador y congestión.