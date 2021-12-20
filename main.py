from Slash.types_ import Column, Table, TablesManager, Int, Text
from Slash.Core.core import Connection

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)


table1 = Table("test1")
table1.set_columns(Column(Int, "age"))
table2 = Table("test2")
table2.set_columns(Column(Int, "name"))
table3 = Table("test3")
table3.set_columns(Column(Int, "age"), Column(Text, "name"))


print(TablesManager.find_by_name("test3"))
print(TablesManager.find_one_by_column("age", "name"))
print(TablesManager.find_many_by_column("age"))


unatedTable = TablesManager.unite(table1, table2)
print(unatedTable.name)
print(unatedTable.columns)

conn.close()