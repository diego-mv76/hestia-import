from pathlib import Path

from hestia_import.mail.maildir import MaildirRestorer
from hestia_import.mail.passwords import MailPasswordRestorer


class MailAccountRestorer:
    """
    Orquesta la restauración de una cuenta de correo.
    """

    def __init__(self):

        self.passwords = MailPasswordRestorer()

        self.maildir = MaildirRestorer()

    # ---------------------------------------------------------
    # Contraseña
    # ---------------------------------------------------------

    def restore_password(
        self,
        user: str,
        domain: str,
        username: str,
        password_hash: str,
    ) -> None:

        passwd_file = (
            Path("/home")
            / user
            / "conf"
            / "mail"
            / domain
            / "passwd"
        )

        self.passwords.restore(
            passwd_file=str(passwd_file),
            username=username,
            password_hash=password_hash,
        )

    # ---------------------------------------------------------
    # Maildir
    # ---------------------------------------------------------

    def restore_maildir(
        self,
        source: str,
        user: str,
        domain: str,
        username: str,
    ) -> None:

        destination = (
            Path("/home")
            / user
            / "mail"
            / domain
            / username
        )

        self.maildir.restore(
            source=source,
            destination=str(destination),
        )
