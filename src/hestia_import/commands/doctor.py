import os
import shutil

import typer
from rich.console import Console

console = Console()


def doctor():
    """
    Verifica que el servidor esté listo para realizar migraciones.
    """

    console.rule("[bold green]Diagnóstico del Servidor")

    #
    # Root
    #
    if os.geteuid() == 0:
        console.print("[green]✔ Ejecutándose como root[/green]")
    else:
        console.print("[red]✘ Debe ejecutarse como root[/red]")

    #
    # Hestia
    #
    if os.path.isdir("/usr/local/hestia"):
        console.print("[green]✔ HestiaCP detectado[/green]")
    else:
        console.print("[red]✘ No se encontró HestiaCP[/red]")

    #
    # Comandos Hestia
    #
    commands = [
        "v-add-user",
        "v-add-web-domain",
        "v-add-web-domain-alias",
        "v-add-mail-account",
        "v-add-database",
        "v-add-letsencrypt-domain",
    ]

    console.print()

    for cmd in commands:

        path = shutil.which(cmd)

        if path:
            console.print(f"[green]✔ {cmd}[/green] ({path})")
        else:
            console.print(f"[red]✘ {cmd}[/red]")

    #
    # Herramientas necesarias
    #
    console.print()

    for cmd in [
        "tar",
        "rsync",
    ]:

        path = shutil.which(cmd)

        if path:
            console.print(f"[green]✔ {cmd}[/green] ({path})")
        else:
            console.print(f"[yellow]⚠ {cmd} no encontrado[/yellow]")
