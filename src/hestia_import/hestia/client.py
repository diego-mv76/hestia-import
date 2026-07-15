class HestiaClient:
    """
    Construye los comandos de HestiaCP.

    No ejecuta comandos.
    """

    def add_user(
        self,
        username: str,
        password: str,
        email: str,
        package: str,
        language: str,
    ) -> list[str]:

        return [
            "v-add-user",
            username,
            password,
            email,
            package,
            language,
        ]

    def add_domain(
        self,
        user: str,
        domain: str,
    ) -> list[str]:

        return [
            "v-add-web-domain",
            user,
            domain,
        ]

    def add_alias(
        self,
        user: str,
        domain: str,
        alias: str,
    ) -> list[str]:

        return [
            "v-add-web-domain-alias",
            user,
            domain,
            alias,
        ]

    def add_mail_account(
        self,
        user: str,
        domain: str,
        username: str,
        password: str,
    ) -> list[str]:

        return [
            "v-add-mail-account",
            user,
            domain,
            username,
            password,
        ]

    def add_database(
        self,
        user: str,
        database: str,
        dbuser: str,
        password: str,
    ) -> list[str]:

        return [
            "v-add-database",
            user,
            database,
            dbuser,
            password,
        ]

    def install_ssl(
        self,
        user: str,
        domain: str,
    ) -> list[str]:

        return [
            "v-add-letsencrypt-domain",
            user,
            domain,
        ]
