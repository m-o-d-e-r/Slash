from Slash.types_ import Column, Table, Int, Text, Bool, Rules, TablesManager
from Slash.Core.core import Connection, SQLConditions
from Slash.Core.operations_ import Operations



conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

table = Table("test1")
table.set_columns(Column(Int, "age"), Column(Text, "name"))
table.create(conn)

print(TablesManager.tables)
print(TablesManager.find_by_name("test1"))
