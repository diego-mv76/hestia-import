import tarfile
import yaml


class UserdataReader:
    def __init__(self, tar: tarfile.TarFile, root_dir: str):
        self.tar = tar
        self.root_dir = root_dir

    def _read_yaml(self, path: str):
        """Lee un archivo YAML dentro del backup."""
        try:
            member = self.tar.getmember(path)
        except KeyError:
            return None

        with self.tar.extractfile(member) as fp:
            if fp is None:
                return None

            data = fp.read().decode("utf-8", errors="ignore")
            return yaml.safe_load(data)

    def read(self):
        """
        Lee userdata/main y userdata/<dominio>.
        Devuelve un diccionario con la información encontrada.
        """

        main = self._read_yaml(f"{self.root_dir}/userdata/main")

        if not main:
            return None

        dominio = main.get("main_domain")

        domain_data = self._read_yaml(
            f"{self.root_dir}/userdata/{dominio}"
        )

        if not domain_data:
            return None

        aliases = []

        if domain_data.get("serveralias"):
            aliases = domain_data["serveralias"].split()

        return {
            "main_domain": dominio,
            "addon_domains": list(main.get("addon_domains", {}).keys()),
            "subdomains": main.get("sub_domains", []),
            "aliases": aliases,
            "php_version": domain_data.get("phpversion", ""),
            "ip": domain_data.get("ip", ""),
            "document_root": domain_data.get("documentroot", ""),
            "server_admin": domain_data.get("serveradmin", ""),
            "ssl_enabled": bool(domain_data.get("ssl", 0)),
        }
