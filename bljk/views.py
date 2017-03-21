# -*- coding: utf-8 -*-

from datetime import datetime

from flask import render_template, request, jsonify
from sqlalchemy_utils import sort_query
from sqlalchemy import func

from bljk.app import app
from bljk.forms import FormSummary, FormDetail
from libs.paginator import paginate
from bljk.models import Summary, Detail, Description, Strategy, db


@app.route('/')
def home():
    return render_template('home.html')


@app.route("/summary", methods=["GET", "POST"])
@app.route("/summary/", methods=["GET", "POST"])
@app.route("/summary/<int:_id>")
@app.route("/summary/<int:_id>/")
def summary(_id=None):

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

    col = request.args.get("col")
    _order = request.args.get("_order")
    identifier = request.args.get("identifier")
    _from = request.args.get("date_from")
    _to = request.args.get("date_to")
    page = request.args.get("page") or 1

    _order = _order or "asc"

    form = FormSummary(request.form)

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

    if _id:
        query = query.filter_by(id=_id)

    if _from or _to:
        _from = _from or "2000-01-01"
        _to = _to or datetime.now().strftime("%Y-%m-%d")
        query = query.filter(
            Summary.date.between(
                _from,
                _to
            )
        ).order_by(Summary.date.desc())

    context = paginate(page, query)

    return render_template("summary.html",
                           forms=form,
                           **context)


@app.route("/detail", methods=["GET", "POST"])
@app.route("/detail/", methods=["GET", "POST"])
@app.route("/detail/<int:_id>")
@app.route("/detail/<int:_id>/")
def detail(_id=None):

    query = Detail.query
    query = sort_query(query, "id")

    confirmed = request.values.get("confirmed")
    identifier = request.values.get("identifier")
    summ_id = request.args.get("summ_id")
    page = request.args.get("page") or 1

    if _id:
        query = query.filter_by(id=_id)

    if summ_id:
        query = query.filter_by(summary_id=summ_id)

    if identifier:
        query = query.filter_by(identifier=identifier)

    if confirmed:
        if confirmed in ["True", "true", "t", "1"]:
            query = query.filter_by(confirmed=True)
        else:
            query = query.filter_by(confirmed=False)

    form = FormDetail(request.form)
    ident_list = set(
        [
            (row.identifier, row.identifier)
            for row in
            Detail.query.distinct(Detail.identifier).all()
        ]
    )

    form.identifier.choices = ident_list
    context = paginate(page, query)

    return render_template("detail.html",
                           form=form,
                           **context)


@app.route("/description", methods=["GET", "POST"])
@app.route("/description/", methods=["GET", "POST"])
@app.route("/description/<int:detail_id>/")
def description(page=1, detail_id=None):

    query = Description.query
    query = sort_query(query, "id")

    if detail_id:
        query = query.filter_by(detail_id=detail_id)

    if request.args.get("page"):
        page = request.args.get("page")

    context = paginate(page, query)
    urlic = request.base_url

    return render_template("description.html",
                           urlic=urlic,
                           **context)


@app.route("/strategy")
@app.route("/strategy/")
def strategy():

    query = db.session.query(
        Strategy.id,
        Strategy.dealer,
        Strategy.cards,
        Strategy.action,
    )
    page = request.args.get("page") or 1
    context = paginate(page, query)

    return render_template("strategy.html",
                           **context)


@app.route('/ajax/', methods=["GET", "POST"])
def ajax(detail_id=None, state=None):

    if request.method == "POST":
        detail_id = request.json.get("detail_id")
        state = request.json.get("state")

        _d = Detail.query.get(detail_id)
        _d.confirmed = state
        db.session.add(_d)
        db.session.commit()

    return jsonify(detail_id=detail_id, state=state)
