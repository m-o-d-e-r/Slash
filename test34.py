from Slash.types_ import Column, Table, Int
from Slash.Core.operations_ import Operations
from Slash.Core.core import Connection, SQLCnd

conn = Connection("Slash", "postgres", "root", "127.0.0.1", 5432)

table = Table("test123")
table.set_columns(
    Column(Int, "field1")
)
conn.create(table)

table << Operations(conn)

# Operations(conn).insert(
#     table,
#     (table.field1,),
#     (Int(2),)
# )

# table.op.delete(
#     table,
#     condition=SQLCnd.where(
#         [table.rowid, SQLCnd.EQ, Int(3)]
#     )
# )

# print(
#     table.op.select(
#         table,
#         (table.rowid,)
#     ).get_data()
# )

# table.op.update(
#     table,
#     (table.field1,),
#     (Int(2),),
#     condition=SQLCnd.where(
#         [table.rowid, SQLCnd.EQ, Int(2)], SQLCnd.AND,
#         [table.field1, SQLCnd.EQ, Int(228)]
#     )
# )
