# `taskflow.logic` — Documentación

Módulo de lógica de negocio para el filtrado, ordenación y análisis estadístico de tareas.

---

## Índice

- [Descripción general](#descripción-general)
- [Dependencias](#dependencias)
- [Funciones](#funciones)
  - [filter\_by\_status](#filter_by_status)
  - [sort\_by\_priority](#sort_by_priority)
  - [get\_stats](#get_stats)

---

## Descripción general

`taskflow/logic.py` expone tres funciones puras que operan sobre listas de objetos `Task`. Ninguna función modifica el estado de la aplicación ni produce efectos secundarios: todas reciben datos, los procesan y devuelven un resultado nuevo.

---

## Dependencias

| Módulo | Símbolo importado | Uso |
|---|---|---|
| `taskflow.models` | `Task` | Tipo base de las tareas gestionadas |

---

## Funciones

### `filter_by_status`

```python
def filter_by_status(tasks: list[Task], status: str) -> list[Task]
```

Filtra una lista de tareas devolviendo únicamente aquellas cuyo campo `estado` coincide exactamente con el valor indicado.

**Parámetros**

| Nombre | Tipo | Descripción |
|---|---|---|
| `tasks` | `list[Task]` | Lista de tareas a filtrar |
| `status` | `str` | Estado buscado, p. ej. `"pendiente"` o `"completada"` |

**Retorna**

`list[Task]` — Lista (puede estar vacía) con las tareas cuyo `estado == status`.

**Comportamiento**

- La comparación es exacta y sensible a mayúsculas/minúsculas.
- Si ninguna tarea coincide, devuelve una lista vacía `[]`.
- La lista original `tasks` no se modifica.

**Ejemplo**

```python
pendientes = filter_by_status(tasks, "pendiente")
```

---

### `sort_by_priority`

```python
def sort_by_priority(tasks: list[Task], reverse: bool = False) -> list[Task]
```

Ordena una lista de tareas según el campo numérico `prioridad`.

**Parámetros**

| Nombre | Tipo | Por defecto | Descripción |
|---|---|---|---|
| `tasks` | `list[Task]` | — | Lista de tareas a ordenar |
| `reverse` | `bool` | `False` | `True` para orden descendente (mayor → menor prioridad) |

**Retorna**

`list[Task]` — Nueva lista ordenada. La lista original permanece intacta.

**Detalles de implementación**

Internamente delega en la función built-in `sorted()` de Python, que aplica el algoritmo **Timsort** (híbrido de *merge sort* e *insertion sort*).

| Complejidad | Valor |
|---|---|
| Temporal | O(n log n) |
| Espacial | O(n) |

**Ejemplo**

```python
# Orden ascendente: prioridad 1 → 5
ascendente  = sort_by_priority(tasks)

# Orden descendente: prioridad 5 → 1
descendente = sort_by_priority(tasks, reverse=True)
```

---

### `get_stats`

```python
def get_stats(tasks: list[Task]) -> dict
```

Calcula un resumen estadístico sobre la lista de tareas proporcionada.

**Parámetros**

| Nombre | Tipo | Descripción |
|---|---|---|
| `tasks` | `list[Task]` | Lista de tareas a analizar |

**Retorna**

`dict` con las siguientes claves:

| Clave | Tipo | Descripción |
|---|---|---|
| `total` | `int` | Número total de tareas |
| `pendientes` | `int` | Tareas con `estado == "pendiente"` |
| `completadas` | `int` | Tareas con `estado == "completada"` |
| `prioridad_media` | `float` | Media aritmética de `prioridad`, redondeada a 2 decimales |

**Casos especiales**

Si `tasks` está vacía, la función retorna de forma anticipada el diccionario por defecto para evitar una división por cero:

```python
{'total': 0, 'pendientes': 0, 'completadas': 0, 'prioridad_media': 0.0}
```

**Ejemplo**

```python
stats = get_stats(tasks)
# {'total': 10, 'pendientes': 6, 'completadas': 4, 'prioridad_media': 3.2}

get_stats([])
# {'total': 0, 'pendientes': 0, 'completadas': 0, 'prioridad_media': 0.0}
```