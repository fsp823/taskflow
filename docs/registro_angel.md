Aquí tienes el Docs_angel.md con el framework S.P.E.C.A.R completo.
Cubre todo lo que hiciste:

S — Situación: tu rol oficial y lo que terminaste haciendo de más
P — Problema: los 4 problemas reales que resolviste (incluyendo el bug de Windows)
E — Ejecución: cada archivo explicado con qué contiene, para qué sirve, qué generó la IA y qué cambiaste tú
C — Tabla resumen de cambios manuales por archivo
A — Aprendizajes técnicos concretos
R — Resultado final con todo lo que funciona

Ponlo en la raíz del repo junto al README para que tus compañeros sepan exactamente qué hiciste tú.



# 📋 Docs_angel.md — Documentación de contribución individual
### Proyecto: TaskFlow CLI · Módulo 2 · Dicampus
### Autor: Ángel · Rol: Dev de Lógica

---

## S — Situación

El proyecto **TaskFlow CLI** es un gestor de tareas en consola escrito en Python 3.12+.
El equipo está formado por 3-4 personas, cada una con un rol asignado.

**Mi rol asignado:** Dev de Lógica (nivel medio-alto)
**Responsabilidad oficial según el enunciado:** Implementar `models.py`, `storage.py` y `logic.py`.

**Lo que terminé haciendo además:**
- `cli.py` — interfaz de comandos con Typer y Rich (rol de Refactor & CLI)
- `main.py` — menú interactivo completo para usuarios sin conocimientos de programación

El motivo fue una decisión del equipo: asumir más carga para avanzar más rápido.

---

## P — Problema

Los archivos que me correspondían debían resolver tres problemas concretos:

1. **Modelo de datos:** Necesitábamos una estructura para representar una tarea con validaciones robustas y capacidad de serialización a JSON.
2. **Persistencia:** Las tareas tenían que guardarse en disco y recuperarse entre sesiones, incluso en sistemas Windows donde PowerShell genera archivos con BOM (Byte Order Mark) que rompían la lectura UTF-8 estándar.
3. **Lógica de negocio:** Filtrar, ordenar y calcular estadísticas sobre las tareas de forma limpia y testeable.
4. **Usabilidad:** La interfaz de comandos tipo `python main.py add "tarea" --prioridad 3` no es intuitiva para usuarios no técnicos, así que construí un menú interactivo completo.

---

## E — Ejecución

### Archivos creados y su contenido

---

#### 📄 `taskflow/models.py`
**Para qué sirve:** Define la estructura de datos central del proyecto. Toda tarea que existe en el sistema es una instancia de `Task`.

**Qué contiene:**
- Clase `Task` con `@dataclass`
- Campos: `id` (str, autogenerado con uuid4), `titulo` (str), `prioridad` (int 1-5), `estado` (str, por defecto `"pendiente"`), `fecha_creacion` (str, ISO format autogenerado)
- `__post_init__`: valida que el título no esté vacío y que la prioridad esté entre 1 y 5, lanzando `ValueError` si no se cumple
- `to_dict()`: convierte la tarea a diccionario para guardarla en JSON
- `from_dict(d)`: método de clase que reconstruye una `Task` desde un diccionario leído del JSON

**Commits:** 05, 06, 07

**Lo que generó la IA:** La estructura base del dataclass con los campos y tipos, el esqueleto de `to_dict` y `from_dict`.

**Lo que cambié yo:**
- Añadí la validación de título vacío (`__post_init__`) — el enunciado no la pedía pero tiene sentido
- Reorganicé el orden de los campos para que los que tienen `default` vayan siempre después de los que no (requisito de Python)
- Añadí docstrings con ejemplos reales de entrada/salida

---

#### 📄 `taskflow/storage.py`
**Para qué sirve:** Gestiona la persistencia de las tareas en disco. Es la capa entre la lógica y el sistema de archivos.

**Qué contiene:**
- `DEFAULT_PATH`: constante con la ruta por defecto (`tasks.json`)
- `load_tasks(path)`: lee el JSON y devuelve lista de `Task`. Si el archivo no existe o está vacío, devuelve lista vacía sin lanzar error
- `save_tasks(tasks, path)`: serializa la lista de tareas y la escribe en JSON con `indent=2`

**Commits:** 11, 12

**Lo que generó la IA:** La estructura base de ambas funciones con `json.load` y `json.dump`.

**Lo que cambié yo:**
- Añadí `path.parent.mkdir(parents=True, exist_ok=True)` en `save_tasks` para que cree la carpeta si no existe
- Añadí `ensure_ascii=False` para que los caracteres como `á`, `ñ`, `é` se guarden correctamente
- Cambié `encoding="utf-8"` a `encoding="utf-8-sig"` en `load_tasks` para resolver un bug real en Windows: PowerShell genera archivos con BOM que rompían la lectura estándar UTF-8
- Añadí la comprobación de contenido vacío (`content.strip()`) para evitar el `JSONDecodeError` cuando el archivo existe pero está vacío

---

#### 📄 `taskflow/logic.py`
**Para qué sirve:** Contiene toda la lógica de negocio sobre las tareas. Estas funciones son las que usa el CLI para filtrar, ordenar y mostrar estadísticas.

