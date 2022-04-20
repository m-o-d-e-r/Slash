from Slash.Core.operations_ import Operations
from Slash.Core.migrate import MigrationCore
from Slash.Core.core import Connection, Logger
from Slash.types_ import (
    Table, TableMeta, Column,
    Int, Text, Bool, Hidden, Date
)
import os

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)
conn.set_migration_engine(MigrationCore(os.path.dirname(__file__) + "/migrations", True))

class Books(Table, metaclass=TableMeta):
    rating = Column(Int, None)
    author = Column(Text, None)    

user_data = Books("user_data")
conn.create(user_data)


#Operations(conn).insert(
#    users,
#    ('rang', 'author_name', 'author_surname', 'single', 'phone', 'login', 'password', 'reg_data'),
#    (Int(100), Text("M_O_D_E_R"), Text("M_O_D_E_R"), Bool(True), Text("095169"), Text("mr"), Hidden("123"), Date(Date.now()))
#)


conn.close()
