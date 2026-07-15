from rich.console import Console

from hestia_import.executor.runner import CommandRunner
from hestia_import.models import (
    MigrationContext,
    MigrationTask,
)
from hestia_import.hestia.client import HestiaClient
from hestia_import.hestia.inspector import HestiaInspector

console = Console()

#
# Acciones que actualmente pueden ejecutarse de forma real.
#
SUPPORTED_ACTIONS = {
    "create_user",
    "create_domain",
    "create_alias",
    "create_mail_account",
}

class HestiaExecutor:
    """
    Convierte las tareas del plan de migración en comandos de HestiaCP.
    """

    def __init__(
        self,
        context: MigrationContext,
        dry_run: bool = True,
    ):

        self.context = context

        self.client = HestiaClient()

        self.inspector = HestiaInspector()

        self.runner = CommandRunner(
            dry_run=dry_run,
        )

        #
        # Tabla de acciones soportadas.
        #
        self.handlers = {
            "create_user": self.create_user,
            "create_domain": self.create_domain,
            "create_alias": self.create_alias,
            "create_mail_account": self.create_mail_account,
            "create_database": self.create_database,
            "restore_web": self.restore_web,
            "restore_mail": self.restore_mail,
            "install_ssl": self.install_ssl,
        }

    def execute(self, task: MigrationTask) -> None:
        """
        Ejecuta (o muestra) una tarea del plan.
        """

        handler = self.handlers.get(task.action)

        if handler is None:
            raise ValueError(f"Acción no soportada: {task.action}")

        command = handler(task.data)

        #
        # Dry Run: mostrar absolutamente todo.
        #
        if self.runner.dry_run:
            self.runner.run(command)
            return

        #
        # Ejecución real solamente para acciones soportadas.
        #
        if task.action in SUPPORTED_ACTIONS:

            #
            # Evitar crear usuarios duplicados.
            #
            if (
                task.action == "create_user"
                and self.inspector.user_exists(task.data["username"])
            ):
                console.print(
                    f"[yellow]SKIP[/yellow] Usuario '{task.data['username']}' ya existe."
                )
                return

            self.runner.run(command)

        else:

            console.print(
                f"[yellow]DRY[/yellow] {' '.join(command)}"
            )
    # ------------------------------------------------------------------
    # Usuario
    # ------------------------------------------------------------------

    def create_user(self, data: dict) -> list[str]:

        return self.client.add_user(
            username=data["username"],
            password=self.context.user_password or "<PASSWORD>",
            email=self.context.admin_email,
            package=self.context.package,
            language=self.context.language,
        )

    # ------------------------------------------------------------------
    # Dominio
    # ------------------------------------------------------------------

    def create_domain(self, data: dict) -> list[str]:

        return self.client.add_domain(
            user=data["user"],
            domain=data["domain"],
        )

    # ------------------------------------------------------------------
    # Alias
    # ------------------------------------------------------------------

    def create_alias(self, data: dict) -> list[str]:

        return self.client.add_alias(
            user=data["user"],
            domain=data["domain"],
            alias=data["alias"],
        )

    # ------------------------------------------------------------------
    # Mail
    # ------------------------------------------------------------------

    def create_mail_account(self, data: dict) -> list[str]:

        return self.client.add_mail_account(
            user=data["user"],
            domain=data["domain"],
            username=data["username"],
            password="<PASSWORD>",
        )

    # ------------------------------------------------------------------
    # MySQL
    # ------------------------------------------------------------------

    def create_database(self, data: dict) -> list[str]:

        return self.client.add_database(
            user=data["user"],
            database=data["database"],
            dbuser="<DBUSER>",
            password="<PASSWORD>",
        )

    # ------------------------------------------------------------------
    # Restaurar sitio
    # ------------------------------------------------------------------

    def restore_web(self, data: dict) -> list[str]:

        return [
            "#",
            "restore_web",
            data["document_root"],
        ]

    # ------------------------------------------------------------------
    # Restaurar Maildir
    # ------------------------------------------------------------------

    def restore_mail(self, data: dict) -> list[str]:

        return [
            "#",
            "restore_mail",
            str(data["accounts"]),
            str(data["messages"]),
        ]

    # ------------------------------------------------------------------
    # SSL
    # ------------------------------------------------------------------

    def install_ssl(self, data: dict) -> list[str]:

        return self.client.install_ssl(
            user=data["user"],
            domain=data["domain"],
        )
