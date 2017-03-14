# -*- coding: utf-8 -*-

from math import ceil


def paginate(_page, _query, per_page=20):
    page = int(_page)
    record_query = _query.paginate(page, per_page, False)

    pages_count = int(ceil(record_query.total / float(per_page)))

    record_items = record_query.items

    context = {
        "page_records": record_items,
        "pages_count": pages_count,
        "page": page,
        "prev_page": page - 1,
        "next_page": page + 1,
    }

    return context