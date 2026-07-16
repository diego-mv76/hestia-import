from dataclasses import dataclass, field
from typing import Any


@dataclass
class MailAccount:
    username: str
    domain: str

    #
    # Ruta del Maildir (home de la cuenta)
    #
    home: str = ""

    #
    # Ruta del Maildir dentro del backup cPanel
    #
    maildir_source: str = ""

    #
    # Hash SHA512 del archivo shadow
    #
    password_hash: str = ""

    #
    # Cuota configurada
    #
    quota: str = ""

    #
    # Estadísticas del buzón
    #
    messages: int = 0
    size_bytes: int = 0
    folders: list[str] = field(default_factory=list)


@dataclass
class Database:
    """
    Base de datos encontrada en el backup.
    """

    name: str

    users: list[str] = field(default_factory=list)

    size_bytes: int = 0

    tables: int = 0


@dataclass
class MigrationTask:
    """
    Una tarea del plan de migración.
    """

    action: str

    description: str

    #
    # Datos que utilizará el importador
    #
    data: dict[str, Any] = field(default_factory=dict)


@dataclass
class MigrationPlan:
    """
    Plan completo de migración.
    """

    tasks: list[MigrationTask] = field(default_factory=list)


@dataclass
class BackupInfo:

    #
    # Información básica
    #
    filename: str
    size: int
    username: str
    root_dir: str

    #
    # Sitio web
    #
    main_domain: str = ""
    php_version: str = ""
    ip: str = ""
    document_root: str = ""
    server_admin: str = ""
    ssl_enabled: bool = False

    #
    # Dominios
    #
    aliases: list[str] = field(default_factory=list)
    addon_domains: list[str] = field(default_factory=list)
    subdomains: list[str] = field(default_factory=list)

    #
    # Correo
    #
    mail_accounts: list[MailAccount] = field(default_factory=list)

    #
    # Bases MySQL
    #
    databases: list[Database] = field(default_factory=list)

    #
    # Resumen global
    #
    total_domains: int = 0
    total_mail_accounts: int = 0
    total_messages: int = 0
    total_mail_size: int = 0
    total_databases: int = 0


@dataclass
class MigrationContext:
    """
    Configuración del destino de la migración.
    """

    #
    # Email del administrador de Hestia
    #
    admin_email: str = "admin@example.com"

    #
    # Contraseña inicial del usuario
    #
    user_password: str = ""

    #
    # Paquete de Hestia
    #
    package: str = "default"

    #
    # Idioma del usuario
    #
    language: str = "en"
