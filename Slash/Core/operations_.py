from typing import Any
from .core import CheckDatas, Connection, SQLCnd, CheckColumns
from ..types_ import DataSet, QueryQueue, Table

from .exceptions_ import SlashRulesError, SlashLenMismatch


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
            CheckDatas.check_sql(self.__responce, "insert"),
            "insert operation"
        )
        self.__metadata: dict = {
            "columns" : names,
            "values" : [val.value for val in values]
        }

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

        sql_responce = f"""INSERT INTO {table.name} ({names}) VALUES ("""

        need_format = ("type_text", "type_date", "type_hidden")

        for index, val in enumerate(values):
            if val.type_name in need_format:
                sql_responce += f"'{val.value}'"
            else:
                sql_responce += str(val.value)
 
            if (index + 1) != len(values):
                sql_responce += ", "


        sql_responce += ")"

        return sql_responce

    @property
    def metadata(self):
        return self.__metadata

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
    def __init__(self, conn: Connection, table: Table, names: tuple, values: tuple, condition, rules="*"):
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

        need_format = ("type_text", "type_date", "type_hidden")

        for index, value in enumerate(values):
            valid_responce = value._is_valid_datas(rules)
            if not valid_responce[0]:
                raise SlashRulesError(f"\n\n\nRule: {valid_responce[1]}")
            
            if value.type_name in need_format:
                sql_responce += " = ".join((names[index], f"'{value.value}'"))
            else:
                sql_responce += " = ".join((names[index], f"{value.value}"))

            sql_responce += ", " if index != (len(values) - 1) else ""

        sql_responce += condition

        return sql_responce

    @property
    def responce(self):
        return self.__responce


class Operations:
    def __init__(self, connection, table_link=None):
        self.__connection = connection
        self.query_handler: QueryQueue = connection.queue
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

                insert_query = Insert(
                    self.__connection, one_table, columns_list, [data[i] for i in columns_list], rules
                )
                self.query_handler.add_query(insert_query)
        else:
            if rules == "*":
                insert_query = Insert(self.__connection, table, names, values)
                self.query_handler.add_query(insert_query)
            else:
                insert_query = Insert(
                    self.__connection, table, names, values, rules
                )
                self.query_handler.add_query(insert_query)

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
            select_query = Select(self.__connection, table, names, condition)
            return select_query.get()

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

                Update(self.__connection, one_table, columns_list, [data[i] for i in columns_list], condition)
        else:
            Update(self.__connection, table, column_names, values, condition)

    def __enter__(self):
        return self
    
    def __exit__(self, *args): ...
