from Slash.Core.migrate import MigrationCore
from Slash.Core.core import Connection
from Slash.types_ import (
    Table, TableMeta, Column,
    Text, Date
)
import os

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)
conn.set_migration_engine(MigrationCore(os.path.dirname(__file__) + "/migrations", False))


readers = Table("readers")
readers.set_columns(
    Column(Text, "username"),
    Column(Date, "date")
)
conn.create(readers)


books = Table("books")
books.set_columns(
    Column(Text, "author"),
    Column(Text, "theme")
)
conn.create(books)

conn.migrate(books, readers)


conn.close()
