from Slash.Core.core import Connection


conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

conn.close()
