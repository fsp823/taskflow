# taskflow/logic.py
from taskflow.models import Task

# ── Constantes ────────────────────────────────────────────────────────────────

ESTADO_PENDIENTE  = "pendiente"
ESTADO_COMPLETADA = "completada"


# ── Funciones públicas ────────────────────────────────────────────────────────

def filter_by_status(lista_tareas: list[Task], estado_buscado: str) -> list[Task]:
    """Filtra tareas por estado.

    Args:
        lista_tareas:   lista de Task a filtrar.
        estado_buscado: estado por el que filtrar, p.ej. 'pendiente' o 'completada'.

    Returns:
        Lista de Task cuyo estado coincide con estado_buscado.
        Vacía si no hay coincidencias.

    Example:
        >>> pendientes = filter_by_status(tareas, "pendiente")
    """
    return [tarea for tarea in lista_tareas if tarea.estado == estado_buscado]


def sort_by_priority(lista_tareas: list[Task], reverse: bool = False) -> list[Task]:
    """Ordena tareas por prioridad sin modificar la lista original.

    Usa Timsort, el algoritmo nativo de Python (híbrido entre merge sort
    e insertion sort). Complejidad temporal: O(n log n). Espacial: O(n).

    Args:
        lista_tareas: lista de Task a ordenar.
        reverse:      si True, ordena de mayor a menor prioridad (5 → 1).
                      Por defecto False (menor a mayor, 1 → 5).

    Returns:
        Nueva lista de Task ordenada. La lista original no se modifica.

    Example:
        >>> urgentes_primero = sort_by_priority(tareas, reverse=True)
    """
    return sorted(lista_tareas, key=lambda tarea: tarea.prioridad, reverse=reverse)


def get_stats(lista_tareas: list[Task]) -> dict:
    """Calcula estadísticas generales sobre una lista de tareas.

    Implementada sin IA — lógica propia del equipo.

    Args:
        lista_tareas: lista de Task a analizar.

    Returns:
        Diccionario con las claves:
            - total           (int):   número total de tareas.
            - pendientes      (int):   tareas con estado 'pendiente'.
            - completadas     (int):   tareas con estado 'completada'.
            - prioridad_media (float): media de prioridad. 0.0 si no hay tareas.

    Example:
        >>> get_stats([])
        {'total': 0, 'pendientes': 0, 'completadas': 0, 'prioridad_media': 0.0}
    """
    if not lista_tareas:
        return {
            "total": 0,
            "pendientes": 0,
            "completadas": 0,
            "prioridad_media": 0.0,
        }

    total_tareas      = len(lista_tareas)
    cantidad_pendientes  = sum(1 for tarea in lista_tareas if tarea.estado == ESTADO_PENDIENTE)
    cantidad_completadas = sum(1 for tarea in lista_tareas if tarea.estado == ESTADO_COMPLETADA)
    media_prioridad      = round(sum(tarea.prioridad for tarea in lista_tareas) / total_tareas, 2)

    return {
        "total":           total_tareas,
        "pendientes":      cantidad_pendientes,
        "completadas":     cantidad_completadas,
        "prioridad_media": media_prioridad,
    }