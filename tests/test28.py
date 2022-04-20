from Slash.types_ import (
    Int, Text, Bool, Date, Hidden, Email, Phone, IPv4, IPv6, Url,
    Table, Column
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


print(
    Operations(conn).inner_join(
        (a, b),
        (a.age, b.username),
        SQLCnd.where([a.rowid, SQLCnd.EQ, b.rowid])
    ).get_data()
)




conn.close()
