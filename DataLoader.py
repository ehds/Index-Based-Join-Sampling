import pandas as pd
import os

# CSV files location
data_loc = 'data/'
csv_loc = data_loc + 'csv/'
pkl_loc = data_loc + 'pkl/'

percentages = {
    'cast_info': 0.03,
    'char_name': 0.25,
    'movie_companies': 0.3,
    'movie_info': 0.06,
    'movie_keyword': 0.5,
    'name': 0.15,
    'person_info': 0.15,
    'title': 0.2
}
# Create data directory
if not os.path.exists(csv_loc):
    os.mkdir(csv_loc)
if not os.path.exists(pkl_loc):
    os.mkdir(pkl_loc)

# Load all the data columns
columns = dict()
with open(data_loc + 'csv_schema.txt', 'r') as f:
    lines = f.readlines()
    for l in lines:
        l = l.replace('\n', '').split(',')
        columns[l[0]] = l[1:]


def load_csv(name, test=False):
    """ Load the given CSV file only """
    assert isinstance(name, str) and name in columns.keys()
    assert isinstance(test, bool)
    if test:
        df = pd.read_csv(csv_loc + name + '.csv', nrows=10000, header=None, escapechar='\\',
                         names=columns[name])
    else:
        #tp = pd.read_csv(csv_loc + name + '.csv', iterator=True, chunksize=10000, header=None, escapechar='\\',
        #                 names=columns[name])
        tp = pd.read_csv(csv_loc + name + '.csv', header=None, escapechar='\\',
                         names=columns[name])
    df = tp
    print("Load finished")
    df.relation_name = name
    return df


def load_pickle(name):
    """ Load the given CSV file only """
    assert isinstance(name, str) and name in columns.keys()
    df = pd.read_pickle(pkl_loc + name + '.pkl')
    return df


def load_all_csv(test=False):
    """ Load all the csv data files """
    assert isinstance(test, bool)
    dfs = []
    for k in columns.keys():
        print('Loading %s' % k)
        dfs.append(load_csv(k, test))
    return dfs


def get_table_names():
    from os import walk
    filenames = [f.split('.')[0] for f in next(walk(pkl_loc))[
        2] if f.split('.')[1] == 'pkl']
    return filenames


def is_column_name(c):
    return any(c in cols for cols in columns.values())


if __name__ == "__main__":
    print(is_column_name('person_role_id'))

    # Pickle all the files
    table_names = get_table_names()
    # print(set(columns.keys())-set(table_names))
    for k in columns.keys():
        if k in table_names:
            continue
        print('Pickling %s' % k)
        df = load_csv(k)
        if k in percentages:
            size = int(percentages[k] * df.shape[0])
            df = df.sample(size)
        df.to_pickle(pkl_loc + k + '.pkl')
        del df
