from Slash.Core.operations_ import Operations
from Slash.Core.migrate import MigrationCore
from Slash.Core.core import Connection, SQLCnd
from Slash.types_ import (
    Table, TableMeta, Column,
    Int, Text, Bool, Hidden, Date
)
import os


conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)
#conn.set_migration_engine(MigrationCore(os.path.dirname(__file__) + "/migrations", True))


class Books(Table, metaclass=TableMeta):
    author = Column(Text, None)    
    theme = Column(Text, None)
    pages = Column(Int, None)
    created = Column(Date, None)


books = Books("books228")
conn.create(books)


#Operations(conn).insert(
#    books,
#    ('author', 'theme', 'pages', 'created'),
#    (Text("mr"), Text("f"), Int(100), Date(Date.now()))
#)
#Operations(conn).update(
#    books,
#    ('author', 'theme', 'pages', 'created'),
#    (Text("m"), Text("fff"), Int(120), Date(Date.now())),
#    condition=SQLCnd.where([books.rowid, SQLCnd.EQ, Int(1)])
#)
Operations(conn).delete(
    books,
    condition=SQLCnd.where([books.author, SQLCnd.EQ, Text("m")])
)



conn.close()
