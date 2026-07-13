import json
import tarfile

import yaml


class BackupArchive:

    def __init__(self, tar: tarfile.TarFile):
        self.tar = tar

        #
        # Índice de todos los archivos
        #
        self.members = {
            member.name: member
            for member in tar.getmembers()
        }

    def exists(self, path: str) -> bool:
        return path in self.members

    def read_text(self, path: str):

        if path not in self.members:
            return None

        member = self.members[path]

        fp = self.tar.extractfile(member)

        if fp is None:
            return None

        return fp.read().decode("utf-8", errors="ignore")

    def read_yaml(self, path: str):

        text = self.read_text(path)

        if text is None:
            return None

        return yaml.safe_load(text)

    def read_json(self, path: str):

        text = self.read_text(path)

        if text is None:
            return None

        return json.loads(text)

    def listdir(self, prefix: str):

        prefix = prefix.rstrip("/") + "/"

        result = []

        for name in self.members:

            if name.startswith(prefix):
                result.append(name)

        return result

    def walk(self, prefix: str):

        prefix = prefix.rstrip("/") + "/"

        for member in self.members.values():

            if member.name.startswith(prefix):
                yield member
