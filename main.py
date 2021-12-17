from re import template
from Slash.types_ import AutoField, Bool, Column, Table, Int, Text, Date
from Slash.Core.core import Connection
from Slash.Core.operations_ import Operations

import datetime

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

table = Table("test22")
table.set_columns(
    Column(AutoField, "id"),
    Column(Text, "Name"),
    Column(Int, "age"),
    Column(Bool, "student"),
    Column(Date, "date")
)
table.create(conn)


Operations(conn).insert(
    "test22",
    ("id", "Name", "age", "student", "date"),
    (
        Int(1),
        Text("test"),
        Int(12),
        Bool(True),
        Date(datetime.date.today())
    )
)

Operations(conn).update(
    table.name,
    ("id", ),
    (Int(200), )
)

print(Operations(conn).select(table.name, ("id", "Name", "age", "student", "date")).get_data())

