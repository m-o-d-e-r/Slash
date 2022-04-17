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


table = Table("test")
table.set_columns(
    Column(Int, "age"),
    Column(Text, "username"),
    Column(Bool, "man"),
    Column(Date, "reg_date"),
    Column(Hidden, "password"),
    Column(Email, "email"),
    Column(Phone, "phone"),
    Column(IPv4, "ipv4"),
    Column(IPv6, "ipv6"),
    Column(Url, "url")
)
conn.create(table)

# INSERT
#Operations(conn).insert(
#    table,
#    tuple([i.name for i in table.columns]),
#    (
#        Int(18),
#        Text("M_O_D_E_R"),
#        Bool(True),
#        Date(Date.now()),
#        Hidden(123),
#        Email("sadasd@gmail.com"),
#        Phone("+380000000000"),
#        IPv4("127.0.0.0"),
#        IPv6("2001:0db8:11a3:09d7:1f34:8a2e:07a0:765d"),
#        Url("https://www.google.com/")
#    )
#)

# UPDATE
#Operations(conn).update(
#    table,
#    tuple([i.name for i in table.columns]),
#    (
#        Int(11),
#        Text("m"),
#        Bool(True),
#        Date(Date.now()),
#        Hidden(2),
#        Email("wewe@gmail.com"),
#        Phone("+380000000000"),
#        IPv4("127.0.0.0"),
#        IPv6("2001:0db8:11a3:09d7:1f34:8a2e:07a0:765d"),
#        Url("https://www.google.com/")
#    ), condition=SQLCnd.where(
#        [table.age, SQLCnd.EQ, Int(22)], SQLCnd.AND,
#        [table.rowid, SQLCnd.EQ, Int(1)]
#    )
#)

# SELECT
#print(
#    Operations(conn).select(
#        table,
#        tuple(["rowid"] + [i.name for i in table.columns]),
#        condition=SQLCnd.where(
#            [table.rowid, SQLCnd.GT, Int(5)]
#        )
#    ).get_data()
#)

# DELETE
#Operations(conn).delete(
#    table,
#    condition=SQLCnd.where(
#        [table.rowid, SQLCnd.GE, Int(2)], SQLCnd.AND,
#        [table.rowid, SQLCnd.LE, Int(5)], SQLCnd.AND,
#        [table.username, SQLCnd.EQ, Text("M_O_D_E_R")]
#    )
#)



conn.close()




