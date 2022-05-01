from Slash.types_ import Column, Table, TableMeta, Int
from Slash.Core.operations_ import Operations
from Slash.Core.core import Connection

conn = Connection(
    "Slash",
    "postgres",
    "root",
    "127.0.0.1",
    5432
)


class Test(Table, metaclass=TableMeta):
    field1 = Column(Int, None)


table = Test("test123")
table << Operations(conn)

conn.create(table)

table.op.insert(
    table,
    [table.field1],
    [Int(123)]
)

#table + Column(Int, "field2")
#table - Column(Int, "field2")
