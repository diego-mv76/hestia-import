import tarfile

from hestia_import.models import MailAccount


class MailReader:

    def __init__(self, tar: tarfile.TarFile, root_dir: str):
        self.tar = tar
        self.root_dir = root_dir

    def read(self) -> list[MailAccount]:

        accounts = {}

        prefix = f"{self.root_dir}/homedir/mail/"

        for member in self.tar.getmembers():

            if not member.isdir():
                continue

            if not member.name.startswith(prefix):
                continue

            relative = member.name[len(prefix):].strip("/")

            if not relative:
                continue

            parts = relative.split("/")

            #
            # Solo aceptamos:
            #
            # homedir/mail/dominio/cuenta
            #
            # Ejemplo:
            #   reprearg.com/marianoines
            #
            if len(parts) != 2:
                continue

            domain = parts[0]
            username = parts[1]

            #
            # El primer nivel debe ser un dominio
            #
            if "." not in domain:
                continue

            #
            # Ignorar carpetas ocultas
            #
            if domain.startswith("."):
                continue

            if username.startswith("."):
                continue

            accounts[(domain, username)] = MailAccount(
                username=username,
                domain=domain,
            )

        return sorted(
            accounts.values(),
            key=lambda x: (x.domain, x.username)
        )
