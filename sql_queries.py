import datetime

import psycopg2
from psycopg2.errors import DuplicateDatabase
from psycopg2.extras import execute_values


connection = psycopg2.connect(dbname='postgres', host='localhost', port=35432,
                              user='postgres', password='ustek')
connection.autocommit = True
with connection.cursor() as cursor:
    try:
        cursor.execute('create database ustek')
    except DuplicateDatabase:
        pass
connection.close()

connection = psycopg2.connect(dbname='ustek', host='localhost', port=35432,
                              user='postgres', password='ustek')
connection.autocommit = True


def main():
    create_tables()
    insert_values()

    print(*get_task_1_results(), sep='\n')
    print()
    print(*get_task_2_results(), sep='\n')
    print()
    print(*get_task_3_results(), sep='\n')


def create_tables():
    with connection.cursor() as cursor:
        # UNIQUE (user_id, order_id, action) -- любой пользователь не может
        # создать заказ с тем же самым номером, как у другого пользователя;
        # UNIQUE (order_id, action) -- не может быть такого, что заказ
        # создан, отменён, а затем снова создан с тем же самым order_id;
        # UNIQUE (user_id, order_id, time) -- не может быть такого, что
        # произошло одновременно создание и удаление
        cursor.execute("""
            create table if not exists user_actions (
                id integer primary key,
                user_id integer not null,
                order_id integer not null,
                action varchar(50) not null,
                time timestamp with time zone not null,
                unique (user_id, order_id, action),
                unique (order_id, action),
                unique (user_id, order_id, time)
            )
        """)
        cursor.execute("""
            create table if not exists products (
                id integer primary key,
                name varchar(50) not null,
                price float4 not null
            )
        """)


actions_values = [
    # user_id = 1
    # заказ создан, затем отменён
    (10, 1, 100, 'create_order', datetime.datetime(2023, 4, 19, 12, 10)),
    (11, 1, 100, 'cancel_order', datetime.datetime(2023, 4, 19, 12, 20)),
    # заказ только отменён
    (12, 1, 101, 'cancel_order', datetime.datetime(2023, 4, 19, 12, 1)),
    (13, 1, 103, 'cancel_order', datetime.datetime(2023, 4, 19, 12, 11)),
    (14, 1, 105, 'cancel_order', datetime.datetime(2023, 4, 19, 12, 20)),
    # заказ только создан (order_by = 104 создан раньше чем 102)
    (15, 1, 102, 'create_order', datetime.datetime(2023, 4, 19, 12, 10)),
    (16, 1, 104, 'create_order', datetime.datetime(2023, 4, 19, 12, 2)),
    (17, 1, 106, 'create_order', datetime.datetime(2023, 4, 19, 12, 20)),
    # отменён, позже создан (возможно ли такое?);
    # совпадает по времени создания с order_by = 104
    (18, 1, 107, 'cancel_order', datetime.datetime(2023, 4, 19, 12, 10)),
    (19, 1, 107, 'create_order', datetime.datetime(2023, 4, 19, 12, 30)),

    # user_id = 2
    # заказ создан, затем отменён
    (20, 2, 200, 'create_order', datetime.datetime(2023, 4, 19, 12, 10)),
    (21, 2, 200, 'cancel_order', datetime.datetime(2023, 4, 19, 12, 20)),
    # заказ только отменён
    (22, 2, 201, 'cancel_order', datetime.datetime(2023, 4, 19, 13, 40)),
    (23, 2, 202, 'cancel_order', datetime.datetime(2023, 4, 19, 13, 40)),
    # заказ только создан
    (24, 2, 203, 'create_order', datetime.datetime(2023, 4, 19, 12, 30)),
    (25, 2, 204, 'create_order', datetime.datetime(2023, 4, 19, 12, 30)),
    # отменён, затем создан
    (26, 2, 205, 'cancel_order', datetime.datetime(2023, 4, 19, 12, 20)),
    (27, 2, 205, 'create_order', datetime.datetime(2023, 4, 19, 12, 30)),
]
product_values = [
    (1, 'хлеб', 54),
    (2, 'молоко', 70),
    (3, 'мясо', 500),
    (4, 'творог', 100),
    (5, 'макароны', 49),
]


def insert_values():
    with connection.cursor() as cursor:
        execute_values(
            cursor,
            'insert into user_actions (id, user_id, order_id, action, time) '
            'values %s',
            actions_values
        )
        execute_values(
            cursor,
            'insert into products (id, name, price) values %s',
            product_values
        )


task_1_query = """
select id, price, max_price, round((price / max_price) :: numeric, 2) as share
from (select id, name, price, max(price) over () as max_price
      from products) as t
order by price desc, id
"""


def get_task_1_results():
    with connection.cursor() as cursor:
        cursor.execute(task_1_query)
        return cursor.fetchall()


task_2_query = """
select user_id, order_id,
  rank() over (partition by user_id order by time, order_id) as order_number
from (select user_id, order_id, action, time,
      rank() over(partition by user_id, order_id order by time desc)
      from user_actions) as t1
where rank = 1 and action = 'create_order'
order by user_id, order_number
"""


def get_task_2_results():
    with connection.cursor() as cursor:
        cursor.execute(task_2_query)
        return cursor.fetchall()


task_3_query = """
select user_id, order_id, order_number, (time - prev_time) as since_prev_order
from (
  select user_id, order_id, time, lag(time, 1) over() as prev_time,
    rank() over (partition by user_id order by time, order_id) as order_number
  from (select user_id, order_id, action, time,
        rank() over(partition by user_id, order_id order by time desc)
        from user_actions) as t1
  where rank = 1 and action = 'create_order'
  order by user_id, order_number
) as t2
"""


def get_task_3_results():
    with connection.cursor() as cursor:
        cursor.execute(task_3_query)
        return cursor.fetchall()


if __name__ == '__main__':
    main()
