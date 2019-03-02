from flask import render_template, jsonify, request
from app import app, db
from app.forms import SearchForm

from app.models import Database, Table, Column


@app.route('/')
@app.route('/index')
def index():
    form = SearchForm()
    return  render_template('index.html', title='Home', form=form)


@app.route('/search/', methods=['get'])
def search():


    print("hello")
    conn = db.session.connection
    session = db.session

    searchterms = request.args.get('searchterms')
    print(searchterms)

    sql = """
    SELECT *
    FROM fulltextsearch
    WHERE fulltextsearch MATCH ?
    ORDER BY bm25(fulltextsearch, 0,0,0,1,2,1,2,1,2);
    """

    result = db.engine.execute(sql, (searchterms,))
    column_names = [r[0] for r in result.cursor.description]

    table = []
    for row in result.fetchall():
        dictrow = dict(zip(column_names, row))
        table.append(dictrow)

    return jsonify(data=table)


@app.route('/db_info/', methods=['get'])
def get_db_info():
    id = request.args.get('id')
    database = Database.query.get(id)
    return render_template("db_info.html", database = database)

@app.route('/tbl_info/', methods=['get'])
def get_tbl_info():
    id = request.args.get('id')
    table = Table.query.get(id)
    return render_template("tbl_info.html", table = table)

@app.route('/clm_info/', methods=['get'])
def get_clm_info():
    id = request.args.get('id')
    column = Column.query.get(id)
    return render_template("clm_info.html", column = column)