#sys libs
import os, sys
import os.path

#tool libs
sys.path.insert(0, '..')
from db.connect import DB

sys.path.insert(0, '..')
from db.queries import Queries as DB_Queries

from libs.helpers import Helpers

# class for queries functions; mainly to read and write database content
class Queries:
    def __init__(self):
        self.data = []

#read from db

#function to read all queries of a study
    def getQueriesNoScrapers(study_id):
        db = DB()
        rows = DB_Queries.getQueriesNoScrapers(db.cursor, study_id)
        db.DBDisconnect()
        return rows

#function to read all unprocessed queries
    def getOpenQueriesStudy(study_id):
        db = DB()
        rows = DB_Queries.getOpenQueriesStudy(db.cursor, study_id)
        db.DBDisconnect()
        return rows

#open one specific query
    def getQuery(study_id, query):
        db = DB()
        rows = DB_Queries.getQuery(db.cursor, study_id, query)
        db.DBDisconnect()
        return rows

#open query of a result
    def getQuerybyResult(results_id):
        db = DB()
        rows = DB_Queries.getQuerybyResult(db.cursor, results_id)
        db.DBDisconnect()
        return rows


#write to db

#function to write query to db
    def insertQuery(study_id, query):
        db = DB()
        DB_Queries.insertQuery(db.cursor, study_id, query)
        db.DBDisconnect()

#function to write query to db with aditional information
    def insertQueryVal(study_id, query, comment, date):
        db = DB()
        DB_Queries.insertQueryVal(db.cursor, study_id, query, comment, date)
        db.DBDisconnect()
