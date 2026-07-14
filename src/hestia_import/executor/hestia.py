from rich.console import Console

from hestia_import.executor.runner import CommandRunner
from hestia_import.models import MigrationTask

console = Console()


class HestiaExecutor:
    """
    Construye los comandos necesarios para HestiaCP.
    """

    def __init__(self, dry_run: bool = True):

        self.runner = CommandRunner(
            dry_run=dry_run,
        )

    def should_execute(self, action: str) -> bool:
        """
        Define qué acciones ya pueden ejecutarse realmente.
        """

        return action in {
            "create_user",
        }

    def execute(self, task: MigrationTask):

        handlers = {
            "create_user": self.create_user,
            "create_domain": self.create_domain,
            "create_alias": self.create_alias,
            "create_mail_account": self.create_mail_account,
            "create_database": self.create_database,
            "restore_web": self.restore_web,
            "restore_mail": self.restore_mail,
            "install_ssl": self.install_ssl,
        }

        handler = handlers.get(task.action)

        if handler is None:
            raise ValueError(f"Acción no soportada: {task.action}")

        command = handler(task.data)

        #
        # Si estamos en Dry Run, mostrar todo.
        #
        if self.runner.dry_run:
            self.runner.run(command)
            return

        #
        # En ejecución real, solo ejecutar las acciones soportadas.
        #
        if self.should_execute(task.action):
            self.runner.run(command)
        else:
            console.print(
                f"[yellow]DRY[/yellow] {' '.join(command)}"
            )

    #
    # Usuario
    #

    def create_user(self, data: dict) -> list[str]:

        return [
            "v-add-user",
            data["username"],
            "<PASSWORD>",
            "admin@example.com",
            "default",
            "default",
        ]

    #
    # Dominio
    #

    def create_domain(self, data: dict) -> list[str]:

        return [
            "v-add-web-domain",
            data["user"],
            data["domain"],
        ]

    #
    # Alias
    #

    def create_alias(self, data: dict) -> list[str]:

        return [
            "v-add-web-domain-alias",
            data["user"],
            data["domain"],
            data["alias"],
        ]

    #
    # Mail
    #

    def create_mail_account(self, data: dict) -> list[str]:

        return [
            "v-add-mail-account",
            data["user"],
            data["domain"],
            data["username"],
            "<PASSWORD>",
        ]

    #
    # MySQL
    #

    def create_database(self, data: dict) -> list[str]:

        return [
            "v-add-database",
            data["user"],
            data["database"],
            "<DBUSER>",
            "<PASSWORD>",
        ]

    #
    # Restaurar sitio
    #

    def restore_web(self, data: dict) -> list[str]:

        return [
            "#",
            "restore_web",
            data["document_root"],
        ]

    #
    # Restaurar Maildir
    #

    def restore_mail(self, data: dict) -> list[str]:

        return [
            "#",
            "restore_mail",
            str(data["accounts"]),
            str(data["messages"]),
        ]

    #
    # SSL
    #

    def install_ssl(self, data: dict) -> list[str]:

        return [
            "v-add-letsencrypt-domain",
            data["user"],
            data["domain"],
        ]
