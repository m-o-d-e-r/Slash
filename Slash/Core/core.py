import psycopg2
import string
import re

from .exeptions_ import (
    SlashBadColumnNameError, SlashRulesError,
    SlashTypeError, SlashBadAction,
    SlashPatternMismatch
)


class Connection:
    def __init__(self, dbname =  " ", user = " ", password = " ", host = " ", port = 0):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        self.__connection = psycopg2.connect(
            dbname = self.dbname,
            user = self.user, 
            password = self.password,
            host = self.host,
            port = self.port    
        )
        self.cursor = self.__connection.cursor()
    
    def execute(self, request):
        self.cursor.execute(request)
        self.__connection.commit()

    def close(self):
        self.__connection.close()

    def create_table(self, table):
        request = "CREATE TABLE IF NOT EXISTS {} ({})".format(
            table.get_name(),
            ", ".join([f"{col.column_name} {col.column_sql_type}" for col in table.get_columns()])
            )
 #       self.cursor.execute(
#        )
  #      self.__connection.commit()
        #print(CheckDatas.checkSQL(request, "create"))



class Create():
    def __init__(self, table, types_list, conn):
        self.connection: Connection = conn
        self.table = table
        if (self.__validate(types_list)):
            self.__create(table)

    def __validate (self, types_list):
        CheckDatas.checkStr(self.table.get_name())

        for column in self.table.get_columns():
            if column.column_type not in types_list:
                raise SlashTypeError(f"{type(column.column_type)} is not available type for data base")

        for column in self.table.get_columns():
            CheckDatas.checkStr(column.column_name)

        return True

    def __create(self, table):
        self.connection.create_table(table)


class Insert():
    def __init__(self, conn: Connection, table_name, names, values, rules="*"):
        responce = self.__validate(table_name, names, values, rules)
        conn.execute(CheckDatas.checkSQL(responce, "insert"))

    def __validate(self, table_name, names, values, rules):
        CheckDatas.checkStr(table_name)

        for name in names:
            CheckDatas.checkStr(name)

        for value in values:
            if value.type_name == "type_text":
                CheckDatas.checkStr(value.value)

            valid_responce = value._is_valid_datas(rules)
            if not valid_responce[0]:
                raise SlashRulesError(f"\n\n\nRule: {valid_responce[1]}")

        r = f"""INSERT INTO {table_name} {str(names).replace("'", "")} VALUES ("""

        for index, v in enumerate(values):
            if v.type_name == "type_int":
                r += str(v.value)
                if (index + 1) != len(values):
                    r += ", "
            elif v.type_name == "type_text":
                r += ("'" + v.value + "'")
                if (index + 1) != len(values):
                    r += ","
        r += ")"

        return r


class Update(): ...

class Delete(): ...

class Operations():
    def __init__(self, connection):
        self.__connection = connection

    def insert(self, connection, table_name, names, values, *, rules="*"):
        if rules == "*":
            Insert(connection, table_name, names, values)
        else:
            Insert(connection, table_name, names, values, rules)

    def update(self):
        Update()

    def delete(self):
        Delete()


class CheckDatas:
    SQL_TEMPLATES = {
        "insert" : "INSERT INTO [a-zA-Z0-9]* [)()a-zA-Z,\s]* VALUES [a-zA-Z)(0-9,\s']*",
        "create" : "CREATE TABLE IF NOT EXISTS [a-zA-Z0-9]* [)()a-zA-Z0-9',\s]*",
    }
    def __init__(self): ...

    @staticmethod
    def checkStr(str_):
        for char_ in str_:
            if char_ in string.punctuation:
                raise SlashBadColumnNameError(
                    f"Error:\n\nBad name for column of data base\nName: {str_}\nSymbol: {char_}"
                )
        return True
 
    @staticmethod
    def checkSQL(sql_request, action):
        sql_template = CheckDatas.SQL_TEMPLATES.get(action)

        if sql_template is not None:
            template = re.findall(sql_template, sql_request)

            if sql_request in template:
                return sql_request
            else:
                raise SlashPatternMismatch("\n\nPattern mismatch:\n\t{}".format(sql_request))
        else:
            raise SlashBadAction("Action is wrong")
