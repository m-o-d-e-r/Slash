from Slash.types_ import Int, TableMeta, Text, Table, Column
from Slash.Core.migrate import MigrationCore, VersionManager
from Slash.Core.core import Connection
import os


conn = Connection("Slash", "postgres", "root", "127.0.0.1", 5432)
conn.set_migration_engine(MigrationCore(os.path.dirname(__file__) + "/migrations"))



table = Table("table")
table.set_columns(
    Column(Int, "c1")
)
table2 = Table("table2")
table2.set_columns(
    Column(Int, "c11"),
    Column(Int, "c22")
)
table3 = Table("table3")
table3.set_columns(
    Column(Int, "c111"),
    Column(Int, "c222"),
    Column(Int, "c333")
)


conn.create(table)
conn.create(table2)
conn.create(table3)



conn.close()
