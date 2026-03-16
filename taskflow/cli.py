# taskflow/cli.py
import typer
from rich.console import Console
from rich.table import Table
from rich import box
from rich.text import Text
from pathlib import Path

from taskflow.models import Task
from taskflow.storage import load_tasks, save_tasks
from taskflow.logic import filter_by_status, sort_by_priority, get_stats

# ── Constantes ────────────────────────────────────────────────────────────────

RUTA_TAREAS = Path("tasks.json")

COLORES_PRIORIDAD = {
    1: "green",
    2: "cyan",
    3: "yellow",
    4: "orange1",
    5: "red",
}

ESTADO_COMPLETADA = "completada"
ESTADO_PENDIENTE  = "pendiente"

# ── App y consola ─────────────────────────────────────────────────────────────

app     = typer.Typer(
    name="taskflow",
    help="✅ TaskFlow CLI — Gestor de tareas en consola",
    add_completion=False,
)
consola = Console()


# ── Helpers privados ──────────────────────────────────────────────────────────

def _color_segun_prioridad(prioridad: int) -> str:
    """Devuelve el color Rich correspondiente a la prioridad dada."""
    return COLORES_PRIORIDAD.get(prioridad, "white")


def _estilo_segun_estado(estado: str) -> str:
    """Devuelve el estilo Rich correspondiente al estado de la tarea."""
    return "strike dim" if estado == ESTADO_COMPLETADA else ""


def _buscar_tarea_por_id(tareas: list[Task], id_parcial: str) -> Task | None:
    """Busca una tarea cuyo ID empiece por id_parcial.

    Args:
        tareas:     lista de Task donde buscar.
        id_parcial: primeros caracteres del ID de la tarea.

    Returns:
        La Task encontrada, o None si no hay exactamente una coincidencia.
    """
    coincidencias = [tarea for tarea in tareas if tarea.id.startswith(id_parcial)]

    if not coincidencias:
        consola.print(f"\n  ❌ [bold red]No se encontró ninguna tarea con id:[/] [cyan]{id_parcial}[/]\n")
        return None

    if len(coincidencias) > 1:
        consola.print(f"\n  ⚠️  [yellow]Varios resultados para[/] [cyan]{id_parcial}[/]. Usa más caracteres del ID.\n")
        return None

    return coincidencias[0]


def _construir_tabla_tareas(tareas: list[Task]) -> Table:
    """Construye y devuelve una tabla Rich con la lista de tareas.

    Args:
        tareas: lista de Task a mostrar.

    Returns:
        Tabla Rich lista para imprimir.
    """
    tabla = Table(
        box=box.ROUNDED,
        show_header=True,
        header_style="bold bright_white on grey23",
        expand=True,
    )
    tabla.add_column("#",          style="dim",      width=4,  justify="right")
    tabla.add_column("ID",         style="dim cyan", width=8)
    tabla.add_column("Título",     min_width=20)
    tabla.add_column("Prioridad",  justify="center", width=10)
    tabla.add_column("Estado",     justify="center", width=12)
    tabla.add_column("Creada",     justify="center", width=20)

    for numero, tarea in enumerate(tareas, start=1):
        color_prioridad = _color_segun_prioridad(tarea.prioridad)
        estilo_titulo   = _estilo_segun_estado(tarea.estado)

        texto_prioridad = Text("★" * tarea.prioridad, style=color_prioridad)
        texto_estado    = Text(
            tarea.estado,
            style="green" if tarea.estado == ESTADO_COMPLETADA else "yellow",
        )
        texto_titulo = Text(tarea.titulo, style=estilo_titulo)

        tabla.add_row(
            str(numero),
            tarea.id[:8],
            texto_titulo,
            texto_prioridad,
            texto_estado,
            tarea.fecha_creacion[:10],
        )

    return tabla


# ── Comandos ──────────────────────────────────────────────────────────────────

