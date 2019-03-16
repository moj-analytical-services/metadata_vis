from flask import render_template, jsonify, request
from main import app, db


from models import Database, Table, Column, AccessRight


@app.route('/')
@app.route('/index')
def index():

    return  render_template('index.html', title='Home')


@app.route('/search/', methods=['get'])
def search():

    conn = db.session.connection
    session = db.session

    searchterms = request.args.get('searchterms')

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

@app.route('/sample_code/', methods=['get'])
def get_sample_code():
    clm_id = request.args.get('clm_id')
    column = Column.query.get(clm_id)
    # table = column.table
    # database = table.database
    return render_template("sample_code.html", column = column)

@app.route('/ar_info/', methods=['get'])
def get_accessrights_info():
    db_id = request.args.get('db_id')
    accessrights = AccessRight.query.filter(AccessRight.db_id == db_id).all()
    print(len(accessrights))
    return render_template("ar_info.html", accessrights=accessrights)
