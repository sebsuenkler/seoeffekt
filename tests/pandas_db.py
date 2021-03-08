import pandas as pd
import psycopg2 as pg

import numpy as np

import sys

import csv

dbname = "seoeffekt"
user = "seo"
host = "207.180.229.184"
password = "b2ftbudj*"



#Evaluations Results

csv_header = 'hash,module,result'

csv_file = 'evaluations.csv'

with open(csv_file,'w+') as f:
    f.write(csv_header)
f.close()

offset = 0
next = 50000

i = 0

save_res = ""

connection = pg.connect("dbname='"+dbname+"' user='"+user+"' host='"+host+"' " + \
                  "password='"+password+"'")

count_sql = "SELECT count(evaluations_id) from evaluations"

counter_pd = pd.read_sql_query(count_sql, connection)

counter = counter_pd['count'].values[0]

counter = int(counter / next)

#counter = 2


for i in range(0, counter):
    connection = pg.connect("dbname='"+dbname+"' user='"+user+"' host='"+host+"' " + \
                      "password='"+password+"'")

    cur = connection.cursor()

    sql = "SELECT evaluations_results_hash, evaluations_module, evaluations_result from evaluations ORDER BY evaluations_results_hash ASC offset "+str(offset)+" fetch next "+str(next)+" rows only"

    print(sql)



    cur.execute(sql)

    rows = cur.fetchall()

    offset = offset + next

    connection = None

    for row in rows:
        value = ""
        build_res = ""
        hash = str(row[0])
        module = str(row[1])
        value = str(row[2])

        build_res = hash+','+module+','+value

        save_res = '\n'+build_res

        with open(csv_file,'a+') as f:
            f.write(save_res)
        f.close()




#Classifications Results

csv_header = 'hash,class'

csv_file = 'classifications.csv'

with open(csv_file,'w+') as f:
    f.write(csv_header)
f.close()

offset = 0

next = 50000

i = 0

save_res = ""

connection = pg.connect("dbname='"+dbname+"' user='"+user+"' host='"+host+"' " + \
                  "password='"+password+"'")

count_sql = "SELECT count(classifications_id) from classifications"

counter_pd = pd.read_sql_query(count_sql, connection)

counter = counter_pd['count'].values[0]

counter = int(counter / next)

for i in range(0, counter):
    connection = pg.connect("dbname='"+dbname+"' user='"+user+"' host='"+host+"' " + \
                      "password='"+password+"'")

    cur = connection.cursor()

    sql = "SELECT classifications_hash, classifications_result from classifications ORDER BY classifications_hash ASC offset "+str(offset)+" fetch next "+str(next)+" rows only"

    print(sql)

    cur.execute(sql)

    rows = cur.fetchall()

    offset = offset + next

    connection = None

    for row in rows:
        value = ""
        build_res = ""
        hash = str(row[0])
        value = str(row[1])

        build_res = hash+','+value

        save_res = '\n'+build_res

        with open(csv_file,'a+') as f:
            f.write(save_res)
        f.close()


#Results Results

save_res = ""

csv_header = 'results_studies_id,results_id,results_position,results_queries_id,results_url,results_main,results_se,hash'

csv_file = 'results.csv'

with open(csv_file,'w+') as f:
    f.write(csv_header)
f.close()

offset = 0

next = 50000

i = 0

connection = pg.connect("dbname='"+dbname+"' user='"+user+"' host='"+host+"' " + \
                  "password='"+password+"'")

count_sql = "SELECT count(results_id) from results"

counter_pd = pd.read_sql_query(count_sql, connection)

counter = counter_pd['count'].values[0]

counter = int(counter / next)

