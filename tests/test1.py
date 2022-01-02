from Slash.types_ import Column, Int, Table, TablesManager, Text

t1 = Table("test1")
t1.set_columns(Column("age", Int))

t2 = Table("test2")
t2.set_columns(Column("name", Text))

u_table = TablesManager.unite(t1, t2)

assert str(type(u_table)) == "<class 'Slash.types_.TablesManager.unite.<locals>.UnitedTable'>"
assert u_table.name == t1.name + "U" + t2.name
