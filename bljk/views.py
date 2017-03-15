# -*- coding: utf-8 -*-

from datetime import datetime

from flask import render_template, redirect, request
from sqlalchemy_utils import sort_query
from sqlalchemy import func

from bljk.app import app
from bljk.forms import FormSummary, FormDetail
from libs.paginator import paginate
from bljk.models import Summary, Detail, Description, db


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

    query = db.session.query(
            Summary.id,
            Summary.date,
            Summary.game,
            Summary.min,
            Summary.plays,
            Summary.wagered,
            Summary.winnings,
            Summary.pending,
            Summary.identifier,
            (Summary.wagered / func.nullif(Summary.plays, 0)).label("rate")
        )

    page = request.args.get("page") or 1

    _order = _order or "asc"

    if col and _order == "desc":
        query = sort_query(query, "-" + col)
    elif col and _order == "asc":
        query = sort_query(query, col)
    else:
        col = col or "id"
        query = sort_query(query, col)

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
@app.route('/detail/summary/<int:summ_id>/')
@app.route('/detail/identifier/<string:identifier>/')
def detail(page=1, summ_id=None, identifier=None):

    query = Detail.query
    query = sort_query(query, 'id')

    if summ_id:
        query = query.filter_by(summary_id=summ_id)
    if identifier:
        query = query.filter_by(identifier=identifier)

    if request.args.get('page'):
        page = request.args.get('page')

    if request.args.get("_id"):
        summary_id = request.args.get("_id")
        print summary_id
        query = query.filter_by(
            summary_id=summary_id
        )

    form = FormDetail()
    ident_list = set(
        [
            (row.identifier, row.identifier)
            for row in
            Detail.query.distinct(Detail.identifier).all()
        ]
    )

    form.identifier.choices = ident_list

    _identifier = request.values.get("identifier")
    if _identifier:
        return redirect("/detail/identifier/{}/".format(_identifier))

    context = paginate(page, query)
    urlic = request.base_url

    return render_template('detail.html',
                           urlic=urlic,
                           form=form,
                           **context)


@app.route('/description')
@app.route('/description/<int:detail_id>/')
def description(page=1, detail_id=None):

    query = Description.query
    query = sort_query(query, 'id')

    if detail_id:
        query = query.filter_by(detail_id=detail_id)

    if request.args.get('page'):
        page = request.args.get('page')

    context = paginate(page, query)
    urlic = request.base_url

    return render_template('description.html', urlic=urlic, **context)
