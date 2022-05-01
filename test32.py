from Slash.Core.core import Connection, SQLCnd, Table, Column
from Slash.Core.operations_ import Operations
from Slash.types_ import Int, Text

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

table1 = Table("test")
table1.set_columns(
    Column(Int, "age")
)
conn.create(table1)

table1 << Operations(conn)

table1.op.insert(
    table1,
    [table1.age],
    [Int(228)]
)

#print(
#    table1.op.select(
#        table1,
#        [table1.age]
#    ).get_data()
#)

#table1.op.update(
#    table1,
#    [table1.age],
#    [Int(228)],
#    condition=SQLCnd.where(
#        [table1.age, SQLCnd.EQ, Int(228)]
#    )
#)

#table1.op.delete(
#    table1
#)


conn.close()
