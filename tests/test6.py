from Slash.Core.core import SQLCnd, Connection
from Slash.Core.operations_ import Operations
from Slash.types_ import Text, Int, Table, Column

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)


#print(SQLCnd.where(["row_id", SQLCnd.EQ, Int(1)], SQLCnd.AND, ["text", SQLCnd.EQ, Text("123")]))


table = Table("testfutures")
table.set_columns(
    Column(Int, "test_int"),
    Column(Text, "test_text")
)
conn.create(table)

Operations(conn).delete(
    table,
    condition=SQLCnd.where(["rowid", SQLCnd.EQ, Int(9)], SQLCnd.AND, ["test_text", SQLCnd.EQ, Text("1")])
)


conn.close()
