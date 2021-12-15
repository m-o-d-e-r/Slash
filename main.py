from Slash.Core.core import Connection
from Slash.Core.operations_ import Operations
from Slash.types_ import Table

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

table = Table("test1")
table.set_columns("age", "names")

print(Operations(conn).select("test1", ("age", "name")).get_data())
