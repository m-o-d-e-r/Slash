from ctypes import Union
from typing import Any, List, Tuple
from .core import CheckDatas, Connection, SQLCnd, CheckColumns
from ..types_ import Column, DataSet, Table, BasicTypes

from .exceptions_ import SlashRulesError, SlashLenMismatch, SlashTypeError


class Insert():
    def __init__(self, conn: Connection, table: Table, names: Any, values: Any, rules="*"):
        names = [names] if (type(names) != list) and (type(names) != tuple) else names
        values = [values] if (type(values) != list) and (type(values) != tuple) else values

        if len(names) != len(values):
            raise SlashLenMismatch(
                """The lenght of the data and the lenght of the columns do not match.
                    Column lenght: {}
                    Values lenght: {}
                """.format(
                    len(names),
                    len(values)
                )
            )

        self.__responce = self.__validate(table, names, values, rules)
        self.__table = table
        conn.execute(
            CheckDatas.check_sql(self.__responce[0], "insert"),
            "insert operation",
            self.__responce[1]
        )

    def __validate(self, table, names, values, rules):
        CheckDatas.check_str(table.name)

        for name in names:
            CheckDatas.check_str(name)

        for value in values:
            if value.type_name == "type_text":
                CheckDatas.check_str(value.value)

            valid_responce = value._is_valid_datas(rules)
            if not valid_responce[0]:
                raise SlashRulesError(f"\n\n\nRule: {valid_responce[1]}")

        names = ", ".join(names)
        sql_responce = f'INSERT INTO {table.name} ({names}) VALUES ({", ".join(["%s" for i in range(len(values))])})'

        return [sql_responce, tuple([i.value for i in values])]

    @property
    def responce(self):
        return self.__responce

    @property
    def table(self):
        return self.__table


class Delete():
    def __init__(self, conn: Connection, table: Table, condition: SQLCnd):
        self.__responce = self.__validate(table, condition)
        conn.execute(
            CheckDatas.check_sql(self.__responce, "delete"),
            "delete operation"
        )

    def __validate(self, table, condition):
        CheckDatas.check_str(table.name)
        sql_responce = f"DELETE FROM {table.name}{condition}"

        return sql_responce

    @property
    def responce(self):
        return self.__responce


class Select():
    def __init__(self, conn: Connection, table: Table, names: tuple, condition: SQLCnd):
        self.__conn = conn
        self.__responce = self.__validate(table, names, condition)
        self.__table__name = table.name
        self.__names = names

    def __validate(self, table, names, condition):
        names = [names] if (type(names) != list) and (type(names) != tuple) else names

        CheckDatas.check_str(table.name)
        for name in names:
            CheckDatas.check_str(name)

        return "SELECT {} FROM {}{}".format(
            ", ".join([n for n in names]),
            table.name, condition
        )

    def get(self):
        self.__conn.execute(
            CheckDatas.check_sql(self.__responce, "select"),
            "select operation"
        )

        return DataSet(
            self.__table__name, self.__names, self.__conn.fetchall()
        )

    @property
    def responce(self):
        return self.__responce


class Update():
    def __init__(
        self,
        conn: Connection,
        table: Table,
        names: tuple,
        values: tuple,
        condition,
        rules="*"
    ):
        self.__responce = self.__validate(
            table, names, values, condition, rules
        )
        conn.execute(
            CheckDatas.check_sql(self.__responce, "update"),
            "update operation"
        )

    def __validate(self, table, names, values, condition, rules):
        names = [names] if (type(names) != list) and (type(names) != tuple) else names
        values = [values] if (type(values) != list) and (type(values) != tuple) else values

        CheckDatas.check_str(table.name)
        sql_responce = "UPDATE {} SET ".format(table.name)

        for index, value in enumerate(values):
            valid_responce = value._is_valid_datas(rules)
            if not valid_responce[0]:
                raise SlashRulesError(f"\n\n\nRule: {valid_responce[1]}")

            if value.type_name in BasicTypes.NEED_FORMAT:
                sql_responce += " = ".join((names[index], f"'{value.value}'"))
            else:
                sql_responce += " = ".join((names[index], f"{value.value}"))

            sql_responce += ", " if index != (len(values) - 1) else ""

        sql_responce += condition

        return sql_responce

    @property
    def responce(self):
        return self.__responce


