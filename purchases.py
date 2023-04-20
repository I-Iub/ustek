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
    print('Общий датафрейм:\n', total_dataframe)
    # total_dataframe.to_csv('total_dataframe.csv')

    print('\nЗадание 2')
    print('Сумма по колонке quantity:', total_dataframe['quantity'].sum())

    purchases = total_dataframe.groupby(['name'])['quantity'].sum()
    if purchases.empty:
        names_string = 'Датафрейм пуст'
    else:
        purchases_max_number = purchases.max()
        top_names = [name for name, purchases_number in purchases.items()
                     if purchases_number == purchases_max_number]
        top_names.sort()
        names_string = ', '.join(top_names)
    print('\nЗадание 3')
    print('Больше всех товаров купил пользователь(и):', names_string)

    sorted_purchases_num = (
        total_dataframe.groupby(['product_id'])['quantity'].sum()
        .sort_values(ascending=False)
    )
    top_10 = sorted_purchases_num.head(10)
    print('\nЗадание 4')
    print('Топ-10 товаров по числу проданных единиц за всё время:',
          *list(top_10.keys()))
    purchases_num_df = pd.DataFrame(sorted_purchases_num.items(),
                                    columns=['product_id', 'purchases_number'])
    top_10_sorted = purchases_num_df.sort_values(
        ['purchases_number', 'product_id'], ascending=[False, True]
    ).head(10)
    print('Топ-10 с дополнительной сортировкой по возрастанию ключей:\n',
          top_10_sorted)


if __name__ == '__main__':
    main()
