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

app = typer.Typer(
    name="taskflow",
    help="✅ TaskFlow CLI — Gestor de tareas en consola",
    add_completion=False,
)
console = Console()

TASKS_PATH = Path("tasks.json")


# ── Helpers ───────────────────────────────────────────────────────────────────

def _priority_color(prioridad: int) -> str:
    """Devuelve un color Rich según la prioridad."""
    colors = {1: "green", 2: "cyan", 3: "yellow", 4: "orange1", 5: "red"}
    return colors.get(prioridad, "white")


def _estado_style(estado: str) -> str:
    """Devuelve un estilo Rich según el estado."""
    return "strike dim" if estado == "completada" else "bold"


def _build_table(tasks: list[Task]) -> Table:
    """Construye la tabla Rich con la lista de tareas."""
    table = Table(
        box=box.ROUNDED,
        show_header=True,
        header_style="bold bright_white on grey23",
        expand=True,
    )
    table.add_column("#",           style="dim",          width=4,  justify="right")
    table.add_column("ID",          style="dim cyan",     width=8)
    table.add_column("Título",      min_width=20)
    table.add_column("Prioridad",   justify="center",     width=10)
    table.add_column("Estado",      justify="center",     width=12)
    table.add_column("Creada",      justify="center",     width=20)

    for i, task in enumerate(tasks, start=1):
        color = _priority_color(task.prioridad)
        style = _estado_style(task.estado)

        priority_text = Text(f"{'★' * task.prioridad}", style=color)
        estado_text   = Text(task.estado, style="green" if task.estado == "completada" else "yellow")
        titulo_text   = Text(task.titulo, style=style)

        table.add_row(
            str(i),
            task.id[:8],
            titulo_text,
            priority_text,
            estado_text,
            task.fecha_creacion[:10],
        )

    return table


# ── Comandos ──────────────────────────────────────────────────────────────────

@app.command()
def add(
    titulo: str = typer.Argument(..., help="Título de la nueva tarea"),
    prioridad: int = typer.Option(3, "--prioridad", "-p", min=1, max=5, help="Prioridad del 1 (baja) al 5 (crítica)"),
):
    """Añade una nueva tarea."""
    try:
        tasks = load_tasks(TASKS_PATH)
        task  = Task(titulo=titulo, prioridad=prioridad)
        tasks.append(task)
        save_tasks(tasks, TASKS_PATH)
        console.print(f"\n  ✅ [bold green]Tarea creada:[/] [cyan]{task.titulo}[/] "
                      f"· prioridad [bold]{prioridad}[/] · id [dim]{task.id[:8]}[/]\n")
    except ValueError as e:
        console.print(f"\n  ❌ [bold red]Error:[/] {e}\n")
        raise typer.Exit(1)


@app.command(name="list")
def list_tasks(
    estado: str = typer.Option(None, "--estado", "-e", help="Filtrar por estado: pendiente | completada"),
    orden: bool = typer.Option(False, "--orden", "-o", help="Ordenar de mayor a menor prioridad"),
):
    """Lista todas las tareas."""
    tasks = load_tasks(TASKS_PATH)

    if not tasks:
        console.print("\n  [dim]No hay tareas todavía. Usa [bold]add[/] para crear una.[/]\n")
        return

    if estado:
        tasks = filter_by_status(tasks, estado)
    if orden:
        tasks = sort_by_priority(tasks, reverse=True)

    console.print()
    console.print(_build_table(tasks))
    console.print(f"  [dim]{len(tasks)} tarea(s) mostrada(s)[/]\n")


@app.command()
def done(
    task_id: str = typer.Argument(..., help="ID (o primeros caracteres) de la tarea a completar"),
):
    """Marca una tarea como completada."""
    tasks = load_tasks(TASKS_PATH)
    matches = [t for t in tasks if t.id.startswith(task_id)]

    if not matches:
        console.print(f"\n  ❌ [bold red]No se encontró ninguna tarea con id:[/] [cyan]{task_id}[/]\n")
        raise typer.Exit(1)

    if len(matches) > 1:
        console.print(f"\n  ⚠️  [yellow]Varios resultados para[/] [cyan]{task_id}[/]. Usa más caracteres del ID.\n")
        raise typer.Exit(1)

    task = matches[0]
    task.estado = "completada"
    save_tasks(tasks, TASKS_PATH)
    console.print(f"\n  ✅ [bold green]Completada:[/] [cyan]{task.titulo}[/]\n")


@app.command()
def delete(
    task_id: str = typer.Argument(..., help="ID (o primeros caracteres) de la tarea a eliminar"),
    force: bool = typer.Option(False, "--force", "-f", help="Eliminar sin confirmación"),
):
    """Elimina una tarea."""
    tasks = load_tasks(TASKS_PATH)
    matches = [t for t in tasks if t.id.startswith(task_id)]

    if not matches:
        console.print(f"\n  ❌ [bold red]No se encontró ninguna tarea con id:[/] [cyan]{task_id}[/]\n")
        raise typer.Exit(1)

    if len(matches) > 1:
        console.print(f"\n  ⚠️  [yellow]Varios resultados para[/] [cyan]{task_id}[/]. Usa más caracteres del ID.\n")
        raise typer.Exit(1)

    task = matches[0]

    if not force:
        confirm = typer.confirm(f"  ¿Eliminar '{task.titulo}'?")
        if not confirm:
            console.print("  [dim]Cancelado.[/]\n")
            return

    tasks = [t for t in tasks if t.id != task.id]
    save_tasks(tasks, TASKS_PATH)
    console.print(f"\n  🗑️  [bold red]Eliminada:[/] [cyan]{task.titulo}[/]\n")


@app.command()
def stats():
    """Muestra estadísticas de las tareas."""
    tasks = load_tasks(TASKS_PATH)
    data  = get_stats(tasks)

    if data["total"] == 0:
        console.print("\n  [dim]No hay tareas todavía.[/]\n")
        return

    completadas = data["completadas"]
    total       = data["total"]
    porcentaje  = int((completadas / total) * 100)
    barra       = "█" * (porcentaje // 5) + "░" * (20 - porcentaje // 5)

    console.print()
    console.print("  [bold bright_white]📊 Estadísticas[/]\n")
    console.print(f"  Total        [cyan]{total}[/]")
    console.print(f"  Pendientes   [yellow]{data['pendientes']}[/]")
    console.print(f"  Completadas  [green]{completadas}[/]")
    console.print(f"  Prioridad media  [bold]{data['prioridad_media']}[/]")
    console.print(f"\n  Progreso  [green]{barra}[/] [dim]{porcentaje}%[/]\n")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app()