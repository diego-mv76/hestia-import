import subprocess


class HestiaInspector:
    """
    Permite consultar el estado actual de HestiaCP.

    No modifica nada.
    Solamente verifica la existencia de recursos.
    """

    def user_exists(self, username: str) -> bool:
        """
        Verifica si un usuario existe.
        """

        result = subprocess.run(
            [
                "v-list-user",
                username,
                "json",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        return result.returncode == 0
