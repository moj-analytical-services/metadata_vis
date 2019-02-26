from flask import render_template, jsonify
from app import app, db
from app.forms import SearchForm

@app.route('/')
@app.route('/index')
def index():
    form = SearchForm()
    return  render_template('index.html', title='Home', form=form)

@app.route('/search/', methods=['post'])
def search():
    form = SearchForm()
    if form.validate_on_submit():

        conn = db.session.connection
        session = db.session

        sql = """
            select * from databases as db
            left join tables as tbl
            on db.db_id= tbl.db_id
            left join columns as cl
            on tbl.tbl_id = cl.tbl_id
        """

        result = db.engine.execute(sql)
        column_names = [r[0] for r in result.cursor.description]

        table = []
        for row in result.fetchall():
            dictrow = dict(zip(column_names, row))
            table.append(dictrow)

        return jsonify(data=table)

    return jsonify(data=form.errors)