@app.command()
def add(
    titulo: str = typer.Argument(..., help="Título de la nueva tarea"),
    prioridad: int = typer.Option(
        3, "--prioridad", "-p",
        min=1, max=5,
        help="Prioridad del 1 (baja) al 5 (crítica)",
    ),
):
    """Añade una nueva tarea al gestor."""
    try:
        tareas_actuales = load_tasks(RUTA_TAREAS)
        nueva_tarea     = Task(titulo=titulo, prioridad=prioridad)

        tareas_actuales.append(nueva_tarea)
        save_tasks(tareas_actuales, RUTA_TAREAS)

        consola.print(
            f"\n  ✅ [bold green]Tarea creada:[/] [cyan]{nueva_tarea.titulo}[/]"
            f" · prioridad [bold]{prioridad}[/]"
            f" · id [dim]{nueva_tarea.id[:8]}[/]\n"
        )
    except ValueError as error:
        consola.print(f"\n  ❌ [bold red]Error:[/] {error}\n")
        raise typer.Exit(1)


@app.command(name="list")
def listar_tareas(
    estado: str = typer.Option(
        None, "--estado", "-e",
        help="Filtrar por estado: pendiente | completada",
    ),
    orden_descendente: bool = typer.Option(
        False, "--orden", "-o",
        help="Ordenar de mayor a menor prioridad",
    ),
):
    """Lista todas las tareas, con filtros opcionales."""
    tareas = load_tasks(RUTA_TAREAS)

    if not tareas:
        consola.print("\n  [dim]No hay tareas todavía. Usa [bold]add[/] para crear una.[/]\n")
        return

    if estado:
        tareas = filter_by_status(tareas, estado)

    if orden_descendente:
        tareas = sort_by_priority(tareas, reverse=True)

    consola.print()
    consola.print(_construir_tabla_tareas(tareas))
    consola.print(f"  [dim]{len(tareas)} tarea(s) mostrada(s)[/]\n")


@app.command()
def done(
    id_parcial: str = typer.Argument(..., help="ID (o primeros caracteres) de la tarea a completar"),
):
    """Marca una tarea como completada."""
    tareas = load_tasks(RUTA_TAREAS)
    tarea  = _buscar_tarea_por_id(tareas, id_parcial)

    if not tarea:
        raise typer.Exit(1)

    tarea.estado = ESTADO_COMPLETADA
    save_tasks(tareas, RUTA_TAREAS)
    consola.print(f"\n  ✅ [bold green]Completada:[/] [cyan]{tarea.titulo}[/]\n")


@app.command()
def delete(
    id_parcial: str = typer.Argument(..., help="ID (o primeros caracteres) de la tarea a eliminar"),
    forzar: bool = typer.Option(False, "--force", "-f", help="Eliminar sin confirmación"),
):
    """Elimina una tarea del gestor."""
    tareas = load_tasks(RUTA_TAREAS)
    tarea  = _buscar_tarea_por_id(tareas, id_parcial)

    if not tarea:
        raise typer.Exit(1)

    if not forzar:
        confirmado = typer.confirm(f"  ¿Eliminar '{tarea.titulo}'?")
        if not confirmado:
            consola.print("  [dim]Cancelado.[/]\n")
            return

    tareas_sin_eliminada = [t for t in tareas if t.id != tarea.id]
    save_tasks(tareas_sin_eliminada, RUTA_TAREAS)
    consola.print(f"\n  🗑️  [bold red]Eliminada:[/] [cyan]{tarea.titulo}[/]\n")


@app.command()
def stats():
    """Muestra estadísticas generales de las tareas."""
    tareas      = load_tasks(RUTA_TAREAS)
    estadisticas = get_stats(tareas)

    if estadisticas["total"] == 0:
        consola.print("\n  [dim]No hay tareas todavía.[/]\n")
        return

    total_tareas       = estadisticas["total"]
    tareas_completadas = estadisticas["completadas"]
    porcentaje_avance  = int((tareas_completadas / total_tareas) * 100)
    barra_progreso     = "█" * (porcentaje_avance // 5) + "░" * (20 - porcentaje_avance // 5)

    consola.print()
    consola.print("  [bold bright_white]📊 Estadísticas[/]\n")
    consola.print(f"  Total            [cyan]{total_tareas}[/]")
    consola.print(f"  Pendientes       [yellow]{estadisticas['pendientes']}[/]")
    consola.print(f"  Completadas      [green]{tareas_completadas}[/]")
    consola.print(f"  Prioridad media  [bold]{estadisticas['prioridad_media']}[/]")
    consola.print(f"\n  Progreso  [green]{barra_progreso}[/] [dim]{porcentaje_avance}%[/]\n")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app()