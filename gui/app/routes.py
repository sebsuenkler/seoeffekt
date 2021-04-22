'''
Sehr einfache Gui:

Index-Seite: Studie auswählen oder neue Studie anlegen x

Wenn ausgewählt, Formular mit Daten zu der Studie (editierbar) x

Wenn neue Studie, Formular mit Eingaben für neue Studie x

Auswahl von Suchmaschinen nach verfügbaren Scrapern x

Menü für das Anlegen von Suchanfragen x

Menü für das Einfügen von URLs (import) x

Übersicht zu bisherigen Ergebnissen mit einfachen Statistiken -> Export der Ergebnisse als CSV Datei mit Generierung eines Downloadlinks per Mail,da viele Daten!

Wichtig! Skript zur Prüfung von Karteileichen, wenn Studie gelöscht wird, werden die Daten auch gelöscht
'''

from flask import Flask
from flask import render_template, flash, redirect, request, url_for, session
from flask import send_file, send_from_directory, safe_join, abort
from app import app

from app.forms import Form



from app.forms import StudyForm
from app.forms import insertStudyForm
from app.forms import editStudyForm


# sys libs
import os
import os, sys
import os.path
import json
sys.path.insert(0, '..')

#date libs
from datetime import date
from datetime import datetime
from datetime import timedelta
import datetime
import time

today = date.today()

#db libs
from db.connect import DB
from libs.scrapers import Scrapers
from libs.queries import Queries
from libs.results import Results
from libs.studies import Studies
from libs.evaluations import Evaluations
from libs.helpers import Helpers
from libs.sources import Sources

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['WTF_CSRF_SECRET_KEY'] = SECRET_KEY
app.config['WTF_CSRF_ENABLED'] = False


se_forms = ""

with open('../config/scraper.ini', 'r') as f:
    array = json.load(f)

    scrapers_json = array['scraper']

    scrapers = []

    for scraper in scrapers_json:
        config = scrapers_json[scraper]
        se_forms = se_forms+config['search_engine']+"\r\n"

se_forms = se_forms.split()
se_forms = [(x, x) for x in se_forms]

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    form = Form()

    studies_form = []
    studies = Studies.getStudies()
    for s in studies:
        studies_form.append(s[0])

    studies_form = tuple(studies_form)

    form.study_list.choices=studies_form

    if form.is_submitted():
        study = form.study_list.data
        study_name = form.study_name.data
        session['study'] = study
        session['study_name'] = study_name
        if study_name:
            return redirect(url_for('insertstudy'))
        else:
            return redirect(url_for('study'))

    return render_template('index.html', title='Index', form=form)



@app.route('/study', methods=['GET', 'POST'])
def study():
    study = session.get('study', None)
    studies_data = Studies.getStudybyName(study)
    study_form = StudyForm()
    study_name = studies_data[0][0]
    study_form.study_name.data = study_name
    study_description = studies_data[0][1]
    study_form.study_description.data = study_description
    study_se = studies_data[0][3]
    study_se = study_se.replace(";", ", ")
    study_form.study_se.data = study_se

    study_id = studies_data[0][4]

    '''
    generate Statistics

    Auswertungsfortschritt

    Anzahl der Suchanfragen
    Anzahl der gescrapten Ergebnisse
    Anzahl der analysierten Ergebnisse

    Auswertung der Klassifikation (Mehrere Klassifikatoren)

    Mit einfachen Grafiken / Dashboard

    Aufteiling nach Suchmaschinen...
    '''

    count_queries = Queries.countQueriesStudy(study_id)
    count_queries = count_queries[0][0]

    count_results = Results.countResultsbyStudy(study_id)
    count_results = count_results[0][0]

    count_classified = Results.countClassifiedResultsbyStudy(study_id)
    count_classified = count_classified[0][0]

    count_failed = Results.countFailedResultsbyStudy(study_id)
    count_failed = count_failed[0][0]

    processed_results = count_classified + count_failed

    progress=0

    if count_results > 0:
        progress = processed_results / count_results * 100
        progress = round(progress, 1)


    search_engines = []
    study_se = study_se.split(',')

    for s in study_se:
        search_engines.append(s)

    results = {}

    for se in search_engines:
        se = se.strip()
        res = Results.countResultsbyStudySE(study_id, se)
        res = res[0][0]

        cl = Results.countClassifiedResultsbyStudySE(study_id, se)
        cl = cl[0][0]

        d = {se: {'results': res, 'class': cl}}


        results.update(d)



    #results = {'Bing': {'results': '100', 'class':'5'}}


    queries_study = Queries.getQueriesStudy(study_id)
    queries = ""
    for q in queries_study:
        query = q[1]
        queries = queries+query+"\n"

    if study_form.is_submitted():
        return redirect(url_for('editstudy'))

    return render_template('study.html', title='Study overview', form=study_form, queries=queries, count_queries=count_queries, count_results=count_results, count_classified=count_classified, count_failed=count_failed, progress=progress, search_engines=search_engines, results=results)


