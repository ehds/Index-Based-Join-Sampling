import glob
import os
data_loc = "data/"


def extract_schema_txt(schema_sql="join-order-benchmark/schema.sql"):
    """ extract schema txt from schema.sql to schema.txt
        Args:
            schema_sql: path to schema.sql
    """
    columns = dict()
    current_table = None
    current_columns = []
    with open(schema_sql, 'r') as f:
        lines = f.readlines()
        for line in lines:
            # erase white space at the begin and end
            line = line.strip()
            if line.startswith("CREATE"):
                current_table = line.split(' ')[2]
            # end of the table define
            elif line.startswith(")"):
                columns[current_table] = current_columns
                current_columns = []
                current_table = None
                continue
            # columns of the table
            else:
                column = line.split(" ")[0]
                if len(column) > 0:
                    current_columns.append(column)
    # save result to schema.txt
    out_file = data_loc+"csv_schema.txt"
    with open(out_file, "w") as f:
        for item in columns:
            data = []
            data.append(item)
            data.extend(columns[item])
            f.write(",".join(data))
            f.write("\n")


def extract_join_sql(sql_dir="join-order-benchmark", max_join_size=6):
    """ extract all sql that join size not greater than max_join_size
        Args:
            sql_dir: dir to join order benchamrk
            max_join_size: max join size
    """
    # Just get benchamrk sql
    from SelectParser import get_where
    files_match = sql_dir+"/[0-9]*.sql"
    files = glob.glob(files_match)
    filter_sql_file = data_loc+"all-queries-filtered.sql"
    with open(filter_sql_file, 'w') as filter_file:
        for file in files:
            with open(file, 'r') as f:
                sql = f.read().replace("\n", " ")
                joins, _ = get_where(sql)
                if len(joins) <= 6:
                    filter_file.write(sql+"\n")


if __name__ == "__main__":
    if not os.path.exists(data_loc):
        os.mkdir(data_loc)
    extract_schema_txt()
    extract_join_sql()
