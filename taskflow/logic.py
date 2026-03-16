# taskflow/logic.py
from taskflow.models import Task


def filter_by_status(tasks: list[Task], status: str) -> list[Task]:
    """Filtra tareas por estado.

    Args:
        tasks:  lista de Task a filtrar.
        status: estado por el que filtrar, p.ej. 'pendiente' o 'completada'.

    Returns:
        Lista de Task cuyo estado coincide con status. Vacía si no hay coincidencias.

    Example:
        >>> pendientes = filter_by_status(tasks, "pendiente")
    """
    return [task for task in tasks if task.estado == status]


def sort_by_priority(tasks: list[Task], reverse: bool = False) -> list[Task]:
    """Ordena tareas por prioridad.

    Usa el algoritmo Timsort de Python (híbrido entre merge sort e insertion sort).
    Complejidad temporal: O(n log n). Complejidad espacial: O(n).

    Args:
        tasks:   lista de Task a ordenar.
        reverse: si True, ordena de mayor a menor prioridad. Por defecto False (menor a mayor).

    Returns:
        Nueva lista de Task ordenada. La lista original no se modifica.

    Example:
        >>> ordenadas = sort_by_priority(tasks, reverse=True)  # 5 → 1
    """
    return sorted(tasks, key=lambda task: task.prioridad, reverse=reverse)


def get_stats(tasks: list[Task]) -> dict:
    """Calcula estadísticas sobre la lista de tareas.

    Args:
        tasks: lista de Task a analizar.

    Returns:
        Diccionario con las claves:
            - total          (int):   número total de tareas.
            - pendientes     (int):   tareas con estado 'pendiente'.
            - completadas    (int):   tareas con estado 'completada'.
            - prioridad_media(float): media de prioridad, 0.0 si no hay tareas.

    Example:
        >>> get_stats([])
        {'total': 0, 'pendientes': 0, 'completadas': 0, 'prioridad_media': 0.0}
    """
    if not tasks:
        return {
            "total": 0,
            "pendientes": 0,
            "completadas": 0,
            "prioridad_media": 0.0,
        }

    total = len(tasks)
    pendientes = sum(1 for task in tasks if task.estado == "pendiente")
    completadas = sum(1 for task in tasks if task.estado == "completada")
    prioridad_media = round(sum(task.prioridad for task in tasks) / total, 2)

    return {
        "total": total,
        "pendientes": pendientes,
        "completadas": completadas,
        "prioridad_media": prioridad_media,
    }