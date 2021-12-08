from typing import final
import psycopg2
import string
import re

from .exeptions_ import (
    SlashBadColumnNameError, SlashTypeError,
    SlashBadAction, SlashPatternMismatch
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
        request = "CREATE TABLE IF NOT EXISTS {} ({})".format(
            table.get_name(),
            ", ".join([f"{col.column_name} {col.column_sql_type}" for col in table.get_columns()])
            )

        self.connection.execute(CheckDatas.checkSQL(request, "create"))

@final
class SQLConditions:
    EQUEL = "="
    AND = "AND"
    NEQUEL = "!="
    OR = "OR"
    NOT = "NOT"
    MORE = ">"
    LESS = "<"
    EMORE = ">="
    ELESS = "<="
    @staticmethod
    def where(*condition):
        return " ".join(list(map(str, condition)))


class CheckDatas:
    SQL_TEMPLATES = {
        "insert" : "INSERT INTO [a-zA-Z0-9]* [)()a-zA-Z,\s]* VALUES [a-zA-Z)(0-9,\s']*",
        "create" : "CREATE TABLE IF NOT EXISTS [a-zA-Z0-9]* [)()a-zA-Z0-9',\s]*",
        "update" : "",
        "delete" : ""
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
