# ⚠️ Advertencia de Pylance con `rich` en VS Code

> Las líneas onduladas rojas **no son errores reales** — tu código funciona perfectamente.

---

## 🔍 ¿Por qué aparecen?

`rich` no incluye archivos de stubs de tipos (`.pyi`), por lo que **Pylance no reconoce bien sus submódulos**:

- `rich`
- `rich.console`
- `rich.table`
- `rich.text`

---

## ✅ Solución

Añade esto en tu `settings.json` de VS Code:

```json
{
    "python.analysis.ignore": ["rich"]
}
```

> **⚠️ Atención:** Al archivo le faltaban las llaves `{}` externas.  
> El bloque JSON debe estar **siempre envuelto** en ellas.

---

## 📁 ¿Dónde está el `settings.json`?

Puedes abrirlo con:

```
Ctrl + Shift + P → "Open User Settings (JSON)"
```