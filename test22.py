from Slash.Core.operations_ import Operations
from Slash.Core.migrate import MigrationCore
from Slash.Core.core import Connection, Logger
from Slash.types_ import (
    Table, TableMeta, Column,
    Int, Text, Bool, Hidden, Date
)
import os

#logger=Logger(__name__, __file__, redirect_error=True)
conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)
conn.set_migration_engine(MigrationCore(os.path.dirname(__file__) + "/migrations", True))


class Books(Table, metaclass=TableMeta):
    author = Column(Text, None)    
    theme = Column(Text, None)
    pages = Column(Int, None)
    created = Column(Date, None)


class UserData(Table, metaclass=TableMeta):
    rang = Column(Int, None)
    author_name = Column(Text, None)
    author_surname = Column(Text, None)
    single = Column(Bool, None)
    phone = Column(Text, None)
    login = Column(Text, None)
    password = Column(Hidden, None)
    reg_data = Column(Date, None)
#    test_field = Column(Text, None)

    __table__name__ = "users"


users = UserData()
conn.create(users)


#books = Books("books")
#conn.create(books)


#Operations(conn).insert(
#    users,
#    ('rang', 'author_name', 'author_surname', 'single', 'phone', 'login', 'password', 'reg_data'),
#    (Int(100), Text("M_O_D_E_R"), Text("M_O_D_E_R"), Bool(True), Text("095169"), Text("mr"), Hidden("123"), Date(Date.now()))
#)


conn.close()
