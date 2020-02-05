import glob
import pandas as pd


def read_parquet_to_pandas(folder_uri, columns):
    file_list = glob.glob(folder_uri + '/*.parquet')
    df = pd.DataFrame([], columns=columns)
    if len(file_list) > 0:
        for file in file_list:
            file_df = pd.read_parquet(file)
            df = pd.concat([df, file_df], sort=False)
    else:
        pass
    return df


def read_txt_to_list(file_name):
    nlist = []
    try:
        with open(file_name, 'r') as file:
            text = file.readlines()
            for line in text:
                current_place = line[:-1]
                nlist.append(current_place)
    except FileNotFoundError:
        pass
    return nlist
