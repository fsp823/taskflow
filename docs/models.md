# `taskflow/models.py`

Modelo de datos principal de taskflow. Define la clase `Task` como un dataclass inmutable con validación automática en la creación.

---

## Dependencias

| Módulo | Uso |
|--------|-----|
| `dataclasses` | `@dataclass`, `field` |
| `datetime` | Marca de tiempo ISO en `fecha_creacion` |
| `uuid` | Generación automática de `id` único |

---

## Clase `Task`

```python
@dataclass
class Task:
    titulo: str
    prioridad: int
    estado: str = "pendiente"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    fecha_creacion: str = field(default_factory=lambda: datetime.now().isoformat())
```

Representa una tarea individual. Los campos `id` y `fecha_creacion` se generan automáticamente si no se proporcionan.

---

### Campos

| Campo | Tipo | Requerido | Default | Descripción |
|-------|------|-----------|---------|-------------|
| `titulo` | `str` | ✅ Sí | — | Nombre de la tarea. No puede estar vacío ni ser solo espacios. |
| `prioridad` | `int` | ✅ Sí | — | Nivel de urgencia. Rango válido: `1` (máxima) a `5` (mínima). |
| `estado` | `str` | ❌ No | `"pendiente"` | Estado actual. Valores esperados: `"pendiente"`, `"completada"`. |
| `id` | `str` | ❌ No | `uuid4()` | Identificador único generado automáticamente. |
| `fecha_creacion` | `str` | ❌ No | `datetime.now().isoformat()` | Timestamp ISO 8601 del momento de creación. |

---

### Validación — `__post_init__`

Se ejecuta automáticamente tras la creación. Lanza `ValueError` en dos casos:

```python
# Título vacío o solo espacios
Task(titulo="   ", prioridad=3)
# → ValueError: El título no puede estar vacío

# Prioridad fuera de rango
Task(titulo="Tarea", prioridad=0)
# → ValueError: La prioridad debe estar entre 1 y 5, recibido: 0
```

---

### Métodos

---

#### `to_dict() → dict`

Serializa la tarea a un diccionario compatible con JSON.

```python
t = Task(titulo="Estudiar", prioridad=3)
t.to_dict()
# → {
#     "id": "a1b2c3...",
#     "titulo": "Estudiar",
#     "prioridad": 3,
#     "estado": "pendiente",
#     "fecha_creacion": "2024-01-15T10:30:00.123456"
# }
```

> **Retorna:** `dict` con los cinco campos de la tarea.

---

#### `from_dict(d: dict) → Task` *(classmethod)*

Reconstruye una `Task` desde un diccionario, típicamente leído de un archivo JSON.

```python
datos = {
    "id": "a1b2c3...",
    "titulo": "Estudiar",
    "prioridad": 3,
    "estado": "pendiente",
    "fecha_creacion": "2024-01-15T10:30:00.123456"
}
t = Task.from_dict(datos)
```

> **Retorna:** instancia de `Task`.  
> **Lanza:** `KeyError` si falta alguno de los cinco campos obligatorios en `d`.

---

### Ejemplo de uso completo

```python
from taskflow.models import Task

# Crear con valores mínimos
t = Task(titulo="Revisar PR", prioridad=2)

# Serializar → JSON
data = t.to_dict()

# Reconstruir desde JSON
t2 = Task.from_dict(data)

assert t.id == t2.id  # ✅ True
```

---

## Errores comunes

| Situación | Error |
|-----------|-------|
| `titulo=""` o `titulo="  "` | `ValueError: El título no puede estar vacío` |
| `prioridad=0` o `prioridad=6` | `ValueError: La prioridad debe estar entre 1 y 5` |
| `from_dict` con clave faltante | `KeyError: '<campo>'` |