for i in range(0, counter):
    connection = pg.connect("dbname='"+dbname+"' user='"+user+"' host='"+host+"' " + \
                      "password='"+password+"'")

    cur = connection.cursor()

    sql = "select results_id, results_studies_id, results_position, results_queries_id, results_url, results_main, results_se, results_hash from results ORDER BY results_hash ASC offset "+str(offset)+" fetch next "+str(next)+" rows only"

    print(sql)

    cur.execute(sql)

    rows = cur.fetchall()

    offset = offset + next

    connection = None

    for er in rows:

        build_res = ""
        results_id = str(er[0])
        study = str(er[1])
        results_pos = str(er[2])
        query_id = str(er[3])
        url = str(er[4])
        url = '"'+url+'"'
        main = str(er[5])
        main = '"'+main+'"'
        se = str(er[6])
        hash = str(er[7])


        build_res = study+','+results_id+','+results_pos+','+query_id+','+url+','+main+','+se+','+hash

        save_res = '\n'+build_res

        with open(csv_file,'a+') as f:
            f.write(save_res)
        f.close()








#Results Speed
save_res = ""

csv_file = 'speed.csv'

csv_header = 'hash,speed'


with open(csv_file,'w+') as f:
    f.write(csv_header)
f.close()


offset = 0

next = 50000

i = 0

connection = pg.connect("dbname='"+dbname+"' user='"+user+"' host='"+host+"' " + \
                  "password='"+password+"'")

count_sql = "SELECT count(sources_id) from sources"

counter_pd = pd.read_sql_query(count_sql, connection)

counter = counter_pd['count'].values[0]

counter = int(counter / next)

for i in range(0, counter):
    connection = pg.connect("dbname='"+dbname+"' user='"+user+"' host='"+host+"' " + \
                      "password='"+password+"'")

    cur = connection.cursor()

    sql = "select sources_hash, sources_speed from sources ORDER BY sources_hash ASC offset "+str(offset)+" fetch next "+str(next)+" rows only"

    print(sql)

    cur.execute(sql)

    rows = cur.fetchall()

    offset = offset + next

    connection = None

    for er in rows:

        build_res = ""
        hash = str(er[0])
        speed = str(er[1])


        build_res = hash+','+speed

        save_res = '\n'+build_res

        with open(csv_file,'a+') as f:
            f.write(save_res)
        f.close()



print("Load: results.csv")
print("\n")

results_df = pd.read_csv('results.csv', error_bad_lines=False, low_memory=False)




print("Load: queries.csv")
print("\n")

queries_df = pd.read_csv('queries.csv', error_bad_lines=False, low_memory=False)


print("Load: speed.csv")
print("\n")

speed_df = pd.read_csv('speed.csv', error_bad_lines=False, low_memory=False)



print("Load: classifications.csv")
print("\n")

classfications_df = pd.read_csv('classifications.csv', error_bad_lines=False, low_memory=False)



print("Load: evaluations.csv")
print("\n")

evaluations_df = pd.read_csv('evaluations.csv', error_bad_lines=False, low_memory=False)


evaluations_df = evaluations_df.groupby('hash').agg(lambda x: list(x))


print("Merge: results speed")
print("\n")

results_speed_merged = results_df.merge(speed_df, left_on='hash', right_on='hash')



print("Merge: results speed evaluations")
print("\n")

results_speed_evaluations_merged = results_speed_merged.merge(evaluations_df, left_on='hash', right_on='hash')




print("Merge: results speed evaluations queries")
print("\n")

results_speed_evaluations_queries_merged = results_speed_evaluations_merged.merge(queries_df, left_on='results_queries_id', right_on='queries_id')



print("Merge: results speed evaluations queries classifications")
print("\n")


results_speed_evaluations_queries_classifications_merged = results_speed_evaluations_queries_merged.merge(classfications_df, left_on='hash', right_on='hash')

#print(results_speed_evaluations_queries_merged.iloc[3])

#print(results_speed_evaluations_queries_merged)

print("Save: seo_results.csv")
print("\n")


results_speed_evaluations_queries_classifications_merged.to_csv(r'seo_results.csv', index = False)

print("Finished")
print("\n")
