from Slash.types_ import Table, TableMeta, Column, Int, Date, Bool
from Slash.Core.operations_ import Operations
from Slash.Core.migrate import MigrationCore
from Slash.Core.core import Connection

conn = Connection("Slash", "postgres", 'root', "127.0.0.1", 5432)
conn.set_migration_engine(MigrationCore("D:\\pyrus\\ORM\\migrations"))


class TableForMigration(Table, metaclass=TableMeta):
    count = Column(Int, None)
    is_true = Column(Bool, None)
    date = Column(Date, None)

    __table__name__ = "tableformigrations"



table = TableForMigration()
conn.create(table)




conn.close()
