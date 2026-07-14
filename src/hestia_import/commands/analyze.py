import typer
from rich.console import Console

from hestia_import.parser import CPanelBackupParser

console = Console()


def analyze(backup: str):
    """Analizar un backup de cPanel."""

    try:

        parser = CPanelBackupParser(backup)
        info = parser.analyze()

        #
        # Información general
        #
        console.rule("[bold green]Información del Backup")

        console.print(f"[cyan]Archivo:[/cyan]          {info.filename}")
        console.print(f"[cyan]Usuario:[/cyan]         {info.username}")
        console.print(f"[cyan]Directorio:[/cyan]      {info.root_dir}")
        console.print(
            f"[cyan]Tamaño:[/cyan]           {round(info.size / 1024 / 1024, 2)} MB"
        )

        #
        # Sitio web
        #
        console.print()
        console.rule("[bold blue]Sitio Web")

        console.print(f"[cyan]Dominio:[/cyan]          {info.main_domain}")
        console.print(f"[cyan]PHP:[/cyan]              {info.php_version}")
        console.print(f"[cyan]IP:[/cyan]               {info.ip}")
        console.print(f"[cyan]DocumentRoot:[/cyan]     {info.document_root}")
        console.print(f"[cyan]ServerAdmin:[/cyan]      {info.server_admin}")
        console.print(
            f"[cyan]SSL:[/cyan]              {'Sí' if info.ssl_enabled else 'No'}"
        )

        if info.aliases:
            console.print()
            console.print("[cyan]Aliases:[/cyan]")

            for alias in info.aliases:
                console.print(f"  • {alias}")

        #
        # Correo
        #
        console.print()
        console.rule("[bold blue]Correo")

        if info.mail_accounts:

            console.print(f"Dominio: {info.main_domain}")
            console.print()

            for account in sorted(info.mail_accounts, key=lambda x: x.username):

                console.print(
                    f"[bold green]✔ {account.username}@{account.domain}[/bold green]"
                )

                if account.home:
                    console.print(f"    Home.......... {account.home}")

                if account.password_hash:
                    console.print("    Password...... SHA512")

                if account.quota:
                    console.print(f"    Quota......... {account.quota}")
                else:
                    console.print("    Quota......... Unlimited")

                console.print(f"    Mensajes...... {account.messages}")
                console.print(f"    Carpetas...... {len(account.folders)}")

                size_mb = account.size_bytes / 1024 / 1024

                console.print(f"    Tamaño........ {size_mb:.2f} MB")
                console.print()

            console.print(
                f"[bold cyan]Total de cuentas:[/bold cyan] {len(info.mail_accounts)}"
            )

        else:
            console.print("[yellow]No se encontraron cuentas de correo.[/yellow]")

        #
        # MySQL
        #
        console.print()
        console.rule("[bold blue]MySQL")

        if info.databases:

            for db in info.databases:

                console.print(f"[bold green]✔ {db.name}[/bold green]")

                if db.users:
                    console.print(f"    Usuarios...... {', '.join(db.users)}")

                if db.tables:
                    console.print(f"    Tablas........ {db.tables}")

                if db.size_bytes:
                    size_mb = db.size_bytes / 1024 / 1024
                    console.print(f"    Tamaño........ {size_mb:.2f} MB")

                console.print()

            console.print(
                f"[bold cyan]Total de bases:[/bold cyan] {info.total_databases}"
            )

        else:
            console.print("[yellow]No se encontraron bases de datos.[/yellow]")

        #
        # Resumen
        #
        console.print()
        console.rule("[bold magenta]Resumen")

        console.print(f"[cyan]Dominios:[/cyan]         {info.total_domains}")
        console.print(f"[cyan]Cuentas:[/cyan]         {info.total_mail_accounts}")
        console.print(f"[cyan]Mensajes:[/cyan]        {info.total_messages}")

        total_gb = info.total_mail_size / 1024 / 1024 / 1024

        console.print(f"[cyan]Correo:[/cyan]          {total_gb:.2f} GB")
        console.print(f"[cyan]Bases MySQL:[/cyan]    {info.total_databases}")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
