from Slash.Core.operations_ import Operations
from Slash.Core.migrate import MigrationCore
from Slash.Core.core import Connection, Logger
from Slash.types_ import (
    Table, TableMeta, Column,
    Int, Text, Bool, Hidden, Date
)
import os

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)
conn.set_migration_engine(MigrationCore(os.path.dirname(__file__) + "/migrations", True))


class Readers(Table, metaclass=TableMeta):
    name__ = Column(Text, None)
    surname = Column(Text, None)

    __table__name__ = "readers"


class Books(Table, metaclass=TableMeta):
    #author = Column(Text, None)
    theme = Column(Text, None)
    created = Column(Date, None)


books = Books("books")
readers = Readers()

conn.create(books)
conn.create(readers)


conn.close()
