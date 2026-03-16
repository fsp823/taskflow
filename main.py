# main.py
from pathlib import Path

from rich.console import Console
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import box

from taskflow.models import Task
from taskflow.storage import load_tasks, save_tasks
from taskflow.logic import filter_by_status, sort_by_priority, get_stats

# ── Constantes ────────────────────────────────────────────────────────────────

RUTA_ARCHIVO_TAREAS = Path("tasks.json")

ESTADO_PENDIENTE  = "pendiente"
ESTADO_COMPLETADA = "completada"

COLORES_PRIORIDAD = {
    1: "green",
    2: "cyan",
    3: "yellow",
    4: "orange1",
    5: "red",
}

OPCIONES_MENU = {
    "1": "➕  Agregar tarea",
    "2": "📋  Todas las tareas",
    "3": "⏳  Tareas por hacer",
    "4": "✅  Tareas completadas",
    "5": "☑️   Marcar tarea como hecha",
    "6": "📊  Estadísticas",
    "7": "🗑️   Eliminar tarea",
    "0": "🚪  Salir",
}

# ── Consola ───────────────────────────────────────────────────────────────────

consola = Console()


# ── Helpers privados ──────────────────────────────────────────────────────────

def _limpiar_pantalla() -> None:
    """Limpia la consola antes de renderizar una nueva pantalla."""
    consola.clear()


def _imprimir_cabecera() -> None:
    """Imprime el header principal de la aplicación."""
    consola.print(Panel(
        Text("✅  TaskFlow CLI", justify="center", style="bold bright_white"),
        subtitle="[dim]Gestor de tareas personal[/]",
        style="bright_blue",
        box=box.DOUBLE_EDGE,
    ))


def _esperar_enter() -> None:
    """Pausa la pantalla hasta que el usuario pulse Enter."""
    Prompt.ask("  [dim]Pulsa Enter para continuar[/]", default="")


def _construir_tabla_tareas(lista_tareas: list[Task]) -> Table:
    """Construye y devuelve una tabla Rich con la lista de tareas.

    Args:
        lista_tareas: lista de Task a mostrar en la tabla.

    Returns:
        Tabla Rich lista para imprimir en consola.
    """
    tabla = Table(box=box.ROUNDED, expand=True, header_style="bold bright_white on grey23")
    tabla.add_column("#",          width=4,  justify="right", style="dim")
    tabla.add_column("ID",         width=8,  style="dim cyan")
    tabla.add_column("Título",     min_width=20)
    tabla.add_column("Prioridad",  width=12, justify="center")
    tabla.add_column("Estado",     width=13, justify="center")
    tabla.add_column("Creada",     width=12, justify="center")

    for numero_fila, tarea in enumerate(lista_tareas, start=1):
        color_prioridad = COLORES_PRIORIDAD.get(tarea.prioridad, "white")
        tarea_completada = tarea.estado == ESTADO_COMPLETADA

        texto_titulo    = Text(tarea.titulo, style="strike dim" if tarea_completada else "")
        texto_prioridad = Text("★" * tarea.prioridad, style=color_prioridad)
        texto_estado    = Text(
            "✔ completada" if tarea_completada else "⏳ pendiente",
            style="green" if tarea_completada else "yellow",
        )

        tabla.add_row(
            str(numero_fila),
            tarea.id[:8],
            texto_titulo,
            texto_prioridad,
            texto_estado,
            tarea.fecha_creacion[:10],
        )

    return tabla


def _buscar_tarea_por_id(lista_tareas: list[Task], id_parcial: str) -> Task | None:
    """Busca una tarea cuyo ID empiece por id_parcial.

    Imprime un mensaje de error si no hay resultados o hay ambigüedad.

    Args:
        lista_tareas: lista de Task donde buscar.
        id_parcial:   primeros caracteres del ID de la tarea buscada.

    Returns:
        La Task encontrada, o None si no hay exactamente una coincidencia.
    """
    coincidencias = [tarea for tarea in lista_tareas if tarea.id.startswith(id_parcial)]

    if not coincidencias:
        consola.print(f"\n  ❌ [red]No se encontró ninguna tarea con id:[/] [cyan]{id_parcial}[/]\n")
        return None

    if len(coincidencias) > 1:
        consola.print(f"\n  ⚠️  [yellow]Varios resultados para[/] [cyan]{id_parcial}[/]. Usa más caracteres del ID.\n")
        return None

    return coincidencias[0]


