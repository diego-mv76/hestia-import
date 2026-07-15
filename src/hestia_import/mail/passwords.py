from pathlib import Path


class MailPasswordRestorer:
    """
    Restaura el hash original de las cuentas de correo
    dentro del archivo passwd de Hestia.
    """

    def restore(
        self,
        passwd_file: str,
        username: str,
        password_hash: str,
    ) -> None:

        passwd_path = Path(passwd_file)

        if not passwd_path.exists():
            raise FileNotFoundError(passwd_file)

        lines = passwd_path.read_text().splitlines()

        new_lines = []

        for line in lines:

            if not line.startswith(username + ":"):
                new_lines.append(line)
                continue

            parts = line.split(":")

            #
            # Campo 2 = password
            #
            parts[1] = "{SHA512-CRYPT}" + password_hash

            new_lines.append(":".join(parts))

        passwd_path.write_text(
            "\n".join(new_lines) + "\n"
        )
