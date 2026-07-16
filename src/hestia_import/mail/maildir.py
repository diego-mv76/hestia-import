from pathlib import Path
import shutil


class MaildirRestorer:
    """
    Restaura el Maildir de una cuenta de correo.
    """

    def restore(
        self,
        source: str,
        destination: str,
    ) -> None:

        source_path = Path(source)
        destination_path = Path(destination)

        if not source_path.exists():
            raise FileNotFoundError(source)

        if destination_path.exists():
            shutil.rmtree(destination_path)

        shutil.copytree(
            source_path,
            destination_path,
            symlinks=True,
        )
