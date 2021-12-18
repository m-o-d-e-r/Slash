from Slash.Core.operations_ import Operations
from Slash.types_ import AutoField, Column, Table, TablesManager, Int, Text
from Slash.Core.core import Connection

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

table = Table("testAout")
table.set_columns(
    Column(AutoField, "id"),
    Column(Text, "name")
)
table.create(conn)


Operations(conn).insert(
    table.name, 
    (
        "name"
    ),
    (
        Text("name"),
    )
)
#table1 = Table("test1")
#table1.set_columns(Column(Int, "age"))
#table2 = Table("test2")
#table2.set_columns(Column(Int, "name"))
#table3 = Table("test3")
#table3.set_columns(Column(Int, "age"), Column(Text, "name"))


#print(TablesManager.find_by_column("age", "name"))
conn.close()