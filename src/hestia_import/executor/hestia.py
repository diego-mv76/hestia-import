from rich.console import Console

from hestia_import.executor.runner import CommandRunner
from hestia_import.hestia.client import HestiaClient
from hestia_import.hestia.inspector import HestiaInspector
from hestia_import.mail.account_restore import MailAccountRestorer
from hestia_import.models import (
    MigrationContext,
    MigrationTask,
)

from hestia_import.tasks.mail import MailTasks

console = Console()


class HestiaExecutor:
    """
    Convierte una MigrationTask en una acción.
    """

    def __init__(
        self,
        context: MigrationContext,
        dry_run: bool = True,
    ):

        self.context = context

        self.client = HestiaClient()

        self.inspector = HestiaInspector()

        self.mail_restorer = MailAccountRestorer()
        
        self.runner = CommandRunner(
            dry_run=dry_run,
        )

        self.mail = MailTasks(
            context=self.context,
            client=self.client,
            runner=self.runner,
        )

        self.handlers = {
            "create_user": self.create_user,
            "create_domain": self.create_domain,
            "create_mail_domain": self.mail.create_mail_domain,
            "create_alias": self.create_alias,
            "create_mail_account": self.mail.create_mail_account,
            "restore_mail_password": self.mail.restore_mail_password,
            "restore_maildir": self.mail.restore_maildir,
            "create_database": self.create_database,
            "restore_web": self.restore_web,
            "install_ssl": self.install_ssl,
        }

    def execute(
        self,
        task: MigrationTask,
        plan,
    ) -> None:

        #
        # Evitar recrear recursos existentes
        #
        if task.action == "create_user":

            if self.inspector.user_exists(
                task.data["username"]
            ):

                console.print(
                    f"[yellow]⏭ Usuario '{task.data['username']}' ya existe.[/yellow]"
                )
                return

        elif task.action == "create_domain":

            if self.inspector.web_domain_exists(
                task.data["user"],
                task.data["domain"],
            ):

                console.print(
                    f"[yellow]⏭ Dominio '{task.data['domain']}' ya existe.[/yellow]"
                )
                return

        elif task.action == "create_mail_domain":

            if self.inspector.mail_domain_exists(
                task.data["user"],
                task.data["domain"],
            ):

                console.print(
                    f"[yellow]⏭ Dominio de correo '{task.data['domain']}' ya existe.[/yellow]"
                )
                return

        handler = self.handlers.get(task.action)

        if handler is None:
            raise ValueError(
                f"Acción no soportada: {task.action}"
            )

        result = handler(task.data)

        if result is None:
            return

        self.runner.run(result)

    # ---------------------------------------------------------
    # Usuario
    # ---------------------------------------------------------

    def create_user(self, data: dict):

        return self.client.add_user(
            username=data["username"],
            password=self.context.user_password or "<PASSWORD>",
            email=self.context.admin_email,
            package=self.context.package,
            language=self.context.language,
        )

    # ---------------------------------------------------------
    # Dominio Web
    # ---------------------------------------------------------

    def create_domain(self, data: dict):

        return self.client.add_domain(
            user=data["user"],
            domain=data["domain"],
        )

    # ---------------------------------------------------------
    # Dominio Mail
    # ---------------------------------------------------------

    def create_mail_domain(self, data: dict):

        return self.client.add_mail_domain(
            user=data["user"],
            domain=data["domain"],
        )

    # ---------------------------------------------------------
    # Alias
    # ---------------------------------------------------------

    def create_alias(self, data: dict):

        return self.client.add_alias(
            user=data["user"],
            domain=data["domain"],
            alias=data["alias"],
        )

    # ---------------------------------------------------------
    # Cuenta Mail
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

    # ---------------------------------------------------------
    # Base MySQL
    # ---------------------------------------------------------

    def create_database(self, data: dict):

        return self.client.add_database(
            user=data["user"],
            database=data["database"],
            dbuser="<DBUSER>",
            password="<PASSWORD>",
        )

    # ---------------------------------------------------------
    # Restaurar Web
    # ---------------------------------------------------------

    def restore_web(self, data: dict):

        return [
            "#",
            "restore_web",
            data["document_root"],
        ]

    # ---------------------------------------------------------
    # SSL
    # ---------------------------------------------------------

    def install_ssl(self, data: dict):

        return self.client.install_ssl(
            user=data["user"],
            domain=data["domain"],
        )
