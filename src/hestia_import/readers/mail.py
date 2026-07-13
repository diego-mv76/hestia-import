from hestia_import.backup_archive import BackupArchive
from hestia_import.models import MailAccount


class MailReader:

    def __init__(self, archive: BackupArchive, root_dir: str):
        self.archive = archive
        self.root_dir = root_dir

    def read(self) -> list[MailAccount]:

        accounts = {}

        prefix = f"{self.root_dir}/homedir/mail/"

        for member in self.archive.walk(prefix):

            if not member.isdir():
                continue

            relative = member.name[len(prefix):].strip("/")

            if not relative:
                continue

            parts = relative.split("/")

            #
            # Solo aceptamos:
            #
            # dominio/cuenta
            #
            # Ejemplo:
            # reprearg.com/marianoines
            #
            if len(parts) != 2:
                continue

            domain = parts[0]
            username = parts[1]

            #
            # Ignorar carpetas ocultas
            #
            if domain.startswith("."):
                continue

            if username.startswith("."):
                continue

            #
            # Debe ser un dominio válido
            #
            if "." not in domain:
                continue

            accounts[(domain, username)] = MailAccount(
                username=username,
                domain=domain,
            )

        return sorted(
            accounts.values(),
            key=lambda x: (x.domain, x.username)
        )
