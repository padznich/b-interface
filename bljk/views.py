# -*- coding: utf-8 -*-

from datetime import datetime

from flask import render_template, redirect, request

from bljk.app import app
from bljk.forms import FormSummary
from libs.paginator import paginate
from libs.sorter import order
from bljk.models import Summary, Detail, Description


_order = "asc"


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/summary', methods=['GET', ])
@app.route('/summary/', methods=['GET', ])
@app.route('/summary/identifier/<string:identifier>/')
@app.route('/summary/identifier/<string:identifier>'
           '/from/<string:_from>/to/<string:_to>/')
@app.route('/summary/from/<string:_from>/to/<string:_to>/')
def summary(page=1, identifier=None, _from=None, _to=None):

    query = Summary.query
    query = order(query, Summary)

    form = FormSummary()

    if request.args.get('page', None):
        page = request.args.get('page')

    if identifier:
        query = query.filter_by(
            identifier=identifier
        )

    if _from or _to:
        _from = _from or "2000-01-01"
        _to = _to or datetime.now().strftime("%Y-%m-%d")
        query = query.filter(
            Summary.date.between(
                _from,
                _to
            )
        )

    _identifier = request.values.get('identifier', None)
    _from = request.values.get('date_from', None)
    _to = request.values.get('date_to', None)

    if _identifier and (_from or _to):
        _from = _from or "2000-01-01"
        _to = _to or datetime.now().strftime("%Y-%m-%d")
        return redirect(
            "/summary/identifier/{}/from/{}/to/{}/".format(
                _identifier, _from, _to
            )
        )

    if _identifier:
        return redirect(
            "/summary/identifier/{}/".format(
                _identifier
            ),
        )

    if _from or _to:
        _from = _from or "2000-01-01"
        _to = _to or datetime.now().strftime("%Y-%m-%d")
        return redirect(
            "/summary/from/{}/to/{}/".format(
                _from, _to
            )
        )

    # Columns Sorting
    if request.method == "GET":
        print '-' * 90
        print request
        if request.values.get('id', None):
            if _order == "asc":
                print 11
                global _order
                _order = "desc"
            else:
                print 12
                global _order
                _order = "asc"
            query = query.order_by(Summary.id.asc())

    context = paginate(page, query)

    return render_template('summary.html',
                           urlic='summary',
                           forms=form,
                           **context)


@app.route('/detail')
@app.route('/detail/<int:summ_id>')
def detail(page=1, summ_id=None):

    query = Detail.query

    if summ_id:
        query = query.filter_by(
            summary_id=summ_id
        )

    if request.args.get('page', None):
        page = request.args.get('page')

    if request.args.get("_id", None):
        summary_id = request.args.get("_id")
        query = query.filter_by(
            summary_id=summary_id
        )

    context = paginate(page, query)

    return render_template('detail.html', urlic='detail', **context)


@app.route('/description')
@app.route('/description/')
def description(page=1):

    query = Description.query

    if request.args.get('page', None):
        page = request.args.get('page')

    context = paginate(page, query)

    return render_template('detail_desc.html', urlic='detail_desc', **context)
