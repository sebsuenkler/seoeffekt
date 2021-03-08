#sys libs
import os, sys
import os.path

#tool libs
sys.path.insert(0, '..')
from db.connect import DB

sys.path.insert(0, '..')
from db.studies import Studies as DB_Studies

from libs.helpers import Helpers

class Studies:
    def __init__(self):
        self.data = []

    def getStudies():
        db = DB()
        rows = DB_Studies.getStudies(db.cursor)
        db.DBDisconnect()
        return rows

    def getStudiesScraper():
        db = DB()
        rows = DB_Studies.getStudiesScraper(db.cursor)
        db.DBDisconnect()
        return rows

    def getStudy(study_id):
        db = DB()
        rows = DB_Studies.getStudy(db.cursor, study_id)
        db.DBDisconnect()
        return rows
