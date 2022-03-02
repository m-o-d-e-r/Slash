from Slash.types_ import Table, TableMeta, Column, Int, Date, Bool
from Slash.Core.operations_ import Operations
from Slash.Core.migrate import MigrationCore
from Slash.Core.core import Connection
import os

conn = Connection("Slash", "postgres", 'root', "127.0.0.1", 5432)
conn.set_migration_engine(MigrationCore(os.path.dirname(__file__) + "/migrations"))


class TableForMigration(Table, metaclass=TableMeta):
    count = Column(Int, None)
    is_true = Column(Bool, None)
    date = Column(Date, None)
    new_column = Column(Bool, None)

    __table__name__ = "tableformigrations"


#class Test2(Table, metaclass=TableMeta):
#   age = Column(Int, None)
#    man = Column(Bool, None)
#    dirsday = Column(Date, None)

#    __table__name__ = "test2"


table = TableForMigration()
conn.create(table)

#table2 = Test2()
#conn.create(table2)



conn.close()
