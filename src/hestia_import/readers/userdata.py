from hestia_import.backup_archive import BackupArchive


class UserdataReader:

    def __init__(self, archive: BackupArchive, root_dir: str):
        self.archive = archive
        self.root_dir = root_dir

    def read(self):

        main = self.archive.read_yaml(
            f"{self.root_dir}/userdata/main"
        )

        if not main:
            return None

        domain = main.get("main_domain")

        data = self.archive.read_yaml(
            f"{self.root_dir}/userdata/{domain}"
        )

        if not data:
            return None

        aliases = []

        if data.get("serveralias"):
            aliases = data["serveralias"].split()

        return {
            "main_domain": domain,
            "addon_domains": list(main.get("addon_domains", {}).keys()),
            "subdomains": main.get("sub_domains", []),
            "aliases": aliases,
            "php_version": data.get("phpversion", ""),
            "ip": data.get("ip", ""),
            "document_root": data.get("documentroot", ""),
            "server_admin": data.get("serveradmin", ""),
            "ssl_enabled": bool(data.get("ssl", 0)),
        }
