import datetime
from pathlib import Path

import pandas as pd

target_dir = Path('data')


def get_total_df(target_dir: Path) -> pd.DataFrame:
    all_dataframes = []
    for date_dir in target_dir.iterdir():
        if date_dir.is_file():
            continue
        date = datetime.datetime.strptime(str(date_dir.name), '%Y-%m-%d')
        for user_dir in date_dir.iterdir():
            if user_dir.is_file():
                continue
            name = user_dir.name
            for file in user_dir.iterdir():
                df = pd.read_csv(file)
                del df[df.columns[0]]
                frame_length = len(df.index)
                df['name'] = [name] * frame_length
                df['date'] = [date] * frame_length
                all_dataframes.append(df)

    return pd.concat(all_dataframes)


def main():
    total_dataframe = get_total_df(target_dir)
    print('Задание 1')
    print('Общий датафрейм:')
    print(total_dataframe)

    # total_dataframe.to_csv('total_dataframe.csv')

    print('\nЗадание 2')
    print('Сумма по колонке quantity:', total_dataframe['quantity'].sum())

    top_users = (total_dataframe.groupby(['name'])['quantity'].sum()
                 .sort_values(ascending=False))
    if top_users.empty:
        names_string = 'Датафрейм пуст'
    else:
        max_sum = top_users.values[0]
        top_names = [
            name for name, value in top_users.items() if value == max_sum
        ]
        top_names.sort()
        names_string = ', '.join(top_names)
    print('\nЗадание 3')
    print('Больше всех товаров купил пользователь(и):', names_string)

    top_10 = (total_dataframe.groupby(['product_id'])['quantity'].sum()
              .sort_values(ascending=False).head(10))
    print('\nЗадание 4')
    print('Топ-10 товаров по числу проданных единиц за всё время:',
          list(top_10.keys()))


if __name__ == '__main__':
    main()
