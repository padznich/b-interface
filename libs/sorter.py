# -*- coding: utf-8 -*-


def order(_query, _model, _col_name="id", _order="asc"):

    query = _query.order_by(
        eval("_model.{}.{}()".format(_col_name, _order))
    )

    return query
