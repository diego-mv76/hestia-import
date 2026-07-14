import re

from hestia_import.backup_archive import BackupArchive
from hestia_import.models import Database


class MySQLReader:

    def __init__(self, archive: BackupArchive, root_dir: str):
        self.archive = archive
        self.root_dir = root_dir

    def read(self) -> list[Database]:
        """
        Lee el dump mysql.sql y detecta las bases de datos.
        """

        path = f"{self.root_dir}/mysql.sql"

        text = self.archive.read_text(path)

        if not text:
            return []

        databases = {}

        #
        # Buscar CREATE DATABASE
        #
        for line in text.splitlines():

            line = line.strip()

            if not line.upper().startswith("CREATE DATABASE"):
                continue

            #
            # CREATE DATABASE `basedatos`
            #
            match = re.search(r"`([^`]+)`", line)

            if not match:
                continue

            name = match.group(1)

            databases[name] = Database(name=name)

        return sorted(
            databases.values(),
            key=lambda db: db.name
        )
