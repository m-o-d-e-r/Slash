from .core import CheckDatas

from .exeptions_ import SlashRulesError

class Insert():
    def __init__(self, conn, table_name, names, values, rules="*"):
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

class Update():
    def __init__(self, conn, table_name, names, values, rules="*"):
        responce = self.__validate(table_name, names, values, rules)
        conn.execute(CheckDatas.checkSQL(responce, "update"))

class Delete():
    def __init__(self, conn, table_name, names, condition):
        print(condition)


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

    def delete(self, connection, table_name, names, condition):
        Delete(connection, table_name, names, condition)

