from rich.console import Console

from hestia_import.executor.runner import CommandRunner
from hestia_import.hestia.client import HestiaClient
from hestia_import.mail.account_restore import MailAccountRestorer
from hestia_import.models import MigrationContext

console = Console()


class MailTasks:
    """
    Tareas relacionadas con el correo.
    """

    def __init__(
        self,
        context: MigrationContext,
        client: HestiaClient,
        runner: CommandRunner,
    ):

        self.context = context
        self.client = client
        self.runner = runner

        self.mail_restorer = MailAccountRestorer()

    # ---------------------------------------------------------
    # Crear dominio de correo
    # ---------------------------------------------------------

    def create_mail_domain(self, data: dict):

        return self.client.add_mail_domain(
            user=data["user"],
            domain=data["domain"],
        )

    # ---------------------------------------------------------
    # Crear cuenta
    # ---------------------------------------------------------

    def create_mail_account(self, data: dict):

        return self.client.add_mail_account(
            user=data["user"],
            domain=data["domain"],
            username=data["username"],
            password="<PASSWORD>",
        )

    # ---------------------------------------------------------
    # Restaurar contraseña
    # ---------------------------------------------------------

    def restore_mail_password(self, data: dict):

        if self.runner.dry_run:

            return [
                "#",
                "restore_mail_password",
                data["username"],
            ]

        self.mail_restorer.restore_password(
            user=data["user"],
            domain=data["domain"],
            username=data["username"],
            password_hash=data["password_hash"],
        )

        console.print(
            f"[green]✔[/green] Contraseña restaurada para "
            f"{data['username']}@{data['domain']}"
        )

        return None

    # ---------------------------------------------------------
    # Restaurar Maildir
    # ---------------------------------------------------------

    def restore_maildir(self, data: dict):

        if self.runner.dry_run:

            return [
                "#",
                "restore_maildir",
                data["username"],
            ]

        self.mail_restorer.restore_maildir(
            source=data["source"],
            user=data["user"],
            domain=data["domain"],
            username=data["username"],
        )

        console.print(
            f"[green]✔[/green] Maildir restaurado para "
            f"{data['username']}@{data['domain']}"
        )

        return None
