import subprocess


class HestiaInspector:
    """
    Permite consultar el estado actual de HestiaCP.

    No modifica nada.
    Solamente verifica la existencia de recursos.
    """

    # ---------------------------------------------------------
    # Usuario
    # ---------------------------------------------------------

    def user_exists(
        self,
        username: str,
    ) -> bool:

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

    # ---------------------------------------------------------
    # Dominio Web
    # ---------------------------------------------------------

    def web_domain_exists(
        self,
        user: str,
        domain: str,
    ) -> bool:

        result = subprocess.run(
            [
                "v-list-web-domain",
                user,
                domain,
                "json",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        return result.returncode == 0

    # ---------------------------------------------------------
    # Dominio Mail
    # ---------------------------------------------------------

    def mail_domain_exists(
        self,
        user: str,
        domain: str,
    ) -> bool:

        result = subprocess.run(
            [
                "v-list-mail-domain",
                user,
                domain,
                "json",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        return result.returncode == 0
