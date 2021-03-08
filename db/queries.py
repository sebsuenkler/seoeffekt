#Class for search queries table
class Queries:
    def __init__(self, cursor):
        self.cursor = cursor


#read from db



#function to read all queries of a study
    def getQueriesNoScrapers(cursor, study_id):
        sql= "SELECT * from queries LEFT JOIN scrapers on scrapers_queries_id = queries_id WHERE queries_studies_id=%s AND scrapers_progress IS NULL"
        data = (study_id)
        cursor.execute(sql,(data,))
        rows = cursor.fetchall()
        return rows

#function to read all unprocessed queries
    def getOpenQueriesStudy(cursor, study_id):
        sql= "SELECT distinct(queries_id) from queries, scrapers WHERE queries_studies_id=%s AND queries_id = scrapers_queries_id AND scrapers_progress = 0"
        data = (study_id)
        cursor.execute(sql,(data,))
        rows = cursor.fetchall()
        return rows

#open one specific query
    def getQuery(cursor, study_id, query):
        sql= "SELECT * from queries WHERE queries_studies_id=%s AND queries_query=%s"
        data = (study_id, query)
        cursor.execute(sql,(data))
        rows = cursor.fetchall()
        return rows

#open query of a result
    def getQuerybyResult(cursor, results_id):
        sql = "SELECT queries_query FROM queries, results where queries_id = results_queries_id and results_id = %s"
        data = (results_id)
        cursor.execute(sql,(data,))
        rows = cursor.fetchall()
        return rows


#write to db


#function to write query to db
    def insertQuery(cursor, studies_id, query):
        cursor.execute("INSERT INTO queries VALUES(%s,%s);", (studies_id, query,))

#function to write query to db with aditional information
    def insertQueryVal(cursor, studies_id, query, comment, date):
        cursor.execute("INSERT INTO queries (queries_studies_id, queries_query, queries_comment, queries_date) VALUES(%s,%s,%s,%s);", (studies_id, query, comment, date,))
