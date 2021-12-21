from Slash.Core.operations_ import Operations
from Slash.types_ import Column, Table, TablesManager, Int, Text
from Slash.Core.core import Connection

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)


table1 = Table("test1")
table1.set_columns(Column(Int, "age"))
table1.create(conn)

table2 = Table("test2")
table2.set_columns(Column(Int, "name"))
table2.create(conn)

table3 = Table("test3")
table3.set_columns(Column(Int, "age"), Column(Text, "name"))
table3.create(conn)

Operations(conn).insert(table3, ("age", "name"), (Int(1), Text("asas"),))
# Operations(conn).insert(table1, ("age"), (Int(1),))
# Operations(conn).insert(table1, ("age"), (Int(2),))
# Operations(conn).insert(table2, ("name"), (Int(11),))
# Operations(conn).insert(table2, ("name"), (Int(22),))


utable = TablesManager.unite(table1, table2)


operations = Operations(conn)
operations.select(utable, ("age", "name"))


conn.close()
