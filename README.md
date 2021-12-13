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
   - `"postgres"` - имя пользлвателя<br>
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
  - `SlashBadColumnNameError` - Не правильное имя колонки(содержание знаков пунктуации) => Проверка осуществляется в `core.py`
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

operations.insert(table.get_name(), ("age", "name"), (Int(1000), Text("Name2")), rules=myRules)
# или (но базовые правила сильно ограничены)
operations.insert(table.get_name(), ("age", "name"), (Int(1000), Text("Name2"))) # SlashRulesError
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
    table.get_name(), SQLConditions.where(
        "age", SQLConditions.LE, 100
    )
)

# удаление без условий
Operations(conn).delete(table.get_name())
```

Выборка данных
```Python
from Slash.Core.core import Connection, SQLConditions
from Slash.Core.operations_ import Operations

conn = Connection(
    "Slash", "postgres", "root", "127.0.0.1", 5432
)

# выборка даннных за условем с сортировкой
print(
    Operations(conn).select(
        table.get_name(),
        ("age", "name"),
        SQLConditions.where(
            "age", SQLConditions.EQ, 3,
            SQLConditions.order_by("age", desc="desc")   
        )
    )
)
```


Скоро допишу и попралю текст)
Также буду изменять синтаксис условий
