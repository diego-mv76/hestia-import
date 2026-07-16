from pathlib import Path
import os
import shutil

from hestia_import.backup_archive import BackupArchive


class ArchiveExtractor:
    """
    Extrae archivos o directorios desde un BackupArchive
    sin descomprimir todo el backup.
    """

    def __init__(self, archive: BackupArchive):

        self.archive = archive

    # ---------------------------------------------------------
    # Extraer un directorio completo
    # ---------------------------------------------------------

    def extract_tree(
        self,
        source: str,
        destination: str,
    ) -> None:

        destination_path = Path(destination)

        if destination_path.exists():
            shutil.rmtree(destination_path)

        destination_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        prefix = source.rstrip("/") + "/"

        for member in self.archive.walk(prefix):

            relative = member.name[len(prefix):]

            target = destination_path / relative

            if member.isdir():

                target.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                continue

            target.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with self.archive.tar.extractfile(member) as src:

                with open(target, "wb") as dst:

                    shutil.copyfileobj(src, dst)

            #
            # Preservar permisos
            #
            os.chmod(
                target,
                member.mode,
            )
