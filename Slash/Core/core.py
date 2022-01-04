from typing import Final, final
import traceback
import logging
import string
import sys
import re
import os

import psycopg2

from .exceptions_ import (
    SlashBadColumnNameError, SlashTypeError,
    SlashBadAction, SlashPatternMismatch
)
from ..types_ import QueryQueue, BasicTypes


class Connection:
    def __init__(self, dbname, user, password, host, port, *, logger=False):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        self.__connection = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cursor = self.__connection.cursor()

        self.__query_queue = QueryQueue(self)

        self.__logger = logger

    @property
    def queue(self):
        return self.__query_queue

    def execute(self, request, message=""):
        try:
            self.cursor.execute(request)
            self.__connection.commit()
        except Exception as e:
            if os.environ.get("redirect_error") != "True":
                print(e)
            self.__logger.info(
                "Unsuccessful commit: \n\t<< {} >>\n\t{}\n\n{}".format(request, message, e)
            )
        else:
            self.__logger.info("Successful commit: {}".format(message))

    def close(self):
        self.__connection.close()
        self.__logger.info("Session closed")

    def fetchall(self):
        return self.cursor.fetchall()

    def create(self, table):
        Create(table, BasicTypes.TYPES_LIST, self)


class Create():
    def __init__(self, table, types_list, conn: Connection):
        self.connection = conn
        self.table = table
        if self.__validate(types_list):
            self.__create(table)

    def __validate(self, types_list):
        CheckDatas.check_str(self.table.name)

        for column in self.table.columns:
            if column.type not in types_list:
                raise SlashTypeError(f"{type(column.type)} is not available type for data base")

            CheckDatas.check_str(column.name)

        return True

    def __create(self, table):
        request = "CREATE TABLE IF NOT EXISTS {} (rowID SERIAL PRIMARY KEY, {})".format(
            table.name,
            ", ".join([f"{col.name} {col.sql_type}" for col in table.columns])
        )
        self.connection.execute(
            CheckDatas.check_sql(request, "create"),
            "create operation"
        )


@final
class SQLConditions:
    EQ = "="
    AND = "AND"
    NE = "!="
    OR = "OR"
    NOT = "NOT"
    GT = ">"
    LT = "<"
    GE = ">="
    LE = "<="

    @staticmethod
    def where(*condition):
        return " WHERE " + " ".join(list(map(str, condition)))

    @staticmethod
    def order_by(column, *, desc=""):
        return " ORDER BY {} {}".format(
            CheckDatas.check_str(column),
            CheckDatas.check_str(desc)
        )

    @staticmethod
    def group_by(): ...


class CheckDatas:
    SQL_TEMPLATES: Final = {
        "insert": r"INSERT INTO [a-zA-Z0-9]* [)()a-zA-Z,\s]* VALUES [a-zA-Z)(0-9,\s'-]*",
        "create": r"CREATE TABLE IF NOT EXISTS [a-zA-Z0-9]* [)()a-zA-Z0-9',\s]*",
        "update": r"UPDATE [a-zA-Z0-9]* SET [a-zA-Z0-9\s<>!=',]*",
        "delete": r"DELETE FROM [a-zA-Z0-9]* [a-zA-Z0-9\s<>!=]*",
        "select": r"SELECT [a-zA-Z0-9(),\s'<>!=*.]*"
    }
    def __init__(self): ...

    @staticmethod
    def check_str(str_: str):
        for char_ in str_:
            if char_ in string.punctuation:
                raise SlashBadColumnNameError(
                    f"Error:\n\nBad name for column of data base\nName: {str_}\nSymbol: {char_}"
                )
        return str_

    @staticmethod
    def check_sql(sql_request: str, action: str):
        sql_template = CheckDatas.SQL_TEMPLATES.get(action)

        if sql_template is not None:
            template = re.findall(sql_template, sql_request)
            if sql_request in template:
                return sql_request
            else:
                raise SlashPatternMismatch(
                    "\n\nPattern mismatch:\n\t{}\n\nFinded pattern: {}\n\t".format(
                        sql_request, template
                    )
                )
        else:
            raise SlashBadAction("Action is wrong")


class Logger(logging.Logger):
    def __init__(self, name: str, file: str, *, redirect_error: bool=False, level=logging.INFO) -> None:
        super().__init__(name, level=level)

        self.__redirect_error = redirect_error
        os.environ.setdefault("redirect_error", str(redirect_error))

        handler = logging.FileHandler(self.__path(file), encoding="utf-8")
        formatter = logging.Formatter("[%(asctime)s]:[%(process)d-%(levelname)s]:[%(name)s]:[%(message)s]")

        handler.setFormatter(formatter)
        self.addHandler(handler)

        with open(os.environ.get("logs"), "a") as file_:
            file_.write("\n")

    def __path(self, file: str):
        path_ = os.path.dirname(os.path.abspath(file)) + "\\logs"

        if not os.path.exists(path_):
            os.mkdir(path_)
        path_ += "\\data.log"

        os.environ.setdefault("logs", path_)
        if self.__redirect_error:
            sys.stderr = open(os.environ.get("logs"), "a")

        return path_
