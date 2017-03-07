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


@app.route('/summary', methods=['GET', 'POST'])
@app.route('/summary/', methods=['GET', 'POST'])
@app.route('/summary/'
           'identifier/<string:identifier>/')
@app.route('/summary/'
           'identifier/<string:identifier>/'
           'from/<string:_from>/'
           'to/<string:_to>/')
@app.route('/summary/'
           'from/<string:_from>/'
           'to/<string:_to>/')
@app.route('/summary/'
           'col/<string:col>/<string:_order>/')
@app.route('/summary/'
           'identifier/<string:identifier>/'
           'col/<string:col>/<string:_order>/')
@app.route('/summary/'
           'identifier/<string:identifier>/'
           'from/<string:_from>/'
           'to/<string:_to>/'
           'col/<string:col>/<string:_order>/')
@app.route('/summary/'
           'from/<string:_from>/'
           'to/<string:_to>/'
           'col/<string:col>/<string:_order>/')
def summary(col=None, _order=None, identifier=None, _from=None, _to=None):

    query = Summary.query

    page = request.args.get("page", None) or 1

    _order = _order or "asc"

    if col == unicode("wagered_plays") and _order == "desc":
        query = query.order_by(Summary.wagered.asc(),
                               Summary.plays.desc())
    elif col == unicode("wagered_plays") and _order == "asc":
        query = query.order_by(Summary.wagered.desc(),
                               Summary.plays.asc())
    else:
        col = col or "id"
        query = order(query, Summary, col, _order)

    if identifier:
        query = query.filter_by(
            identifier=identifier
        ).order_by(Summary.identifier.desc())

    if _from or _to:
        _from = _from or "2000-01-01"
        _to = _to or datetime.now().strftime("%Y-%m-%d")
        query = query.filter(
            Summary.date.between(
                _from,
                _to
            )
        ).order_by(Summary.date.desc())

    form = FormSummary()

    _identifier = request.values.get('identifier')
    _from = request.values.get('date_from')
    _to = request.values.get('date_to')

    if _identifier and (_from or _to):
        _from = _from or "2000-01-01"
        _to = _to or datetime.now().strftime("%Y-%m-%d")
        return redirect(
            "/summary/identifier/{}/from/{}/to/{}/".format(
                _identifier, _from, _to)
        )

    if _identifier:
        return redirect("/summary/identifier/{}/".format(_identifier))

    if _from or _to:
        _from = _from or "2000-01-01"
        _to = _to or datetime.now().strftime("%Y-%m-%d")
        return redirect("/summary/from/{}/to/{}/".format(
            _from, _to
        ))

    context = paginate(page, query)

    urlic = request.base_url
    if "col" in urlic.split("/"):
        urlic = "/".join(urlic.split("/")[:-4]) + "/"

    return render_template("summary.html",
                           urlic=urlic,
                           forms=form,
                           **context)


@app.route('/detail')
@app.route('/detail/<int:summ_id>/')
def detail(page=1, summ_id=None):

    query = Detail.query
    query = order(query, Detail, "id", "asc")

    if summ_id:
        query = query.filter_by(summary_id=summ_id)

    if request.args.get('page', None):
        page = request.args.get('page')

    if request.args.get("_id", None):
        summary_id = request.args.get("_id")
        print summary_id
        query = query.filter_by(
            summary_id=summary_id
        )

    context = paginate(page, query)
    urlic = request.base_url

    return render_template('detail.html', urlic=urlic, **context)


@app.route('/description')
@app.route('/description/<int:detail_id>/')
def description(page=1, detail_id=None):

    query = Description.query
    query = order(query, Description, "id", "asc")

    if detail_id:
        query = query.filter_by(detail_id=detail_id)

    if request.args.get('page', None):
        page = request.args.get('page')

    context = paginate(page, query)
    urlic = request.base_url

    return render_template('description.html', urlic=urlic, **context)
