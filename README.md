An implementation of the algorithms presented in the paper "Cardinality Estimation Done Right: Index-Based Join Sampling"

Step：
1. Downlad dataset from http://homepages.cwi.nl/~boncz/job/imdb.tgz, extract all csv file to `data/csv`.
more infomation please refer to [join-order-benchmark](https://github.com/gregrahn/join-order-benchmark)

2. Install dependencies
    ```shell
    # Update job repository
    git submodule init
    git submodule update
    # install python dependencies
    pip install -r requirements.txt
    ```

3. Generate `csv_schema.txt` and `all-queries-filtered.sql`
    ```
    python3 extract.py
    ```

4. Generate pkl data for every relation
    ```
    python3 DataLoader.py
    ```

5.  Run main and test
    ```
    python3 main.py
    python3 test.py
    ```
