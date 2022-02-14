from Slash.Core.operations_ import Operations
from Slash.types_ import Table, Column, Text, Int
from Slash.Core.core import Connection, SQLCnd


table = Table("testtableforcondition")
table.set_columns(Column(Text, "some_c"))

with Connection("Slash", "postgres", "root", "127.0.0.1", 5432) as conn:
    conn.create(table)

    print(SQLCnd.where([table.some_c, SQLCnd.EQ, Text("1")]))
