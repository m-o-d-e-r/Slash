from Slash.types_ import Column, Table, Int, Text
from Slash.Core.core import Connection, SQLConditions
from Slash.Core.operations_ import Operations



conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

table = Table("test1")
table.set_columns(Column(Int, "age"), Column(Text, "name"))
table.create(conn)

print(
    Operations(conn).select(
        table.get_name(),
        ("age", "name"),
        SQLConditions.where(
            "age", SQLConditions.EQ, 3,
            SQLConditions.order_by("age", desc="desc")   
        )
    )
)


