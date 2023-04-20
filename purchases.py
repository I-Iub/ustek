import datetime
from pathlib import Path

import pandas as pd

base_dir = Path('data')


def get_total_df():
    all_dataframes = []
    for date_dir in base_dir.iterdir():
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


print(get_total_df())
