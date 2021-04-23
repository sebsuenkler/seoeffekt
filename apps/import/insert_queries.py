import sys
sys.path.insert(0, '..')
from include import *


queries_file = "gesund_bund.csv"
study_id = 10

with open(queries_file, 'r') as csvfile:
    queries = csv.reader(csvfile)

    for query in queries:
        print(query[0])
        Queries.insertQuery(study_id, query[0])
