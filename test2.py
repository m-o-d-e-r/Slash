from Slash.types_ import AutoField, Column, Table, Int, Text
from Slash.Core.core import Connection, SQLConditions
from Slash.Core.operations_ import Operations

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

table = Table("test1")
table.set_columns(Column(Int, "age"), Column(Text, "name"))
conn.create(table)

Operations(conn).update(
    table,
    ("name", ),
    (Text("33"), ),
    SQLConditions.where(
        "age", SQLConditions.LE, "3"
    )
)