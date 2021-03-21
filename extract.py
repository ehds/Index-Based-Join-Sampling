data_file = "/home/ehds/data/join-order-benchmark-master/schema.sql"

columns = dict()
current_table = None
current_columns = []
with open(data_file, 'r') as f:
    lines = f.readlines()
    for line in lines:
        # erase white space at the begin and end
        line = line.strip()
        if line.startswith("CREATE"):
            current_table = line.split(' ')[2]
        # end of the table def
        elif line.startswith(")"):
            columns[current_table] = current_columns
            current_columns = []
            current_table = None
            continue
        # columns
        else:
            column = line.split(" ")[0]
            if len(column) > 0:
                current_columns.append(column)

print(columns)
with open("data/csv_schema.txt", "w") as f:
    for item in columns:
        data = []
        data.append(item)
        data.extend(columns[item])
        f.write(",".join(data))
        f.write("\n")
