from psycopg2.extensions import connection as psycopg_conn

from db_utils import get_connection, populate_database

task_1_query = """
select product_id, name, price, max_price,
  round((price / max_price) :: numeric, 2) as share_of_max
from (select product_id, name, price, max(price) over() as max_price
      from products) as t
order by price desc, product_id
"""
task_2_query = """
select user_id, order_id,
  rank() over(partition by user_id order by time, order_id) as order_number
from (select user_id, order_id, action, time,
      rank() over(partition by user_id, order_id order by time desc)
      from user_actions) as t1
where rank = 1 and action = 'create_order'
order by user_id, order_number
"""
task_3_query = """
select user_id, order_id,
  rank() over(partition by user_id order by time, order_id) as order_number,
  (time - lag(time, 1) over(partition by user_id order by time, order_id))
  as since_prev_order
from (select user_id, order_id, action, time,
      rank() over(partition by user_id, order_id order by time desc)
      from user_actions) as t1
where rank = 1 and action = 'create_order'
order by user_id, order_number
"""


def main():
    populate_database()
    connection = get_connection()

    for query in task_1_query, task_2_query, task_3_query:
        print(*get_task_results(connection, query), sep='\n')
        print()


def get_task_results(connection: psycopg_conn, query: str) -> None:
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()


if __name__ == '__main__':
    main()
