from Slash.Core.core import Connection, Logger
from Slash.Core.operations_ import Operations
from Slash.types_ import Column, Int, Table, Text


log = Logger(__name__, __file__)
log.info("New session")


conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432,
    logger=log
)

table = Table("test3")
table.set_columns(
    Column(Int, "age"),
    Column(Text, "name")
)
conn.create(table)

op = Operations(conn)
op.select(table, ("age", "name", )).get_data()

op.insert(
    table,
    ("age", "name" , ),
    (Int(229), Text("hello"), )
)


conn.close()
