from Slash.Core.operations_ import Operations, CheckDatas
from Slash.types_ import Table, Column, Text, Int
from Slash.Core.core import Connection, SQLCnd


table = Table("testtableforcondition")
table.set_columns(
    Column(Text, "some_1"),
    Column(Text, "some_2")
)

with Connection("Slash", "postgres", "root", "127.0.0.1", 5432) as conn:
    conn.create(table)

#    Operations(conn).insert(table, ("some_1", "some_2"), (Text("q"), Text("w")))
    Operations(conn).update(
        table,
        ("some_1", "some_2"),
        (Text("qwqw"), Text("erer")),
        SQLCnd.where(
            [table.rowid, SQLCnd.EQ, Int(3)], SQLCnd.OR,
            [table.some_2, SQLCnd.EQ, Text("w")]
        )
    )
