from Slash.types_ import Column, Table, Int, Text, Bool, Rules, TablesManager
from Slash.Core.core import Connection, SQLConditions
from Slash.Core.operations_ import Operations



conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

table = Table("test1")
table.set_columns(Column(Int, "age"), Column(Text, "name"))
table.create(conn)

class myRules(Rules): ...

user_rules = myRules()
user_rules.new_rules(
    {
            "type_int"  : {
                "min" : 0,
                "max" : 20_000,
                "valide_foo" : user_rules.valid_int
            },
            "type_text" : {
                "length" : 100,
                "valide_foo" : user_rules.valid_text
            },
            "type_bool" : {
                "symbols" : [True, False],
                "valide_foo" : user_rules.valid_bool
            },
            "type_date" : {
                "current" : "{}.{}.{}",
                "valide_foo" : user_rules.valid_date
            }
        }
    )

#for i in range(1, 10_000):
#    Operations(conn).insert("test1", ("age", "name"), (Int(i), Text("Name2")), rules=user_rules)


Operations(conn).delete(
    table.get_name(), SQLConditions.where(
        "age", SQLConditions.ELESS, "100"
    )
)