**Qué contiene:**
- `filter_by_status(tasks, status)`: filtra una lista de tareas por estado. Maneja lista vacía.
- `sort_by_priority(tasks, reverse=False)`: ordena tareas por prioridad usando Timsort (O(n log n)). Devuelve una nueva lista sin modificar la original.
- `get_stats(tasks)`: calcula estadísticas: total, pendientes, completadas y prioridad media. Implementada **sin IA**, como exige el enunciado.

**Commits:** 14, 15, 16

**Lo que generó la IA:** `filter_by_status` y `sort_by_priority` con sus docstrings base.

**Lo que cambié yo:**
- En `sort_by_priority` añadí el comentario explicando que Python usa Timsort y su complejidad O(n log n) — el enunciado lo exige explícitamente
- `get_stats` la implementé yo completamente sin IA: usé `sum()` con generadores en lugar de bucles para mayor limpieza, y añadí el early return para lista vacía que evita la división por cero en `prioridad_media`

---

#### 📄 `taskflow/cli.py`
**Para qué sirve:** Interfaz de línea de comandos usando Typer. Permite usar la app desde el terminal con comandos como `python main.py add "tarea"`.

> ⚠️ Este archivo no era mi responsabilidad oficial según el enunciado (es del rol Refactor & CLI), pero lo implementé por decisión del equipo.

**Qué contiene:**
- Comando `add`: crea una tarea con título y prioridad
- Comando `list`: muestra todas las tareas en tabla Rich con colores por prioridad, con opciones de filtro y orden
- Comando `done`: marca una tarea como completada por ID parcial
- Comando `delete`: elimina una tarea con confirmación
- Comando `stats`: muestra estadísticas con barra de progreso visual

**Lo que generó la IA:** La estructura base de los comandos Typer y la tabla Rich.

**Lo que cambié yo:**
- Añadí búsqueda por ID parcial (los primeros caracteres) para no tener que escribir el UUID completo
- Añadí detección de IDs ambiguos (varios resultados) con mensaje de error claro
- Colores por prioridad con el diccionario `colors`
- Integré `get_stats` en el comando `stats` con la barra de progreso del reto opcional

---

#### 📄 `main.py`
**Para qué sirve:** Punto de entrada de la aplicación. Contiene un menú interactivo completo pensado para usuarios sin conocimientos de programación. En lugar de recordar comandos, el usuario navega con números.

**Qué contiene:**
- Menú principal con 8 opciones numeradas
- Opción 1: Agregar tarea (pide título y prioridad interactivamente)
- Opción 2: Ver todas las tareas
- Opción 3: Ver tareas por hacer (pendientes)
- Opción 4: Ver tareas completadas
- Opción 5: Marcar tarea como hecha
- Opción 6: Estadísticas con barra de progreso
- Opción 7: Eliminar tarea
- Opción 0: Salir
- Header visual con Panel Rich en cada pantalla
- Limpieza de pantalla entre opciones para una experiencia limpia

**Lo que generó la IA:** La estructura del bucle principal y las funciones de pantalla base.

**Lo que cambié yo:**
- Añadí la opción 5 (marcar como hecha) que no estaba en la versión inicial
- Resolví el bug de PowerShell BOM que impedía crear el `tasks.json` correctamente
- Añadí la función `completar_tarea()` que muestra solo las pendientes y permite marcarlas

---

## C — Cambios respecto al código generado por IA

| Archivo | Cambio manual más importante |
|---|---|
| `models.py` | Validación de título vacío en `__post_init__` |
| `storage.py` | Encoding `utf-8-sig` para compatibilidad con Windows + comprobación de archivo vacío |
| `logic.py` | `get_stats` implementada 100% sin IA + early return para lista vacía |
| `cli.py` | Búsqueda por ID parcial + detección de ambigüedad |
| `main.py` | Menú interactivo completo + opción de marcar tareas como hechas |

---

## A — Aprendizajes

- **`@dataclass` y `__post_init__`:** Los dataclasses de Python generan automáticamente `__init__`, `__repr__` y `__eq__`. El `__post_init__` se ejecuta justo después y es el lugar correcto para validar.
- **`@classmethod` como constructor alternativo:** `from_dict` usa `cls(...)` en lugar de `Task(...)` para que funcione correctamente si la clase se hereda en el futuro.
- **`sorted()` vs `.sort()`:** `sorted()` devuelve una nueva lista sin modificar la original. Usar `.sort()` habría mutado la lista del caller, lo que es un efecto secundario inesperado.
- **BOM en Windows:** PowerShell genera archivos UTF-8 con BOM por defecto. `utf-8-sig` en Python lo maneja de forma transparente.
- **Early return:** En `get_stats`, manejar el caso vacío al principio evita la división por cero y hace el código más legible.

---

## R — Resultado

La aplicación funciona completamente:

```
python main.py
```

- ✅ Crear tareas con título y prioridad
- ✅ Listar tareas con colores por prioridad
- ✅ Filtrar por estado (pendiente / completada)
- ✅ Marcar tareas como hechas
- ✅ Eliminar tareas con confirmación
- ✅ Ver estadísticas con barra de progreso
- ✅ Persistencia en `tasks.json` entre sesiones
- ✅ Compatible con Windows (PowerShell BOM)
- ✅ Interfaz navegable sin conocimientos de programación

---

*Documentación generada al cierre del proyecto · TaskFlow CLI · Dicampus Módulo 2*