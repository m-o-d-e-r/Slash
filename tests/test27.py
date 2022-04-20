from Slash.types_ import (
    Int, Text, Bool,
    Table, Column,
    TableMeta
)
from Slash.Core.core import Connection
from Slash.Core.operations_ import Operations, SQLCnd


conn = Connection(
    "Slash",
    "postgres",
    "root",
    "127.0.0.1",
    5432
)


class Author(Table, metaclass=TableMeta):
    authorname = Column(Text, None)
    book_count = Column(Int, None)

    __table__name__ = "authors"


class Book(Table, metaclass=TableMeta):
    author = Column(Text, None)


table_a = Author()
table_b = Book("books")

conn.create(table_a)
conn.create(table_b)


conn.close()
