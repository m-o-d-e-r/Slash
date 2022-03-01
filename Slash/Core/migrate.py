import hashlib
import json
import os

from migration_templates import (
    STANDART_JSON_CONFIG,
    MIGRATION_BLOCK
)
from ..types_ import BasicTypes


class Migration:
    def __init__(self, name, columns, path):
        self.__name = name
        self.__columns = columns
        self.__path = path
        self._check_migrations()

    def _check_migrations(self):
        config: dict = self._read_config_file()

        if config["count_of_blocks"] == 0:
            new_migration: dict = MIGRATION_BLOCK
            new_migration["is_first"] = True
            new_migration["tables"].update(
                {
                    self.__name: list(
                        zip(
                            [c.name for c in self.__columns],
                            [BasicTypes.DB_TYPES_LIST[c.type] for c in self.__columns]
                        )
                    )
                }
            )
            new_migration["hash"] = hashlib.sha512(
                (
                    self.__name + "".join([c.name for c in self.__columns])
                ).encode("utf-8")
            ).hexdigest()
            config["blocks"].update(
                {
                    "migration_"+str(config["count_of_blocks"]): new_migration
                }
            )
            config["last_hash"] = new_migration["hash"]
        else:
            ...

#        config["count_of_blocks"] += 1
        self._write_config_file(config)
    
    def _read_config_file(self):
        if os.path.exists(self.__path + "\\config.json"):
            with open(self.__path + "\\config.json") as json_configs:
                return json.load(json_configs)
        else:
            raise FileExistsError(f"\n\tConfig file is not found...\n\t\t{self.__path}\config.json")

    def _write_config_file(self, data):
        with open(self.__path + "\\config.json", "w") as json_configs:
            json.dump(data, json_configs, indent=4)

    @property
    def signature(self):
        return (self.__name, self.__columns)


class MigrationCore:
    def __init__(self, path_) -> None:
        if not os.path.exists(path_):
            os.mkdir(path_)
            with open(path_+"/config.json", "w") as file_:
                json.dump(STANDART_JSON_CONFIG, file_, indent=4)
        self.__migrations_folder = path_

    @property
    def path(self):
        return self.__migrations_folder

    def make_signature(self, table):
        Migration(table.name, table.columns, self.path)
