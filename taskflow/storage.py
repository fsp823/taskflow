# taskflow/storage.py
import json
from pathlib import Path
from taskflow.models import Task

DEFAULT_PATH = Path("tasks.json")


def load_tasks(path: Path = DEFAULT_PATH) -> list[Task]:
    """Carga las tareas desde un archivo JSON.

    Si el archivo no existe o está vacío, retorna una lista vacía sin lanzar error.

    Args:
        path: ruta al archivo JSON. Por defecto 'tasks.json'.

    Returns:
        Lista de Task. Vacía si el archivo no existe o está vacío.

    Raises:
        json.JSONDecodeError: si el archivo existe pero tiene JSON malformado.
    """
    if not path.exists():
        return []

    content = path.read_text(encoding="utf-8-sig").strip()
    if not content:
        return []

    return [Task.from_dict(item) for item in json.loads(content)]


def save_tasks(tasks: list[Task], path: Path = DEFAULT_PATH) -> None:
    """Guarda la lista de tareas en un archivo JSON.

    Crea el archivo si no existe. Sobreescribe si ya existe.

    Args:
        tasks: lista de Task a guardar.
        path:  ruta al archivo JSON. Por defecto 'tasks.json'.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump([task.to_dict() for task in tasks], f, indent=2, ensure_ascii=False)