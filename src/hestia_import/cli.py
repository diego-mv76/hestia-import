import typer
from rich.console import Console

from hestia_import import __version__

console = Console()

app = typer.Typer(
    help="Migrador de backups cPanel hacia HestiaCP",
    no_args_is_help=True
)


@app.command()
def version():
    """Mostrar versión."""
    console.print(f"[green]Hestia Import {__version__}[/green]")


@app.command()
def analyze(backup: str):
    """Analizar un backup de cPanel."""
    console.rule("[bold blue]Analyze")
    console.print(f"Backup: [cyan]{backup}[/cyan]")
    console.print("[yellow]Parser todavía no implementado[/yellow]")


if __name__ == "__main__":
    app()
