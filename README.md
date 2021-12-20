# Скоро
  - Упрощение работы с таблицами

# Новое
  - TablesManager

```Python
from Slash.types_ import Column, Table, TablesManager, Int, Text
from Slash.Core.core import Connection

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)


table1 = Table("test1")
table1.set_columns(Column(Int, "age"))
table2 = Table("test2")
table2.set_columns(Column(Int, "name"))
table3 = Table("test3")
table3.set_columns(Column(Int, "age"), Column(Text, "name"))


print(TablesManager.find_by_name("test3"))
print(TablesManager.find_one_by_column("age", "name"))
print(TablesManager.find_many_by_column("age"))


unatedTable = TablesManager.unite(table1, table2)
print(unatedTable.name)
print(unatedTable.columns)

conn.close()
```

# Файлы
  - `Slash/types_.py` <p>Базовые типы, класс для валидации типов(за правилами)</p>
  - `Slash/Core/core.py` <p>Создание подключения, классы валидации, расширение SQL-запросов</p>
  - `Slash/Core/exeptions_.py` <p>Исключения</p>
  - `Slash/Core/operations_.py` <p>Операции с БД</p>

# Создание подключения
  ```Python
from Slash.Core.core import Connection

conn = Connection("Slash", "postgres", "root", "127.0.0.1", 5432)
   ```
   - `"Slash"` - имя базы данных<br>
   - `"postgres"` - имя пользователя<br>
   - `"root"` - пароль<br>
   - `"127.0.0.1"` - хост<br>
   - `5432` - порт<br>

# Создать свои правили валидации
 ```Python
 from Slash.types_ import Rules

class MyRules(Rules):
    def __init__(self): ...

# нормально работает валидация для строки и числа, всё остальное будет позже
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
 ```
  Данные проходят валидацию нескольких уровней.
  - проверка на валидность входных строк
  - проверка данных(за правилом) на валидность
  - проверка на валидность SQL-запроса

  Если данные не проходят один уровень, будет поднято исключения:
  - `SlashBadColumnNameError` - Неправильное имя колонки(содержание знаков пунктуации) => Проверка осуществляется в `core.py`
  - `SlashRulesError` - Несоответствие правилам => Проверка осуществляется в `types_.py`
  - `SlashPatternMismatch` - Несоответствие шаблонному SQL-запросов => Проверка осуществляется в `core.py`

# Операции

Создать таблицу
```Python
from Slash.types_ import Column, Table, Int, Text
from Slash.Core.core import Connection

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

table = Table("test1")
table.set_columns(Column(Int, "age"), Column(Text, "name"))
table.create(conn)
```

Вставка данных
```Python
from Slash.types_ import Column, Table, Int, Text, Rules
from Slash.Core.core import Connection
from Slash.Core.operations_ import Operations


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

operations.insert(table.name, ("age", "name"), (Int(1000), Text("Name2")), rules=myRules)
# или (но базовые правила сильно ограничены)
operations.insert(table.name, ("age", "name"), (Int(1000), Text("Name2"))) # SlashRulesError
```

Обновление данных
```Python
from Slash.types_ import AutoField, Column, Table, Int, Text
from Slash.Core.core import Connection, SQLConditions
from Slash.Core.operations_ import Operations

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

table = Table("test1")
table.set_columns(Column(Int, "age"), Column(Text, "name"))
table.create(conn)

Operations(conn).update(
    table.name,
    ("name", ),
    (Text("33"), ),
    SQLConditions.where(
        "age", SQLConditions.LE, "3"
    )
)
```

Удаление данных
```Python
from Slash.Core.core import Connection, SQLConditions
from Slash.Core.operations_ import Operations

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

# удаление с условием
Operations(conn).delete(
    table.name, SQLConditions.where(
        "age", SQLConditions.LE, 100
    )
)

# удаление без условий
Operations(conn).delete(table.name)
```

Выборка данных
```Python
from Slash.Core.core import Connection, SQLConditions
from Slash.Core.operations_ import Operations

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

# выборка даннных за условем из сортировкой
print(
    Operations(conn).select(
        table.name,
        ("age", "name"),
        SQLConditions.where(
            "age", SQLConditions.EQ, 3,
            SQLConditions.order_by("age", desc="desc")   
        )
    )
)
```
# PyPI
<a href="https://pypi.org/project/Slash92/0.1.4/">0.1.5</a><br>
<a href="https://pypi.org/project/Slash92/0.1.4/">0.1.4</a><br>
<a href="https://pypi.org/project/Slash92/0.1.3/">0.1.3</a><br>
<a href="https://pypi.org/project/Slash92/0.1.2/">0.1.2</a><br>
<a href="https://pypi.org/project/Slash92/0.1.1/">0.1.1</a><br>
<a href="https://pypi.org/project/Slash92/0.1.0/">0.1.0</a>

# Собрать .whl
    python setup.py bdist_wheel
    
# Установка через .whl
    pip install Slash92-0.1.5-py3-none-any.whl

# Установка через setup.py
    python setup.py install

Скоро допишу и поправлю текст)
Также буду изменять синтаксис условий
