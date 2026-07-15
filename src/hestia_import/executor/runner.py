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

    def run(
        self,
        command: list[str],
        capture_output: bool = False,
    ) -> subprocess.CompletedProcess | None:
        """
        Ejecuta un comando.

        Si capture_output=True devuelve stdout y stderr.
        """

        #
        # Dry Run
        #
        if self.dry_run:

            console.print("[cyan]$[/cyan] " + " ".join(command))
            return None

        #
        # Mostrar comando
        #
        console.print("[green]►[/green] " + " ".join(command))

        try:

            result = subprocess.run(
                command,
                check=True,
                text=True,
                capture_output=capture_output,
            )

        except subprocess.CalledProcessError as e:

            console.print("[red]✖ ERROR[/red]")

            if e.stderr:
                console.print(e.stderr.strip())

            raise

        console.print("[green]✔ OK[/green]")

        return result