# ── Pantallas ─────────────────────────────────────────────────────────────────

def pantalla_agregar_tarea() -> None:
    """Muestra el formulario para crear una nueva tarea."""
    _limpiar_pantalla()
    _imprimir_cabecera()
    consola.print(Panel("➕  [bold]Nueva tarea[/]", style="cyan", box=box.ROUNDED))
    consola.print()

    titulo_nueva_tarea    = Prompt.ask("  [bold]Título[/]")
    prioridad_nueva_tarea = IntPrompt.ask("  [bold]Prioridad[/] [dim](1=baja · 5=crítica)[/]", default=3)

    try:
        lista_tareas_actual = load_tasks(RUTA_ARCHIVO_TAREAS)
        nueva_tarea         = Task(titulo=titulo_nueva_tarea, prioridad=prioridad_nueva_tarea)

        lista_tareas_actual.append(nueva_tarea)
        save_tasks(lista_tareas_actual, RUTA_ARCHIVO_TAREAS)

        consola.print(
            f"\n  ✅ [bold green]Tarea creada:[/] [cyan]{nueva_tarea.titulo}[/]"
            f" · prioridad [bold]{prioridad_nueva_tarea}[/]"
            f" · id [dim]{nueva_tarea.id[:8]}[/]\n"
        )
    except ValueError as error_validacion:
        consola.print(f"\n  ❌ [bold red]Error:[/] {error_validacion}\n")

    _esperar_enter()


def pantalla_listar_tareas(filtro_estado: str | None = None) -> None:
    """Muestra la lista de tareas, con filtro opcional por estado.

    Args:
        filtro_estado: si se indica, muestra solo las tareas con ese estado.
    """
    _limpiar_pantalla()
    _imprimir_cabecera()

    lista_tareas = load_tasks(RUTA_ARCHIVO_TAREAS)

    if filtro_estado:
        lista_tareas   = filter_by_status(lista_tareas, filtro_estado)
        titulo_pantalla = "⏳  Tareas por hacer" if filtro_estado == ESTADO_PENDIENTE else "✅  Tareas completadas"
    else:
        titulo_pantalla = "📋  Todas las tareas"

    consola.print(Panel(f"[bold]{titulo_pantalla}[/]", style="cyan", box=box.ROUNDED))
    consola.print()

    if not lista_tareas:
        consola.print("  [dim]No hay tareas aquí todavía.[/]\n")
    else:
        lista_tareas_ordenada = sort_by_priority(lista_tareas, reverse=True)
        consola.print(_construir_tabla_tareas(lista_tareas_ordenada))
        consola.print(f"\n  [dim]{len(lista_tareas)} tarea(s)[/]\n")

    _esperar_enter()


def pantalla_completar_tarea() -> None:
    """Muestra las tareas pendientes y permite marcar una como completada."""
    _limpiar_pantalla()
    _imprimir_cabecera()
    consola.print(Panel("☑️   [bold]Marcar tarea como completada[/]", style="green", box=box.ROUNDED))
    consola.print()

    lista_tareas      = load_tasks(RUTA_ARCHIVO_TAREAS)
    tareas_pendientes = filter_by_status(lista_tareas, ESTADO_PENDIENTE)

    if not tareas_pendientes:
        consola.print("  [dim]No hay tareas pendientes.[/]\n")
        _esperar_enter()
        return

    consola.print(_construir_tabla_tareas(tareas_pendientes))
    consola.print()

    id_introducido = Prompt.ask("  [bold]ID de la tarea completada[/] [dim](primeros caracteres)[/]")
    tarea_encontrada = _buscar_tarea_por_id(tareas_pendientes, id_introducido)

    if tarea_encontrada:
        tarea_encontrada.estado = ESTADO_COMPLETADA
        save_tasks(lista_tareas, RUTA_ARCHIVO_TAREAS)
        consola.print(f"\n  ✅ [bold green]Completada:[/] [cyan]{tarea_encontrada.titulo}[/]\n")

    _esperar_enter()


