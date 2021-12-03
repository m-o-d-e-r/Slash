from Slash.types_ import Column, Table, Int, Text, Bool, Rules
from Slash.Core.core import Connection, Operations


class MyRules(Rules):
    def __init__(self): ...


myRules = MyRules()
myRules.new_rules(
    {
        "type_int"  : {
            "min" : 0,
            "max" : 2000,
            "valide_foo" : myRules.valid_int
        },
        "type_text" : {
            "length" : 100,
            "valide_foo" : myRules.valid_text
        },
        "type_bool" : {
            "symbols" : [True, False],
            "valide_foo" : myRules.valid_bool
        },
        "type_date" : {
            "current" : "{}.{}.{}",
            "valide_foo" : myRules.valid_date
        }
    }
)

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

table = Table("test1")
table.set_columns(Column(Int, "age"), Column(Text, "name"))
table.create(conn)


operations = Operations(conn)

operations.insert(conn, "test1", ("age", "name"), (Int(1000), Text("Name2")), rules=myRules)

