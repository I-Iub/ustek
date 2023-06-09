import datetime

import psycopg2
from psycopg2.errors import DuplicateDatabase
from psycopg2.extensions import connection as psycopg_conn
from psycopg2.extras import execute_values


def populate_database() -> None:
    _create_database()
    connection = get_connection()
    _create_tables(connection)
    _insert_values(connection)


def _create_database() -> None:
    connection = psycopg2.connect(dbname='postgres', host='localhost',
                                  port=35432, user='postgres',
                                  password='ustek')
    connection.autocommit = True
    with connection.cursor() as cursor:
        try:
            cursor.execute('create database ustek')
        except DuplicateDatabase:
            pass
    connection.close()


def get_connection() -> psycopg_conn:
    connection = psycopg2.connect(dbname='ustek', host='localhost', port=35432,
                                  user='postgres', password='ustek')
    connection.autocommit = True
    return connection


def _create_tables(connection: psycopg_conn) -> None:
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
                product_id integer primary key,
                name varchar(50) not null,
                price float4 not null
            )
        """)


actions_values = [
    # user_id = 1
    # заказ создан, затем отменён
    # (10, 1, 100, 'create_order', datetime.datetime(2023, 4, 19, 12, 10)),
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
    # совпадает по времени создания с order_id = 106
    (18, 1, 107, 'cancel_order', datetime.datetime(2023, 4, 19, 12, 10)),
    (19, 1, 107, 'create_order', datetime.datetime(2023, 4, 19, 12, 20)),

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
    (1, 'хлеб', 54.4),
    (2, 'молоко', 70),
    (3, 'мясо', 500),
    (4, 'творог', 100),
    (5, 'макароны', 54.4),
]


def _insert_values(connection: psycopg_conn) -> None:
    with connection.cursor() as cursor:
        execute_values(
            cursor,
            'insert into user_actions (id, user_id, order_id, action,'
            'time) values %s',
            actions_values
        )
        execute_values(
            cursor,
            'insert into products (product_id, name, price) values %s',
            product_values
        )
