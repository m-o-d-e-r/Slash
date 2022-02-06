from webbrowser import Opera
import tabledata
from Slash.Core.core import Connection, Logger
from Slash.Core.operations_ import Operations
from Slash.types_ import Column, Int, Table, Text



log = Logger(__name__, __file__)
log.info("New session")


conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432,
    logger=log
)


table = Table("testfutures")
table.set_columns(
    Column(Int, "test_int"),
    Column(Text, "test_text")
)
conn.create(table)

Operations(conn).insert(
    table,
    ("test_int", "test_text"),
    (Int(1), Text("1"))
)


conn.close()
