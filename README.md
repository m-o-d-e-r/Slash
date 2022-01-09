# Скоро
  - Операции с объединенными таблицами
  - Можно будет создавать откат (вот прям скоро)
  - Можно будет пользовательськие правила закинуть в json
  - Можно будет вызывать операцию из таблицы
  - Следующим шагом сделаю норм(+-) документацию

# Новое
  - добавлена возможность записи/чтения правил из json-фалов(rules.json)<p>
     &emsp;Есть два класса которые позволяют это сделать(JsonConverter, WinJsonConverter)<br>
        `JsonConverter` - под все платформы<br>
        `WinJsonConverter` - только под винду(так как для линухи .so)<br>

      &emsp;Решил так сделать для эксперимента.
      А вообще хочу написать какую-то фичу на плюсах и портировать под ORM.<br>
      Мб какой-то валидатор, или парсер. Ну или сделаю пачку модулей для каких-то расчетов. <a href="#WinJsonConverter">Помощь в сборке WinJsonConverter</a>(сборка под линуху такая же).
</p>


```Python
from Slash.types_ import Rules, WinJsonConverter, JsonConverter


rule = Rules()

t = WinJsonConverter(rule.get_rules()) # передача правил для записи в rules.json
t.write()

t.read(rule) # чтение

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
conn.create(table)
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
conn.create(table)

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
conn.create(table)

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
<a href="https://pypi.org/project/Slash92/0.2.1.0/">0.2.1.0</a><br>
<a href="https://pypi.org/project/Slash92/0.2.0/">0.2.0</a><br>
<a href="https://pypi.org/project/Slash92/0.1.9/">0.1.9</a><br>
<a href="https://pypi.org/project/Slash92/0.1.8/">0.1.8</a><br>
<a href="https://pypi.org/project/Slash92/0.1.7.0/">0.1.7.0</a><br>
<a href="https://pypi.org/project/Slash92/0.1.6/">0.1.6</a><br>
<a href="https://pypi.org/project/Slash92/0.1.5/">0.1.5</a><br>
<a href="https://pypi.org/project/Slash92/0.1.4/">0.1.4</a><br>
<a href="https://pypi.org/project/Slash92/0.1.3/">0.1.3</a><br>
<a href="https://pypi.org/project/Slash92/0.1.2/">0.1.2</a><br>
<a href="https://pypi.org/project/Slash92/0.1.1/">0.1.1</a><br>
<a href="https://pypi.org/project/Slash92/0.1.0/">0.1.0</a>

# Собрать .whl
    python setup.py bdist_wheel
    
# Установка через .whl
    pip install Slash92-0.2.1-py3-none-any.whl

# Установка через setup.py
    python setup.py install

# Собрать WinJsonConverter
<div id="WinJsonConverter"></div>
&emsp;Для начала cкопируйте исходник ORM
    
    git clone https://github.com/m-o-d-e-r/Slash.git
  &emsp;<s>Если вас у вас не появился синий экран</s> найдите файл `setup_for_cython.py`, он понадобится для сборки нашей динамической либы.
  Потом с помощью <s>древней</s> команды запустите компиляцию `utils_for_rules.pyx`(этот файл тусит в `Slash/utilities/`, надо чтобы он был в одной папке с `setup_for_cython.py` или изменить путь в `setup_for_cython.py`). В `Slash/utilities/` находится: исходник `WinJsonConverter` и уже скомпилирования его версия, это значит что вы можете не собирать этот модуль заново.

    python setup_for_cython.py build_ext --inplace

  &emsp;<s>Если с вашего монитора ничего не вылезло</s> можете смело перемещать файл с расширением .pyd в `Slash/utilities/`.<br><br><br>
  <b>!!!Важно!!!</b><br>
  
|  Можно  |       Нельзя       |
| ------- | ------------------ |
| Добавлять что-то новое   | Менять имя файла   |
| Гладить кота при сборке(+2 к удаче) | Пить томатный сок  |

&emsp;Если есть какие-то трудности в сборке пишите <a href="https://t.me/M_O_D_E_R">сюда</a>.


  <b>!!!Не сильно важно, но к сути!!!</b><br>
  `Windows` - .pyd<br>
  `Linux` - .so<br>
&emsp;Под каждую ось свое расширение, но питон всё понимает. + вы не будете импортировать эту либу напрямую, хотя конечно это возможно.
