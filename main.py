from Slash.Core.core import Connection
from Slash.Core.operations_ import Operations
from Slash.types_ import Column, Int, Table, Text



conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

table = Table("test3")
table.set_columns(
    Column(Int, "age"),
    Column(Text, "name")
)
conn.create(table)

op = Operations(conn)
op.select(table, ("age", "name", )).get_data()
op.select(table, ("age", "name", )).get_data()
op.select(table, ("age", "name", )).get_data()

print(op.query_handler.rollback())

conn.close()
