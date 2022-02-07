from Slash.Core.core import SQLCnd, Connection
from Slash.Core.operations_ import Operations
from Slash.types_ import Text, Int, Table, Column, TableMeta

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)


class Users(Table, metaclass=TableMeta):
    name = Column(Text, None)
    report = Column(Text, None)
    status = Column(Int, None)


table = Users("users_table")
conn.create(table)


Operations(conn).insert(
    table,
    ("name", "report", "status"),
    (Text("Bohdan"), Text("Hi its my report"), Int(100))
)
Operations(conn).update(
    table,
    ("name", "report", "status"),
    (Text("Bogdan"), Text("Hi"), Int(200)),
    condition=SQLCnd.where(["rowid", SQLCnd.EQ, Int(1)])
)



conn.close()
