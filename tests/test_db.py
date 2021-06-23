# sys libs
import os
import os, sys
import os.path
sys.path.insert(0, '..')

from db.connect import DB
from libs.scrapers import Scrapers
from libs.queries import Queries
from libs.results import Results
from libs.studies import Studies
from libs.evaluations import Evaluations
from libs.helpers import Helpers
from libs.sources import Sources


studies = Studies.getStudies()

for s in studies:
    print(s[0])


db = DB()
db.cursor.execute("select scrapers_id from scrapers, results  where scrapers_queries_id = results_queries_id and scrapers_studies_id = 60 group by scrapers_id")
rows = db.cursor.fetchall()
db.DBDisconnect()

db = DB()

for r in rows:
    id = str(r[0])
    sql = "update scrapers set scrapers_progress = 1 where scrapers_id = "+id
    db.cursor.execute(sql)


db.DBDisconnect()
