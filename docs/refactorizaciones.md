# 📋 Docs_angel.md — Documentación de la refactorizacion
### Proyecto: TaskFlow CLI · Módulo 2 · Dicampus
### Autor: Ángel · Rol: Dev de Lógica


# 🔧 Refactorizaciones — TaskFlow CLI
### Registro completo de cambios de nomenclatura y limpieza de código

---

## Criterios aplicados en todas las refactorizaciones

- **Español consistente** en todas las variables, parámetros y funciones (el proyecto es en español)
- **Sin letras sueltas** — ninguna variable se llama `f`, `d`, `i`, `t` o similar
- **Nombres que dicen qué contienen** — una variable debe describir su contenido sin necesidad de leer el código alrededor
- **Constantes para valores mágicos** — ningún string o número hardcodeado dentro de las funciones
- **Prefijo `_`** en helpers privados que no forman parte de la API pública del módulo
- **Early return** para casos vacíos o de error — evita anidamiento innecesario
- **Sin lógica duplicada** — si dos funciones hacían lo mismo, se extrajo a un helper

---

## 📄 `taskflow/models.py`

### Constantes añadidas

| Antes | Después | Motivo |
|---|---|---|
| `1` hardcodeado | `PRIORIDAD_MINIMA = 1` | Los números mágicos no se explican solos |
| `5` hardcodeado | `PRIORIDAD_MAXIMA = 5` | Si cambia el rango, se cambia en un solo sitio |
| `"pendiente"` hardcodeado | `ESTADO_INICIAL = "pendiente"` | Consistencia con el resto de archivos |

### Nomenclatura

| Antes | Después | Motivo |
|---|---|---|
| `d` | `datos_tarea` | Un parámetro de una letra no dice qué contiene |
| `t = Task(...)` en ejemplos | `tarea = Task(...)` | Consistencia con el resto del proyecto |

### Lógica

| Antes | Después | Motivo |
|---|---|---|
| `if self.prioridad < 1 or self.prioridad > 5:` | `prioridad_fuera_de_rango = ...` + `if prioridad_fuera_de_rango:` | La condición se nombra antes de usarse — el `if` se lee como lenguaje natural |
| `if not self.titulo or not self.titulo.strip():` | `titulo_vacio = ...` + `if titulo_vacio:` | Mismo criterio — condición nombrada |
| Sin docstring de clase | Docstring completo con `Attributes:` | Los compañeros saben qué representa cada campo sin leer el código |
| `def __post_init__(self):` | `def __post_init__(self) -> None:` | Type hint explícito en todos los métodos |

---

## 📄 `taskflow/storage.py`

### Constantes añadidas

| Antes | Después | Motivo |
|---|---|---|
| `Path("tasks.json")` hardcodeado | `RUTA_PREDETERMINADA = Path("tasks.json")` | Reutilizable y cambiable en un solo sitio |
| `"utf-8-sig"` hardcodeado | `ENCODING_LECTURA = "utf-8-sig"` | El comentario explica el porqué del BOM de Windows |
| `"utf-8"` hardcodeado | `ENCODING_ESCRITURA = "utf-8"` | Consistencia |
| `indent=2` hardcodeado | `INDENTACION_JSON = 2` | Valor configurable sin tocar la lógica |

### Nomenclatura

| Antes | Después | Motivo |
|---|---|---|
| `path` | `ruta_archivo` | `path` es genérico — `ruta_archivo` dice exactamente qué es |
| `tasks` | `lista_tareas` | Deja claro que es una colección, no una tarea suelta |
| `task` | `tarea` | Español consistente |
| `content` | `contenido_crudo` | Indica que es texto raw antes de parsear |
| `f` | `archivo_destino` | Una letra no dice nada |
| `item` | `datos_tarea` | Cada elemento del JSON es el dict de una tarea |

### Lógica

| Antes | Después | Motivo |
|---|---|---|
| `[Task.from_dict(item) for item in json.loads(content)]` en una línea | Variable intermedia `datos_json` + comprehension separada | Más fácil de depurar — se puede inspeccionar `datos_json` |
| `json.dump([task.to_dict() for task in tasks], f, ...)` en una línea | Variable `tareas_serializadas` + `json.dump` separado | Mismo criterio |

---

## 📄 `taskflow/logic.py`

### Constantes añadidas

| Antes | Después | Motivo |
|---|---|---|
| `"pendiente"` hardcodeado | `ESTADO_PENDIENTE = "pendiente"` | Centralizado — si cambia, se cambia en un sitio |
| `"completada"` hardcodeado | `ESTADO_COMPLETADA = "completada"` | Mismo criterio |

### Nomenclatura

| Antes | Después | Motivo |
|---|---|---|
| `tasks` | `lista_tareas` | Deja claro que es una colección |
| `status` | `estado_buscado` | `status` es inglés — `estado_buscado` describe la intención |
| `task` en bucles | `tarea` | Español consistente |
| `total` | `total_tareas` | Evita confusión con otras variables `total` |
| `pendientes` | `cantidad_pendientes` | Deja claro que es un número, no una lista |
| `completadas` | `cantidad_completadas` | Mismo criterio |
| `prioridad_media` | `media_prioridad` | Adjetivo antes del sustantivo — más natural en español |

