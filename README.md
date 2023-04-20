
## Инструкция по запуску скриптов

---
### Задание по SQL
Если нужно просто посмотреть SQL-запросы:
- [задание 1](https://github.com/I-Iub/ustek/blob/main/queries.py#L5)
- [задание 2](https://github.com/I-Iub/ustek/blob/main/queries.py#L11)
- [задание 3](https://github.com/I-Iub/ustek/blob/main/queries.py#L20)

Можно также запустить скрипт `queries.py`, который эти заросы выполнит и 
результаты выведет в консоль. Для этого нужно выполнить следующие шаги.
Клонировать проект, создать виртуальное окружение, установить зависимости
```
git clone https://github.com/I-Iub/ustek.git
cd ustek
python -m venv venv  # срипты написаны под версию python 3.10
. venv/bin/activate  # если Linux
pip install --upgrade pip
pip install -r requirements.txt
```
Для работы скрипта `queries.py`, нужна база данных. Её можно запистить, 
например, в контейнере командой:
```
docker run --name ustek -e POSTGRES_PASSWORD=ustek -p 35432:5432 -d postgres:14.5-alpine
```
Параметры, указанные в команде соответствуют указанным в скрипте 
[здесь](https://github.com/I-Iub/ustek/blob/main/db_utils.py#L17) 
(подключение к базе данных `postgres` для создание базы данных `ustek`) и 
[здесь](https://github.com/I-Iub/ustek/blob/main/db_utils.py#L30) 
(подключение к базе данных `ustek`)
Запустить скрипт:
```
python queries.py
```
Если нужно подключиться к базе данных в контейнере (будет работать только 
после запуска `python queries.py`, т.к. этот скрипт создаёт базу данных `ustek`):
```
psql -U postgres -h localhost -p 35432 -d ustek -W
```
Ввести пароль `"ustek"`.

---
### Задание по Pandas (Python)

Если ещё не выполнены нижеследующие команды (как в разделе "Задание по SQL" выше), 
то выполнить их:
```
git clone https://github.com/I-Iub/ustek.git
cd ustek
python -m venv venv  # срипты написаны под версию python 3.10
. venv/bin/activate  # если Linux
pip install --upgrade pip
pip install -r requirements.txt
```
Запустить скрипт:
```
python purchases.py
```
---
### Комментарии к решению задания по SQL
В задании 2 указано: "Отменённые заказы не учитывайте." Запрос работает таким 
образом, что отменённым заказ считается, если последняя запись 
(определяемая по полю `time`) с этим номером в поле `actions` имеет значение 
`create_order`. Также запрос полагается на наличие ограничений в таблице, 
которые указаны [здесь](https://github.com/I-Iub/ustek/blob/main/db_utils.py#L38).
Я посчитал наличие таких ограничений логичным, но о том, что они есть не 
указано в условии задания.

В запросах `task_2_query` и `task_2_query` есть условия `where rank = 1`.
Благодаря тому, что в выражении `over` оконной функции `rank` в этом запросе 
указано `order by time, order_id` и одновременно в таблице есть ограничение 
`unique (user_id, order_id, time)` не может быть больше одной строки 
для каждой группы (раздела) где `rank = 1`. Здесь группа определяется 
`partition by user_id, order_id` в выражении `over`. Т.е. запрос будет 
корректно работать, только если в таблице будет ограничение 
`unique (user_id, order_id, time)`. Этого условия нет в постановки задачи, но 
решение полагается на его наличие.
