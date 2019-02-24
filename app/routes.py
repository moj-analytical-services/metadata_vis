from flask import render_template, jsonify
from app import app
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
        return jsonify(data={'message': 'Search terms: {}'.format(form.searchterms.data)})
    return jsonify(data=form.errors)