def pantalla_estadisticas() -> None:
    """Muestra estadísticas generales de las tareas con barra de progreso."""
    _limpiar_pantalla()
    _imprimir_cabecera()
    consola.print(Panel("📊  [bold]Estadísticas[/]", style="cyan", box=box.ROUNDED))
    consola.print()

    lista_tareas  = load_tasks(RUTA_ARCHIVO_TAREAS)
    estadisticas  = get_stats(lista_tareas)

    if estadisticas["total"] == 0:
        consola.print("  [dim]No hay tareas todavía.[/]\n")
    else:
        total_tareas        = estadisticas["total"]
        cantidad_completadas = estadisticas["completadas"]
        porcentaje_avance   = int((cantidad_completadas / total_tareas) * 100)
        barra_progreso      = "█" * (porcentaje_avance // 5) + "░" * (20 - porcentaje_avance // 5)

        consola.print(f"  Total            [cyan]{total_tareas}[/]")
        consola.print(f"  Por hacer        [yellow]{estadisticas['pendientes']}[/]")
        consola.print(f"  Completadas      [green]{cantidad_completadas}[/]")
        consola.print(f"  Prioridad media  [bold]{estadisticas['prioridad_media']}[/]")
        consola.print(f"\n  Progreso  [green]{barra_progreso}[/] [dim]{porcentaje_avance}%[/]\n")

    _esperar_enter()


def pantalla_eliminar_tarea() -> None:
    """Muestra todas las tareas y permite eliminar una por ID."""
    _limpiar_pantalla()
    _imprimir_cabecera()
    consola.print(Panel("🗑️  [bold]Eliminar tarea[/]", style="red", box=box.ROUNDED))
    consola.print()

    lista_tareas = load_tasks(RUTA_ARCHIVO_TAREAS)

    if not lista_tareas:
        consola.print("  [dim]No hay tareas para eliminar.[/]\n")
        _esperar_enter()
        return

    consola.print(_construir_tabla_tareas(lista_tareas))
    consola.print()

    id_introducido   = Prompt.ask("  [bold]ID de la tarea a eliminar[/] [dim](primeros caracteres)[/]")
    tarea_encontrada = _buscar_tarea_por_id(lista_tareas, id_introducido)

    if not tarea_encontrada:
        _esperar_enter()
        return

    confirmado = Confirm.ask(f"  ¿Eliminar [cyan]{tarea_encontrada.titulo}[/]?")

    if confirmado:
        lista_sin_eliminada = [tarea for tarea in lista_tareas if tarea.id != tarea_encontrada.id]
        save_tasks(lista_sin_eliminada, RUTA_ARCHIVO_TAREAS)
        consola.print(f"\n  🗑️  [bold red]Eliminada:[/] [cyan]{tarea_encontrada.titulo}[/]\n")
    else:
        consola.print("  [dim]Cancelado.[/]\n")

    _esperar_enter()


def mostrar_menu_principal() -> str:
    """Imprime las opciones del menú y devuelve la opción elegida por el usuario.

    Returns:
        String con la clave de la opción seleccionada.
    """
    consola.print()
    for clave_opcion, etiqueta_opcion in OPCIONES_MENU.items():
        consola.print(f"  [bold cyan]{clave_opcion}[/]  {etiqueta_opcion}")
    consola.print()

    return Prompt.ask(
        "  [bold]Elige una opción[/]",
        choices=list(OPCIONES_MENU.keys()),
        show_choices=False,
    )


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    """Bucle principal de la aplicación. Gestiona la navegación entre pantallas."""
    acciones_menu = {
        "1": pantalla_agregar_tarea,
        "2": lambda: pantalla_listar_tareas(),
        "3": lambda: pantalla_listar_tareas(filtro_estado=ESTADO_PENDIENTE),
        "4": lambda: pantalla_listar_tareas(filtro_estado=ESTADO_COMPLETADA),
        "5": pantalla_completar_tarea,
        "6": pantalla_estadisticas,
        "7": pantalla_eliminar_tarea,
    }

    while True:
        _limpiar_pantalla()
        _imprimir_cabecera()
        opcion_elegida = mostrar_menu_principal()

        if opcion_elegida == "0":
            _limpiar_pantalla()
            consola.print(Panel(
                Text("👋  ¡Hasta luego!", justify="center", style="bold bright_white"),
                style="bright_blue",
                box=box.DOUBLE_EDGE,
            ))
            break

        accion = acciones_menu.get(opcion_elegida)
        if accion:
            accion()


if __name__ == "__main__":
    main()