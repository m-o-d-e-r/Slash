from Slash.Core.core import Connection
from Slash.Core.migrate import MigrationCore
from Slash.types_ import (
    Table, TableMeta, Column,
    Int, Text, Bool
)
import os


conn = Connection("Slash", "postgres", "root", "127.0.0.1", 5432)
conn.set_migration_engine(MigrationCore(os.path.dirname(__file__) + "/migrations"))


class UserData(Table, metaclass=TableMeta):
    author = Column(Text, None)
    phone = Column(Text, None)

    __table__name__ = "users"

class UserData2(Table, metaclass=TableMeta):
    author2 = Column(Text, None)
    phone2 = Column(Text, None)

    __table__name__ = "users2"


usersphone = UserData()
conn.create(usersphone)

usersphone2 = UserData2()
conn.create(usersphone2)

conn.close()

