from pathlib import Path
import shutil


class MailPasswordRestorer:
    """
    Restaura el hash original de una cuenta de correo
    dentro del archivo passwd de Hestia.

    Características:

      - Verifica que el archivo exista.
      - Verifica que el usuario exista.
      - Genera un backup (.bak) automáticamente.
      - Escribe mediante un archivo temporal.
      - Reemplaza el archivo de forma atómica.
    """

    def restore(
        self,
        passwd_file: str,
        username: str,
        password_hash: str,
    ) -> None:

        passwd_path = Path(passwd_file)

        if not passwd_path.exists():
            raise FileNotFoundError(
                f"No existe el archivo: {passwd_file}"
            )

        #
        # Backup automático
        #
        backup_path = passwd_path.with_suffix(
            passwd_path.suffix + ".bak"
        )

        shutil.copy2(
            passwd_path,
            backup_path,
        )

        lines = passwd_path.read_text().splitlines()

        new_lines = []

        found = False

        for line in lines:

            if not line.startswith(username + ":"):
                new_lines.append(line)
                continue

            found = True

            parts = line.split(":")

            #
            # Campo 2 = hash de contraseña
            #
            parts[1] = "{SHA512-CRYPT}" + password_hash

            new_lines.append(
                ":".join(parts)
            )

        if not found:
            raise ValueError(
                f"No se encontró la cuenta '{username}' en '{passwd_file}'."
            )

        #
        # Escritura segura mediante archivo temporal
        #
        tmp_path = passwd_path.with_suffix(
            passwd_path.suffix + ".tmp"
        )

        tmp_path.write_text(
            "\n".join(new_lines) + "\n"
        )

        #
        # Preservar permisos del archivo original
        #
        shutil.copymode(
            passwd_path,
            tmp_path,
        )

        #
        # Reemplazo atómico
        #
        tmp_path.replace(
            passwd_path
        )
