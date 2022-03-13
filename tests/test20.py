from Slash.types_ import Int, TableMeta, Text, Table, Column
from Slash.Core.migrate import MigrationCore, VersionManager
from Slash.Core.core import Connection
import os


conn = Connection("Slash", "postgres", "root", "127.0.0.1", 5432)
conn.set_migration_engine(MigrationCore(os.path.dirname(__file__) + "/migrations"))


class Test(Table, metaclass=TableMeta):
    c1 = Column(Int, None)

    __table__name__ = "t1"

class Test2(Table, metaclass=TableMeta):
    c11 = Column(Int, None)
    c22 = Column(Int, None)

    __table__name__ = "t2"

class Test3(Table, metaclass=TableMeta):
    c111 = Column(Int, None)
    c222 = Column(Int, None)
    c333 = Column(Int, None)

    __table__name__ = "t3"



table = Test()
table2 = Test2()
table3 = Test3()


print(table.name)
print(table2.name)
print(table3.name)


print(table.columns)
print(table2.columns)
print(table3.columns)


conn.create(table)
conn.create(table2)
conn.create(table3)



conn.close()

