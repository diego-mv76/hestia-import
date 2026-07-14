from hestia_import.backup_archive import BackupArchive
from hestia_import.models import MailAccount


class MailReader:

    def __init__(self, archive: BackupArchive, root_dir: str):
        self.archive = archive
        self.root_dir = root_dir

    def read(self) -> list[MailAccount]:

        accounts = {}

        domains = self._find_domains()

        for domain in domains:

            self._read_passwd(domain, accounts)
            self._read_shadow(domain, accounts)
            self._read_quota(domain, accounts)
            self._read_maildir(domain, accounts)

        return sorted(
            accounts.values(),
            key=lambda x: (x.domain, x.username)
        )

    def _find_domains(self) -> list[str]:
        """
        Busca dominios que tengan configuración de correo.

        Un dominio válido es aquel que posee:
            homedir/etc/<dominio>/passwd
        """

        prefix = f"{self.root_dir}/homedir/etc/"

        domains = set()

        for member in self.archive.walk(prefix):

            relative = member.name[len(prefix):].strip("/")

            if not relative:
                continue

            parts = relative.split("/")

            if len(parts) != 2:
                continue

            domain = parts[0]
            filename = parts[1]

            if filename != "passwd":
                continue

            domains.add(domain)

        return sorted(domains)

    def _read_passwd(self, domain: str, accounts: dict):

        path = f"{self.root_dir}/homedir/etc/{domain}/passwd"

        text = self.archive.read_text(path)

        if not text:
            return

        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            fields = line.split(":")

            if len(fields) < 7:
                continue

            username = fields[0]
            home = fields[5]

            accounts[(domain, username)] = MailAccount(
                username=username,
                domain=domain,
                home=home,
            )

    def _read_shadow(self, domain: str, accounts: dict):

        path = f"{self.root_dir}/homedir/etc/{domain}/shadow"

        text = self.archive.read_text(path)

        if not text:
            return

        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            fields = line.split(":")

            if len(fields) < 2:
                continue

            username = fields[0]
            password_hash = fields[1]

            key = (domain, username)

            if key in accounts:
                accounts[key].password_hash = password_hash

    def _read_quota(self, domain: str, accounts: dict):

        path = f"{self.root_dir}/homedir/etc/{domain}/quota"

        text = self.archive.read_text(path)

        #
        # Algunos backups no poseen este archivo
        #
        if text is None:
            return

        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            fields = line.split(":")

            if len(fields) < 2:
                continue

            username = fields[0]
            quota = fields[1]

            key = (domain, username)

            if key in accounts:
                accounts[key].quota = quota

    def _read_maildir(self, domain: str, accounts: dict):
        """
        Analiza el Maildir para obtener:

        - cantidad de mensajes
        - tamaño ocupado
        - carpetas IMAP
        """

        prefix = f"{self.root_dir}/homedir/mail/{domain}/"

        for member in self.archive.walk(prefix):

            relative = member.name[len(prefix):].strip("/")

            if not relative:
                continue

            parts = relative.split("/")

            #
            # Debe ser:
            #
            # usuario/...
            #
            if len(parts) < 2:
                continue

            username = parts[0]

            key = (domain, username)

            if key not in accounts:
                continue

            account = accounts[key]

            #
            # Detectar carpetas IMAP
            #
            if len(parts) == 2 and member.isdir():

                folder = parts[1]

                if folder.startswith("."):

                    folder = folder[1:]

                    if folder not in account.folders:
                        account.folders.append(folder)

            #
            # Contar mensajes
            #
            if member.isfile():

                if "/cur/" in member.name or "/new/" in member.name:
                    account.messages += 1
                    account.size_bytes += member.size
