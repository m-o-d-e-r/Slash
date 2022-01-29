from Slash.Core.core import Connection, Logger
from Slash.Core.operations_ import Operations, Insert
from Slash.types_ import (
    Table, TableMeta, Column,
    Int, Text
)

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432,
    logger=Logger(__name__, __file__, redirect_error=True)
)





class InfoClass(Table, metaclass=TableMeta):
    number = Column(Int, None)
    count = Column(Int, None)
    teacher = Column(Text, None)


table = InfoClass("class")


Insert(conn, table, ("number", "count", "teacher"), (Int(1), Int(1), Text("qwerty")))