### Lógica

| Antes | Después | Motivo |
|---|---|---|
| `return sorted(tasks, key=lambda task: task.prioridad, ...)` | `lambda tarea: tarea.prioridad` | Consistencia con el resto del archivo |
| Alineación irregular en `return` | Alineación vertical de valores | Los campos se leen de un vistazo |

---

## 📄 `taskflow/cli.py`

### Constantes añadidas

| Antes | Después | Motivo |
|---|---|---|
| `Path("tasks.json")` | `RUTA_TAREAS` | Reutilizable |
| `{1: "green", ...}` dentro de función | `COLORES_PRIORIDAD` | No debe reconstruirse en cada llamada |
| `"completada"` hardcodeado | `ESTADO_COMPLETADA` | Centralizado |
| `"pendiente"` hardcodeado | `ESTADO_PENDIENTE` | Centralizado |

### Nomenclatura

| Antes | Después | Motivo |
|---|---|---|
| `console` | `consola` | Español consistente |
| `tasks` | `tareas_actuales` / `lista_tareas` | Contexto claro según el uso |
| `task` | `nueva_tarea` / `tarea` | Nombre según su rol en el contexto |
| `matches` | `coincidencias` | Español y descripción clara |
| `force` | `forzar` | Español |
| `reverse` | `orden_descendente` | Describe el comportamiento, no la implementación |
| `i` en bucles | `numero` | Una letra no dice nada |
| `color` | `color_prioridad` | Especifica de qué es el color |

### Lógica extraída

| Antes | Después | Motivo |
|---|---|---|
| Búsqueda por ID duplicada en `done` y `delete` | `_buscar_tarea_por_id()` helper privado | DRY — no repetir lógica |

---

## 📄 `main.py`

### Constantes añadidas

| Antes | Después | Motivo |
|---|---|---|
| `Path("tasks.json")` | `RUTA_ARCHIVO_TAREAS` | Reutilizable y descriptivo |
| `{1: "green", ...}` dentro de función | `COLORES_PRIORIDAD` | No debe reconstruirse en cada llamada |
| `"pendiente"` / `"completada"` hardcodeados | `ESTADO_PENDIENTE` / `ESTADO_COMPLETADA` | Centralizados |
| Opciones del menú dentro de la función | `OPCIONES_MENU` | El menú no debe estar hardcodeado en una función |

### Nomenclatura

| Antes | Después | Motivo |
|---|---|---|
| `console` | `consola` | Español consistente |
| `tasks` | `lista_tareas` | Colección explícita |
| `task` | `tarea` / `nueva_tarea` / `tarea_encontrada` | Nombre según rol en contexto |
| `i` | `numero_fila` | Describe qué representa el número |
| `data` | `estadisticas` | `data` es demasiado genérico |
| `matches` | `coincidencias` | Español y descripción clara |
| `task_id` | `id_introducido` | Describe que es lo que escribió el usuario |
| `color` | `color_prioridad` | Especifica de qué es el color |
| `barra` | `barra_progreso` | Nombre descriptivo |
| `porcentaje` | `porcentaje_avance` | Especifica qué porcentaje |
| `total` | `total_tareas` | Evita ambigüedad |
| `completadas` | `cantidad_completadas` | Deja claro que es un número |

### Funciones renombradas

| Antes | Después | Motivo |
|---|---|---|
| `clear()` | `_limpiar_pantalla()` | Prefijo `_` de privado + nombre descriptivo |
| `header()` | `_imprimir_cabecera()` | Mismo criterio |
| `build_table()` | `_construir_tabla_tareas()` | Prefijo `_` + describe qué construye |
| `menu_principal()` | `mostrar_menu_principal()` | Verbo que describe la acción |
| `agregar_tarea()` | `pantalla_agregar_tarea()` | Prefijo `pantalla_` — es una vista completa |
| `mostrar_tareas()` | `pantalla_listar_tareas()` | Mismo criterio |
| `completar_tarea()` | `pantalla_completar_tarea()` | Mismo criterio |
| `mostrar_stats()` | `pantalla_estadisticas()` | Mismo criterio |
| `eliminar_tarea()` | `pantalla_eliminar_tarea()` | Mismo criterio |

### Lógica

| Antes | Después | Motivo |
|---|---|---|
| `if/elif` largo en `main()` | Diccionario `acciones_menu` + `accion()` | Sin repetición, extensible sin tocar el bucle |
| Lógica de búsqueda duplicada en `completar` y `eliminar` | `_buscar_tarea_por_id()` helper privado | DRY |
| `Prompt.ask("Pulsa Enter...")` repetido en cada función | `_esperar_enter()` helper privado | DRY |

---

## Resumen global de cambios

| Tipo de cambio | Cantidad aproximada |
|---|---|
| Variables renombradas | 40+ |
| Constantes extraídas | 15 |
| Helpers privados creados | 4 |
| Lógica duplicada eliminada | 3 bloques |
| Docstrings añadidos o mejorados | 12 |
| Type hints añadidos | 8 |

---

*Refactorizaciones aplicadas durante el desarrollo de TaskFlow CLI · Dicampus Módulo 2*