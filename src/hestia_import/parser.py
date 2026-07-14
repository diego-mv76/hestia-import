import os
import tarfile

from hestia_import.backup_archive import BackupArchive
from hestia_import.models import BackupInfo
from hestia_import.readers.mail import MailReader
from hestia_import.readers.userdata import UserdataReader
from hestia_import.readers.mysql import MySQLReader


class CPanelBackupParser:

    def __init__(self, backup_file: str):
        self.backup_file = backup_file

    def analyze(self) -> BackupInfo:

        if not os.path.exists(self.backup_file):
            raise FileNotFoundError(self.backup_file)

        if not tarfile.is_tarfile(self.backup_file):
            raise Exception("El archivo no es un backup TAR válido.")

        size = os.path.getsize(self.backup_file)

        with tarfile.open(self.backup_file, "r:*") as tar:

            members = tar.getmembers()

            if not members:
                raise Exception("El backup está vacío.")

            root = members[0].name.split("/")[0]

            if not root.startswith("cpmove-"):
                raise Exception("No parece un backup de cPanel.")

            username = root.replace("cpmove-", "", 1)

            #
            # Nueva capa de acceso al backup
            #
            archive = BackupArchive(tar)

            info = BackupInfo(
                filename=os.path.basename(self.backup_file),
                size=size,
                username=username,
                root_dir=root,
            )

            #
            # Información del dominio
            #
            userdata = UserdataReader(archive, root).read()

            if userdata:
                info.main_domain = userdata["main_domain"]
                info.php_version = userdata["php_version"]
                info.ip = userdata["ip"]
                info.document_root = userdata["document_root"]
                info.server_admin = userdata["server_admin"]
                info.ssl_enabled = userdata["ssl_enabled"]

                info.aliases = userdata["aliases"]
                info.addon_domains = userdata["addon_domains"]
                info.subdomains = userdata["subdomains"]

            #
            # Correo
            #
            info.mail_accounts = MailReader(
                archive,
                root,
            ).read()

            #
            # MySQL
            #
            info.databases = MySQLReader(
                archive,
                root,
            ).read()

            #
            # Resumen global
            #
            info.total_domains = 1 + len(info.addon_domains)

            info.total_mail_accounts = len(info.mail_accounts)

            info.total_messages = sum(
                account.messages
                for account in info.mail_accounts
            )

            info.total_mail_size = sum(
                account.size_bytes
                for account in info.mail_accounts
            )

            return info
