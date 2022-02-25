from Slash.Core.operations_ import Operations
from Slash.Core.core import Connection, SQLCnd
from Slash.types_ import RolesManager, Role, Table, Column, Text, Int, TableMeta, Bool, RoleRights



conn = Connection(
    dbname="Slash",
    user="postgres",
    password="root",
    host="127.0.0.1",
    port=5432
)

class Books(Table, metaclass=TableMeta):
    book = Column(Text, None)
    pages = Column(Int, None)
    it = Column(Bool, None)

    __table__name__ = "books"

books = Books()
conn.create(books)


#r = RoleRights(1, 2, 3)
#print(r)
#Operations(conn).insert(books, ("book", "pages", "it"), (Text("Java Script"), Int(25), Bool(True)))
#Operations(conn).update(books, ("book"), Text("Cpp"), SQLCnd.where([books.book, SQLCnd.EQ, Text("C")]))
#print(
#    Operations(conn).select(
#        books,
#        ("book", "pages", "it"),
#        SQLCnd.where([books.rowid, SQLCnd.GE, Int(1)])
#    ).get_data()
#)
#Operations(conn).delete(books, SQLCnd.where([books.book, SQLCnd.EQ, Text("Java Script")]))




#r_manager = RolesManager(conn)
#r_manager.create_role(Role("admin2", "admin2", "CREATEDB"))

#print(r_manager.get_roles())

conn.close()
