from Slash.types_ import Table, TableMeta, Column, Int, Date, Bool, Text, Hidden, Rules
from Slash.Core.operations_ import Operations
from Slash.Core.migrate import MigrationCore
from Slash.Core.core import Connection
import random
import re
import os


conn = Connection("Slash", "postgres", 'root', "127.0.0.1", 5432)
conn.set_migration_engine(MigrationCore(os.path.dirname(__file__) + "/migrations"))

class MyRules(Rules):
    ...

mr = MyRules()
mr.new_rules(
    {
        "type_int": {
            "min": 0,
            "max": 1000,
            "type": int,
            "valide_foo": mr.valid_int
        },
        "type_text": {
            "length": 3,
            "valide_foo": mr.valid_text
        },
        "type_bool": {
            "valide_foo": mr.valid_bool
        },
        "type_date": {
            "do": re.search,
            "valide_foo": mr.valid_date
        },
        "type_hidden": {
            "available": [str],
            "valide_foo": mr.valid_hidden
        }        
    }
)


class Test(Table, metaclass=TableMeta):
    count = Column(Int, None)
    is_true = Column(Bool, None)
    text = Column(Text, None)
    date = Column(Date, None)
    passw = Column(Hidden, None)
    __table__name__ = "q"



table = Test()
conn.create(table)


Operations(conn).insert(
    table,
    ("count", "is_true", "text", "date", "passw"),
    (Int(random.randint(0, 1000)), Bool(True), Text("qwe"), Date(Date.now()), Hidden("123")),
    rules=mr
)



conn.close()
