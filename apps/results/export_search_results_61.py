#!!!
#sys libs
import sys
sys.path.insert(0, '..')
from include import *

tmp = 'tmp/'


next = 1000


#Results Results

db = DB()

cur = db.cursor

save_res = ""

csv_header = 'results_studies_id,results_id,results_position,results_queries_id,query,results_url,results_main,results_se,hash'

csv_file = 'results_61.csv'

with open(tmp+csv_file,'w+') as f:
    f.write(csv_header)
f.close()

offset = 0

i = 0

sql = "SELECT count(results_id) from results, queries where queries_id = results_queries_id and queries_query not like '%&uule=%' and queries_studies_id = 61"

cur.execute(sql)

rows = cur.fetchall()

db.DBDisconnect()

counter = rows[0][0]

counter = int(round(counter+0.5) / next) + 1

for i in range(0, counter):

    db = DB()

    cur = db.cursor

    sql = "select results_id, results_studies_id, results_position, results_queries_id, queries_query, results_url, results_main, results_se, results_hash from results, queries where results_queries_id = queries_id and queries_studies_id = 61 and results_position < 20 and queries_query not like '%&uule=%' order by queries_id, results_position ASC offset "+str(offset)+" fetch next "+str(next)+" rows only"

    print(sql)

    cur.execute(sql)

    rows = cur.fetchall()

    db.DBDisconnect()

    offset = offset + next

    connection = None

    for er in rows:

        build_res = ""
        results_id = str(er[0])
        study = str(er[1])
        results_pos = str(er[2])
        query_id = str(er[3])
        query = str(er[4])
        query = query.replace('"', "")
        url = str(er[5])
        url = '"'+url+'"'
        main = str(er[6])
        main = '"'+main+'"'
        se = str(er[7])
        hash = str(er[8])


        build_res = study+','+results_id+','+results_pos+','+query_id+','+query+','+url+','+main+','+se+','+hash

        save_res = '\n'+build_res

        with open(tmp+csv_file,'a+') as f:
            f.write(save_res)
        f.close()
