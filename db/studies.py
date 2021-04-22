#Class for studies table
class Studies:
    def __init__(self, cursor):
        self.cursor = cursor

    def getStudies(cursor):
        cursor.execute("SELECT * from studies")
        rows = cursor.fetchall()
        return rows

    def getStudiesScraper(cursor):
        cursor.execute("SELECT * from studies WHERE import IS NULL")
        rows = cursor.fetchall()
        return rows

    def getStudy(cursor, id):
        sql= "SELECT * from studies WHERE studies_id=%s"
        data = (id)
        cursor.execute(sql,(data,))
        rows = cursor.fetchall()
        return rows

    def getStudybyName(cursor, studies_name):
        sql= "SELECT studies_name, studies_comment, studies_date, studies_se, studies_id from studies WHERE studies_name=%s"
        data = (studies_name)
        cursor.execute(sql,(data,))
        rows = cursor.fetchall()
        return rows

    def getStudybyNamenotID(cursor, studies_name, studies_id):
        sql= "SELECT studies_name from studies WHERE studies_name=%s AND studies_id != %s"
        data = (studies_name, studies_id)
        cursor.execute(sql,(data))
        rows = cursor.fetchall()
        return rows

    def updateStudy(cursor, studies_name, studies_comment, studies_se, studies_id):
        cursor.execute(
            "UPDATE studies SET studies_name= %s, studies_comment = %s, studies_se = %s WHERE studies_id = %s",
            (studies_name, studies_comment, studies_se, studies_id)
        )


    def insertStudy(cursor, studies_name, studies_comment, studies_date, studies_se):
        cursor.execute("INSERT INTO studies (studies_name, studies_comment, studies_date, studies_se) VALUES(%s,%s,%s,%s);", (studies_name, studies_comment, studies_date, studies_se))

    def deleteStudy(cursor, studies_id):
        #delete from studies
        sql= "DELETE from studies WHERE studies_id=%s"
        data = (studies_id)
        cursor.execute(sql,(data,))
        #delete from queries
        #delete from scrapers
        #delete from results
        #delete from sources
        #delete from serps
        #delete from evaluations
        #delete from classifications
