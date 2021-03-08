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

    def addStudy():
        print("addStudycursor")

    def editStudy():
        print("editStudycursor")

    def delStudy():
        print("delStudycursor")