@app.route('/editstudy', methods=['GET', 'POST'])
def editstudy():
    study = session.get('study', None)
    studies_data = Studies.getStudybyName(study)
    edit_form = editStudyForm()
    study_name = studies_data[0][0]

    study_description = studies_data[0][1]

    study_se = studies_data[0][3]

    study_se = study_se.split(';')

    edit_form.study_se.choices=se_forms

    study_id = studies_data[0][4]
    queries_study = Queries.getQueriesStudy(study_id)

    queries = ""
    for q in queries_study:
        query = q[1]
        queries = queries+query+"\n"

    error = 0

    if edit_form.is_submitted():
        study = session.get('study', None)
        study_delete = edit_form.study_delete.data
        studies_data = Studies.getStudybyName(study)
        study_id = studies_data[0][4]
        study_name_db = studies_data[0][0]


        if study_delete == "DELETE":
            study = session.get('study', None)
            studies_data = Studies.getStudybyName(study)
            study_id = studies_data[0][4]
            study_name_db = studies_data[0][0]
            study_se = studies_data[0][3]
            study_se = study_se.split(';')

            Studies.deleteStudy(study_id)

            queries_db = Queries.getQueriesStudy(study_id)

            for q in queries_db:

                query_id = q[-2]

                for s in study_se:
                    Results.deleteResults(query_id, s)

                Queries.deleteQuerybyId(study_id, query_id)

            return redirect(url_for('index'))
        else:

            study_name = edit_form.study_name.data
            studies_data_check = Studies.getStudybyNamenotID(study_name, study_id)

            if not studies_data_check:
                study_name = edit_form.study_name.data
                study_description = edit_form.study_description.data
                study_se = edit_form.study_se.data
                se = ""

                if study_se:
                    for s in study_se:
                        se = se+s+";"
                    se = se[:-1]

                Studies.updateStudy(study_name, study_description, se, study_id)
                session['study'] = study_name

                study_queries = edit_form.study_queries.data



                if study_queries:
                    queries_db = Queries.getQueriesStudy(study_id)

                    queries = ""
                    for q in queries_study:
                        query = q[1]
                        if query:
                            query = query.strip()
                            queries = queries+query+"\n"

                    queries = queries[:-1]

                    queries_db_split = queries.split("\n")

                    split_queries = study_queries.split("\n")

                    check_split_queries = []

                    for sq in split_queries:
                        if sq:
                            sq = sq.replace("\r", "")
                            sq = sq.strip()
                            check_split_queries.append(sq)


                    delete_queries = []
                    keep_queries = []
                    add_queries = []


                    for qdb in queries_db_split:
                        if qdb in check_split_queries:
                            keep_queries.append(qdb)
                        else:
                            delete_queries.append(qdb)

                    for sq in check_split_queries:
                        if not sq in queries_db_split:
                            add_queries.append(sq)

                    if add_queries:
                        for aq in add_queries:
                            try:
                                if aq:
                                    if not Queries.getQuery(study_id, aq):
                                        Queries.insertQuery(study_id, aq, today)
                            except:
                                pass

                    if delete_queries:
                        study = session.get('study', None)
                        studies_data = Studies.getStudybyName(study)
                        study_id = studies_data[0][4]
                        study_name_db = studies_data[0][0]
                        study_se = studies_data[0][3]
                        study_se = study_se.split(';')

                        for dq in delete_queries:

                            try:
                                query = Queries.getQuery(study_id, dq)



                                query_id = query[0][-2]

                                for s in study_se:
                                    Results.deleteResults(query_id, s)

                                Queries.deleteQuerybyId(study_id, query_id)

                            except:
                                pass


                else:
                    study = session.get('study', None)
                    studies_data = Studies.getStudybyName(study)
                    study_id = studies_data[0][4]
                    study_name_db = studies_data[0][0]
                    study_se = studies_data[0][3]
                    study_se = study_se.split(';')

                    queries_db = Queries.getQueriesStudy(study_id)

                    for q in queries_db:



                        query_id = q[-2]

                        for s in study_se:
                            Results.deleteResults(query_id, s)

                        Queries.deleteQuerybyId(study_id, query_id)


                return redirect(url_for('study'))


    return render_template('editstudy.html', title='Edit study', form=edit_form, queries=queries, error=error, study_name = study_name, study_description=study_description, study_se=study_se)


@app.route('/insertstudy', methods=['GET', 'POST'])
def insertstudy():
    study_name = session.get('study_name', None)
    insert_form = insertStudyForm()
    insert_form.study_se.choices=se_forms
    se = ""
    error = 0
    if insert_form.is_submitted():
        study_name = insert_form.study_name.data
        studies_data = Studies.getStudybyName(study_name)
        if not studies_data:
            study_name = insert_form.study_name.data
            study_description = insert_form.study_description.data
            study_se = insert_form.study_se.data

            if study_se:
                for s in study_se:
                    se = se+s+";"
                se = se[:-1]

            Studies.insertStudy(study_name, study_description, today, se)
            session['study'] = study_name
            return redirect(url_for('study'))
        else:
            error = 1


    return render_template('insertstudy.html', title='Insert new study', study_name=study_name, form=insert_form, error = error)
