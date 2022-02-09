from Slash.Core.core import Connection, SQLCnd
from Slash.Core.operations_ import Operations
from Slash.types_ import Table, Column, Int, Text, Date, Hidden, Bool, TableMeta, TablesManager

import datetime


conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)


class Users(Table, metaclass=TableMeta):
    author = Column(Text, None)
    status = Column(Int, None)
    password = Column(Hidden, None)
    admin = Column(Bool, None)

    __table__name__ = "users"

class UsersPhone(Table, metaclass=TableMeta):
    author = Column(Text, None)
    phone = Column(Text, None)
    reg_data = Column(Date, None)

    __table__name__ = "users_phone"


users = Users()
usersphone = UsersPhone()

conn.create(users)
conn.create(usersphone)


united_table = TablesManager.unite(users, usersphone)


print(Operations(conn).select(
    united_table,
    ("status", "password", "admin", "author", "phone", "reg_data")
).get_data()
)

#Operations(conn).update(
#    united_table,
#    ("status", "password", "admin", "author", "phone", "reg_data"),
#    (
#        Int(101), Hidden("my_password"), Bool(True), Text("Bohdan"), Text("38045456465465"), Date(datetime.date.today())
#    ),
#    SQLCnd.where(
#        ["author", SQLCnd.EQ, Text("M_O_D_E_R")]
#    )
#)

#Operations(conn).insert(
#    united_table,
#    ("status", "password", "admin", "author", "phone", "reg_data"),
#    (
#        Int(100), Hidden("my_password"), Bool(True), Text("M_O_D_E_R"), Text("38045456465465"), Date(datetime.date.today())
#    )
#)

#Operations(conn).delete(
#    united_table,
#    SQLCnd.where(
#        ["author", SQLCnd.EQ, Text("M_O_D_E_R")]
#    )
#)


conn.close()
