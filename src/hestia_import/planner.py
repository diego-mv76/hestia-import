from hestia_import.models import (
    BackupInfo,
    MigrationPlan,
    MigrationTask,
)


class MigrationPlanner:
    """
    Genera el plan de migración a partir del BackupInfo.
    """

    def create_plan(self, info: BackupInfo) -> MigrationPlan:

        plan = MigrationPlan()

        #
        # Usuario
        #
        plan.tasks.append(
            MigrationTask(
                action="create_user",
                description=f"Crear usuario '{info.username}'",
                data={
                    "username": info.username,
                },
            )
        )

        #
        # Dominio principal
        #
        plan.tasks.append(
            MigrationTask(
                action="create_domain",
                description=f"Crear dominio '{info.main_domain}'",
                data={
                    "user": info.username,
                    "domain": info.main_domain,
                    "ip": info.ip,
                    "php": info.php_version,
                },
            )
        )

        #
        # Alias
        #
        for alias in info.aliases:

            plan.tasks.append(
                MigrationTask(
                    action="create_alias",
                    description=f"Agregar alias '{alias}'",
                    data={
                        "user": info.username,
                        "domain": info.main_domain,
                        "alias": alias,
                    },
                )
            )

        #
        # Cuentas de correo
        #
        for account in info.mail_accounts:

            plan.tasks.append(
                MigrationTask(
                    action="create_mail_account",
                    description=f"Crear cuenta {account.username}@{account.domain}",
                    data={
                        "user": info.username,
                        "username": account.username,
                        "domain": account.domain,
                        "password_hash": account.password_hash,
                        "quota": account.quota,
                        "home": account.home,
                    },
                )
            )

        #
        # Restaurar contraseña original
        #
            plan.tasks.append(
                MigrationTask(
                    action="restore_mail_password",
                    description=f"Restaurar contraseña de {account.username}@{account.domain}",
                    data={
                        "user": info.username,
                        "username": account.username,
                        "domain": account.domain,
                        "password_hash": account.password_hash,
                    },
                )
            )

        #
        # Bases MySQL
        #
        for db in info.databases:

            plan.tasks.append(
                MigrationTask(
                    action="create_database",
                    description=f"Crear base '{db.name}'",
                    data={
                        "user": info.username,
                        "database": db.name,
                        "users": db.users,
                    },
                )
            )

        #
        # Restaurar sitio
        #
        plan.tasks.append(
            MigrationTask(
                action="restore_web",
                description="Restaurar archivos del sitio web",
                data={
                    "user": info.username,
                    "document_root": info.document_root,
                },
            )
        )

        #
        # Restaurar correo
        #
        if info.mail_accounts:

            plan.tasks.append(
                MigrationTask(
                    action="restore_mail",
                    description="Restaurar Maildir",
                    data={
                        "user": info.username,
                        "accounts": len(info.mail_accounts),
                        "messages": info.total_messages,
                    },
                )
            )

        #
        # SSL
        #
        if info.ssl_enabled:

            plan.tasks.append(
                MigrationTask(
                    action="install_ssl",
                    description="Instalar certificado SSL",
                    data={
                        "user": info.username,
                        "domain": info.main_domain,
                    },
                )
            )

        return plan
