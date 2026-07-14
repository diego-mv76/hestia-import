import subprocess

from rich.console import Console

console = Console()


class CommandRunner:
    """
    Ejecuta comandos del sistema.

    dry_run=True:
        Solo imprime.

    dry_run=False:
        Ejecuta realmente.
    """

    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run

    def run(self, command: list[str]) -> None:

        #
        # Dry Run
        #
        if self.dry_run:

            console.print("[cyan]$[/cyan] " + " ".join(command))
            return

        #
        # Mostrar comando
        #
        console.print("[green]►[/green] " + " ".join(command))

        #
        # Ejecutar
        #
        subprocess.run(
            command,
            check=True,
        )

        console.print("[green]✔ OK[/green]")
