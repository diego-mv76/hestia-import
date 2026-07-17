import typer
from rich.console import Console

from hestia_import.executor.hestia import HestiaExecutor
from hestia_import.models import MigrationContext
from hestia_import.parser import CPanelBackupParser
from hestia_import.planner import MigrationPlanner

console = Console()


def execute(
    backup: str,
    execute: bool = typer.Option(
        False,
        "--execute",
        help="Ejecutar realmente las tareas.",
    ),
):
    """
    Mostrar los comandos que se ejecutarían sobre HestiaCP.
    """

    parser = CPanelBackupParser(backup)

    info = parser.analyze()

    planner = MigrationPlanner()

    migration = planner.create_plan(info)

    context = MigrationContext()

    executor = HestiaExecutor(
        context=context,
        dry_run=not execute,
    )
    console.rule(
        "[bold green]Dry Run"
        if not execute
        else "[bold red]Ejecución Real"
    )

    if execute:

        console.print()
        console.print(
            "[bold red]ATENCIÓN[/bold red]: Se ejecutarán cambios reales sobre HestiaCP."
        )

        confirm = typer.confirm(
            "¿Desea continuar?",
            default=False,
        )

        if not confirm:
            raise typer.Exit()

    total = len(migration.tasks)

    for index, task in enumerate(migration.tasks, start=1):

        console.print()

        console.rule(
            f"[bold blue][{index}/{total}][/bold blue] {task.description}"
        )

        executor.execute(
            task,
            migration,
        )
