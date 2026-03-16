# main.py
from rich.console import Console
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.table import Table

from taskflow.models import Task
from taskflow.storage import load_tasks, save_tasks
from taskflow.logic import filter_by_status, sort_by_priority, get_stats
from pathlib import Path

console = Console()
TASKS_PATH = Path("tasks.json")


def clear():
    console.clear()


def header():
    console.print(Panel(
        Text("✅  TaskFlow CLI", justify="center", style="bold bright_white"),
        subtitle="[dim]Gestor de tareas personal[/]",
        style="bright_blue",
        box=box.DOUBLE_EDGE,
    ))


def build_table(tasks: list[Task]) -> Table:
    table = Table(box=box.ROUNDED, expand=True, header_style="bold bright_white on grey23")
    table.add_column("#",         width=4,  justify="right", style="dim")
    table.add_column("ID",        width=8,  style="dim cyan")
    table.add_column("Título",    min_width=20)
    table.add_column("Prioridad", width=12, justify="center")
    table.add_column("Estado",    width=13, justify="center")
    table.add_column("Creada",    width=12, justify="center")

    colors = {1: "green", 2: "cyan", 3: "yellow", 4: "orange1", 5: "red"}

    for i, task in enumerate(tasks, start=1):
        color  = colors.get(task.prioridad, "white")
        estado = Text("✔ completada", style="green") if task.estado == "completada" else Text("⏳ pendiente", style="yellow")
        titulo = Text(task.titulo, style="strike dim" if task.estado == "completada" else "")
        table.add_row(
            str(i),
            task.id[:8],
            titulo,
            Text("★" * task.prioridad, style=color),
            estado,
            task.fecha_creacion[:10],
        )
    return table


def menu_principal():
    opciones = {
        "1": "➕  Agregar tarea",
        "2": "📋  Todas las tareas",
        "3": "⏳  Tareas por hacer",
        "4": "✅  Tareas completadas",
        "5": "📊  Estadísticas",
        "6": "🗑️   Eliminar tarea",
        "0": "🚪  Salir",
    }
    console.print()
    for key, label in opciones.items():
        console.print(f"  [bold cyan]{key}[/]  {label}")
    console.print()
    return Prompt.ask("  [bold]Elige una opción[/]", choices=list(opciones.keys()), show_choices=False)


def agregar_tarea():
    clear()
    header()
    console.print(Panel("➕  [bold]Nueva tarea[/]", style="cyan", box=box.ROUNDED))
    console.print()

    titulo = Prompt.ask("  [bold]Título[/]")
    prioridad = IntPrompt.ask("  [bold]Prioridad[/] [dim](1=baja · 5=crítica)[/]", default=3)

    try:
        tasks = load_tasks(TASKS_PATH)
        task  = Task(titulo=titulo, prioridad=prioridad)
        tasks.append(task)
        save_tasks(tasks, TASKS_PATH)
        console.print(f"\n  ✅ [bold green]Tarea creada:[/] [cyan]{task.titulo}[/] · prioridad [bold]{prioridad}[/] · id [dim]{task.id[:8]}[/]\n")
    except ValueError as e:
        console.print(f"\n  ❌ [bold red]Error:[/] {e}\n")

    Prompt.ask("  [dim]Pulsa Enter para continuar[/]", default="")


def mostrar_tareas(filtro: str | None = None):
    clear()
    header()

    tasks = load_tasks(TASKS_PATH)

    if filtro:
        tasks = filter_by_status(tasks, filtro)
        titulo = "⏳  Tareas por hacer" if filtro == "pendiente" else "✅  Tareas completadas"
    else:
        titulo = "📋  Todas las tareas"

    console.print(Panel(f"[bold]{titulo}[/]", style="cyan", box=box.ROUNDED))
    console.print()

    if not tasks:
        console.print("  [dim]No hay tareas aquí todavía.[/]\n")
    else:
        tasks = sort_by_priority(tasks, reverse=True)
        console.print(build_table(tasks))
        console.print(f"\n  [dim]{len(tasks)} tarea(s)[/]\n")

    Prompt.ask("  [dim]Pulsa Enter para continuar[/]", default="")


def mostrar_stats():
    clear()
    header()
    console.print(Panel("📊  [bold]Estadísticas[/]", style="cyan", box=box.ROUNDED))
    console.print()

    tasks = load_tasks(TASKS_PATH)
    data  = get_stats(tasks)

    if data["total"] == 0:
        console.print("  [dim]No hay tareas todavía.[/]\n")
    else:
        total      = data["total"]
        completadas = data["completadas"]
        porcentaje  = int((completadas / total) * 100)
        barra       = "█" * (porcentaje // 5) + "░" * (20 - porcentaje // 5)

        console.print(f"  Total            [cyan]{total}[/]")
        console.print(f"  Por hacer        [yellow]{data['pendientes']}[/]")
        console.print(f"  Completadas      [green]{completadas}[/]")
        console.print(f"  Prioridad media  [bold]{data['prioridad_media']}[/]")
        console.print(f"\n  Progreso  [green]{barra}[/] [dim]{porcentaje}%[/]\n")

    Prompt.ask("  [dim]Pulsa Enter para continuar[/]", default="")


def eliminar_tarea():
    clear()
    header()
    console.print(Panel("🗑️  [bold]Eliminar tarea[/]", style="red", box=box.ROUNDED))
    console.print()

    tasks = load_tasks(TASKS_PATH)

    if not tasks:
        console.print("  [dim]No hay tareas para eliminar.[/]\n")
        Prompt.ask("  [dim]Pulsa Enter para continuar[/]", default="")
        return

    console.print(build_table(tasks))
    console.print()

    task_id = Prompt.ask("  [bold]ID de la tarea a eliminar[/] [dim](primeros caracteres)[/]")
    matches = [t for t in tasks if t.id.startswith(task_id)]

    if not matches:
        console.print(f"\n  ❌ [red]No se encontró ninguna tarea con id:[/] [cyan]{task_id}[/]\n")
    elif len(matches) > 1:
        console.print(f"\n  ⚠️  [yellow]Varios resultados. Usa más caracteres del ID.[/]\n")
    else:
        task = matches[0]
        if Confirm.ask(f"  ¿Eliminar [cyan]{task.titulo}[/]?"):
            tasks = [t for t in tasks if t.id != task.id]
            save_tasks(tasks, TASKS_PATH)
            console.print(f"\n  🗑️  [bold red]Eliminada:[/] [cyan]{task.titulo}[/]\n")
        else:
            console.print("  [dim]Cancelado.[/]\n")

    Prompt.ask("  [dim]Pulsa Enter para continuar[/]", default="")


def main():
    while True:
        clear()
        header()
        opcion = menu_principal()

        if opcion == "1":
            agregar_tarea()
        elif opcion == "2":
            mostrar_tareas()
        elif opcion == "3":
            mostrar_tareas(filtro="pendiente")
        elif opcion == "4":
            mostrar_tareas(filtro="completada")
        elif opcion == "5":
            mostrar_stats()
        elif opcion == "6":
            eliminar_tarea()
        elif opcion == "0":
            clear()
            console.print(Panel(
                Text("👋  ¡Hasta luego!", justify="center", style="bold bright_white"),
                style="bright_blue",
                box=box.DOUBLE_EDGE,
            ))
            break


if __name__ == "__main__":
    main()