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
        SELECT * FROM fulltextsearch WHERE fulltextsearch MATCH '{}' ORDER BY bm25(fulltextsearch, 1,2,1,2,1,2);
        """.format(form.searchterms.data)


        result = db.engine.execute(sql)
        column_names = [r[0] for r in result.cursor.description]

        table = []
        for row in result.fetchall():
            dictrow = dict(zip(column_names, row))
            table.append(dictrow)

        return jsonify(data=table)

    return jsonify(data=form.errors)