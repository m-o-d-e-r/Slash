from Slash.Core.core import Connection
from Slash.Core.operations_ import Operations

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

print(Operations(conn).select("test1", ("age", "name")).get_data())
