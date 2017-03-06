# -*- coding: utf-8 -*-

from math import ceil


def paginate(_page, _query, _rec_number=20):

    page = int(_page)
    prev_page = page - 1
    next_page = page + 1

    records_count = _query.count()
    pages_count = int(ceil(float(records_count) / _rec_number))

    page_records = _query.all()[_rec_number * prev_page: _rec_number * page]

    context = {
        "page_records": page_records,
        "pages_count": pages_count,
        "page": page,
        "prev_page": prev_page,
        "next_page": next_page,
    }

    return context
