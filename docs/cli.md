## 🖥️ CLI — Referencia de comandos

Archivo: `taskflow/cli.py`

Todos los comandos se ejecutan con:
```bash
python -m taskflow.cli <comando> [opciones]
```

---

### ➕ `add` — Añadir una tarea
```bash
python -m taskflow.cli add "Título de la tarea" [--prioridad N]
```

| Argumento | Tipo | Obligatorio | Descripción |
|-----------|------|-------------|-------------|
| `titulo` | string | ✅ | Título de la nueva tarea |
| `--prioridad` / `-p` | int (1-5) | ❌ | Prioridad (por defecto: `3`) |

**Ejemplo:**
```bash
python -m taskflow.cli add "Revisar pull requests" --prioridad 5
```

---

### 📋 `list` — Listar tareas
```bash
python -m taskflow.cli list [--estado ESTADO] [--orden]
```

| Opción | Tipo | Descripción |
|--------|------|-------------|
| `--estado` / `-e` | string | Filtra por `pendiente` o `completada` |
| `--orden` / `-o` | flag | Ordena de mayor a menor prioridad |

**Ejemplos:**
```bash
python -m taskflow.cli list
python -m taskflow.cli list --estado pendiente
python -m taskflow.cli list --orden
```

---

### ✅ `done` — Completar una tarea
```bash
python -m taskflow.cli done <task_id>
```

| Argumento | Tipo | Descripción |
|-----------|------|-------------|
| `task_id` | string | ID completo o primeros caracteres de la tarea |

**Ejemplo:**
```bash
python -m taskflow.cli done a1b2c3
```

---

### 🗑️ `delete` — Eliminar una tarea
```bash
python -m taskflow.cli delete <task_id> [--force]
```

| Argumento | Tipo | Descripción |
|-----------|------|-------------|
| `task_id` | string | ID completo o primeros caracteres de la tarea |
| `--force` / `-f` | flag | Elimina sin pedir confirmación |

**Ejemplo:**
```bash
python -m taskflow.cli delete a1b2c3
python -m taskflow.cli delete a1b2c3 --force
```

---

### 📊 `stats` — Ver estadísticas
```bash
python -m taskflow.cli stats
```

Muestra un resumen con:
- Total de tareas
- Tareas pendientes y completadas
- Prioridad media
- Barra de progreso visual

---

### 🎨 Sistema de prioridades

| Valor | Color | Significado |
|-------|-------|-------------|
| `1` | 🟢 Verde | Baja |
| `2` | 🔵 Cyan | Normal |
| `3` | 🟡 Amarillo | Media *(por defecto)* |
| `4` | 🟠 Naranja | Alta |
| `5` | 🔴 Rojo | Crítica |