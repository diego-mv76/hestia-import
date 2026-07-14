import typer
from rich.console import Console

from hestia_import.parser import CPanelBackupParser
from hestia_import.planner import MigrationPlanner

console = Console()


def plan(
    backup: str,
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Mostrar los datos internos de cada tarea.",
    ),
):
    """Generar el plan de migración."""

    parser = CPanelBackupParser(backup)
    info = parser.analyze()

    planner = MigrationPlanner()
    migration = planner.create_plan(info)

    console.rule("[bold green]Plan de Migración")

    for i, task in enumerate(migration.tasks, start=1):

        console.print(
            f"[cyan]{i:02d}.[/cyan] {task.description}"
        )

        if verbose and task.data:

            for key, value in task.data.items():

                console.print(
                    f"      [dim]{key:<15}[/dim] {value}"
                )

        console.print()

    console.print(
        f"[bold green]Total de tareas:[/bold green] {len(migration.tasks)}"
    )
