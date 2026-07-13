from dataclasses import dataclass, field


@dataclass
class MailAccount:
    username: str
    domain: str


@dataclass
class BackupInfo:
    # Información básica
    filename: str
    size: int
    username: str
    root_dir: str

    # Dominio principal
    main_domain: str = ""
    php_version: str = ""
    ip: str = ""
    document_root: str = ""
    server_admin: str = ""
    ssl_enabled: bool = False

    # Dominios
    aliases: list[str] = field(default_factory=list)
    addon_domains: list[str] = field(default_factory=list)
    subdomains: list[str] = field(default_factory=list)

    # Correo
    mail_accounts: list[MailAccount] = field(default_factory=list)
