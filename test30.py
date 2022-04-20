from Slash.types_ import (
    Int, Text,
    Table, Column,
    TablesManager
)
from Slash.Core.core import Connection
from Slash.Core.operations_ import Operations, SQLCnd


conn = Connection(
    "Slash",
    "postgres",
    "root",
    "127.0.0.1",
    5432
)


a = Table("a")
a.set_columns(Column(Int, "age"))

b = Table("b")
b.set_columns(Column(Text, "username"))

conn.create(a)
conn.create(b)

# INNER JOIN
print(
    Operations(conn).inner_join(
        (a, b),
        (a.rowid, a.age, b.username),
        SQLCnd.where([a.rowid, SQLCnd.EQ, b.rowid])
    ).get_data()
)



#table = TablesManager.unite(a, b)
#Operations(conn).insert(
#    table,
#    ("age", "username"),
#    (Int(7), Text("M_O_D_E_R"))
#)
#Operations(conn).insert(
#    b,
#    ("username"),
#    (Text("e"))
#)
#Operations(conn).delete(
#    b,
#    SQLCnd.where(
#        [a.rowid, SQLCnd.EQ, Int(6)]
#    )
#)



conn.close()
