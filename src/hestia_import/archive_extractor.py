from pathlib import Path
import os
import shutil
import tarfile

from hestia_import.backup_archive import BackupArchive


class ArchiveExtractor:
    """
    Extrae archivos y directorios desde un backup TAR
    sin necesidad de descomprimirlo completamente.
    """

    def __init__(self, backup_file: str):

        self.backup_file = backup_file

    # ---------------------------------------------------------
    # Abrir backup
    # ---------------------------------------------------------

    def _open_archive(self) -> BackupArchive:

        tar = tarfile.open(
            self.backup_file,
            "r:*",
        )

        archive = BackupArchive(tar)

        #
        # Devolvemos ambos para poder cerrar el TAR luego.
        #
        return archive

    # ---------------------------------------------------------
    # Verificar existencia
    # ---------------------------------------------------------

    def exists(self, path: str) -> bool:

        tar = tarfile.open(self.backup_file, "r:*")

        try:

            archive = BackupArchive(tar)

            return archive.exists(path)

        finally:

            tar.close()

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

        tar = tarfile.open(
            self.backup_file,
            "r:*",
        )

        try:

            archive = BackupArchive(tar)

            prefix = source.rstrip("/") + "/"

            for member in archive.walk(prefix):

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

                src = tar.extractfile(member)

                if src is None:
                    continue

                with src:

                    with open(target, "wb") as dst:

                        shutil.copyfileobj(
                            src,
                            dst,
                        )

                #
                # Permisos
                #
                os.chmod(
                    target,
                    member.mode,
                )

        finally:

            tar.close()

    # ---------------------------------------------------------
    # Extraer un único archivo
    # ---------------------------------------------------------

    def extract_file(
        self,
        source: str,
        destination: str,
    ) -> None:

        tar = tarfile.open(
            self.backup_file,
            "r:*",
        )

        try:

            archive = BackupArchive(tar)

            if not archive.exists(source):
                raise FileNotFoundError(source)

            member = archive.members[source]

            fp = tar.extractfile(member)

            if fp is None:
                raise FileNotFoundError(source)

            destination_path = Path(destination)

            destination_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with fp:

                with open(destination_path, "wb") as out:

                    shutil.copyfileobj(
                        fp,
                        out,
                    )

            os.chmod(
                destination_path,
                member.mode,
            )

        finally:

            tar.close()
