
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
Запустить скрипт который выведет результаты в консоль:
```
python purchases.py
```