class InnerJoin():
    def __init__(
        self,
        conn: Connection,
        tables,
        names: Any,
        condition: str
    ):
        self.__conn = conn
        self.__tables = tables
        self.__names = names
        self.__responce = self.__validate(condition)

    def __validate(self, condition):
        SQL_RESPONCE = "SELECT {} FROM {} INNER JOIN {} ON {}"
        for name in self.__names:
            if type(name) is not Column:
                raise SlashTypeError(
                    f"""
                    Type of this object should be Column, not {type(name)}
                    Operation: INNER JOIN
                    Object value: --{name}--
                    """
                )
            CheckDatas.check_str(name.name)

        for table in self.__tables:
            if type(table) is not Table:
                raise SlashTypeError(
                    f"""
                    Type of this object should be Table, not {type(name)}
                    Operation: INNER JOIN
                    Object value: --{name}--
                    """
                )
            CheckDatas.check_str(table.name)

        return SQL_RESPONCE.format(
            ", ".join([".".join((item._p, item.name)) for item in self.__names]),
            *[table.name for table in self.__tables],
            condition
        )
    
    def get(self):
        self.__conn.execute(
            CheckDatas.check_sql(self.__responce, "select"),
            "select operation"
        )
        return DataSet(
            self.__tables, self.__names, self.__conn.fetchall()
        )


class LeftOuter():
    ...


class RightOuter():
    ...


class Operations:
    def __init__(self, connection, table_link=None):
        self.__connection = connection
        self.__table = table_link

    def insert(self, table, names, values, *, rules="*"):
        if self.__table:
            table = self.__table

        if table.__dict__.get("_is_unated") is not None:
            table._is_unated

            data: dict = dict(zip(names, values))

            for one_table in table.tables:
                columns_list = []
                for column in one_table.columns:
                    columns_list.append(column.name)

                Insert(
                    self.__connection,
                    one_table,
                    columns_list,
                    [data[i] for i in columns_list],
                    rules
                )
        else:
            if rules == "*":
                Insert(self.__connection, table, names, values)
            else:
                Insert(
                    self.__connection, table, names, values, rules
                )

    def select(self, table, names, condition=" "):
        if self.__table:
            table = self.__table

        if table.__dict__.get("_is_unated") is not None:
            table._is_unated

            data_matrix = []
            output = []
            result = []

            for one_table in table.tables:
                columns_list = []
                for column in one_table.columns:
                    columns_list.append(column.name)

                select_query = Select(self.__connection, one_table, columns_list, condition).get()
                temp = []
                for data in select_query.get_data():
                    temp.append(data)
                data_matrix.append(temp)

            for t in range(len(data_matrix)):
                temp_data = []
                for i, item in enumerate(data_matrix):
                    for n, nitem in enumerate(item):
                        temp_data.append(data_matrix[n][t])
                    break
                output.append(temp_data)

            for i, output_item in enumerate(output):
                temp_user_data = []
                for item_frame in output_item:
                    for item in item_frame:
                        temp_user_data.append(item)
                len_ = len(temp_user_data)

                for n in range(len_-1):
                    if temp_user_data.count(temp_user_data[n]) > 1:
                        del temp_user_data[n]
                result.append(tuple(temp_user_data))

            return DataSet(table.name, table.columns, result)
        else:
            return Select(self.__connection, table, names, condition).get()

    def delete(self, table, condition=" "):
        if self.__table:
            table = self.__table

        if table.__dict__.get("_is_unated") is not None:
            table._is_unated

            CheckColumns.check(condition, table.tables)
            for table_item in table.tables:
                Delete(self.__connection, table_item, condition)
        else:
            return Delete(self.__connection, table, condition)

    def update(self, table, column_names, values, condition=" "):
        if self.__table:
            table = self.__table

        if table.__dict__.get("_is_unated") is not None:
            table._is_unated

            data: dict = dict(zip(column_names, values))

            for one_table in table.tables:
                columns_list = []
                for column in one_table.columns:
                    columns_list.append(column.name)

                Update(
                    self.__connection,
                    one_table,
                    columns_list,
                    [data[i] for i in columns_list],
                    condition
                )
        else:
            Update(self.__connection, table, column_names, values, condition)

    def inner_join(self, tables, names, condition):
        return InnerJoin(self.__connection, tables, names, condition).get()

    def __enter__(self):
        return self
    
    def __exit__(self, *args): ...
