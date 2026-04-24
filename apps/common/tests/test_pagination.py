"""Tests for the hub pagination class."""

import json

from django.test import RequestFactory
from rest_framework.request import Request

from apps.common.pagination import HubLimitPagination
from apps.common.renderers import HubJSONRenderer


def _req(path: str) -> Request:
    return Request(RequestFactory().get(path))


def test_limit_default_when_unset() -> None:
    assert HubLimitPagination().get_limit(_req("/")) == 50


def test_limit_default_when_invalid() -> None:
    assert HubLimitPagination().get_limit(_req("/?limit=abc")) == 50


def test_limit_clamps_below_1_to_1() -> None:
    assert HubLimitPagination().get_limit(_req("/?limit=0")) == 1
    assert HubLimitPagination().get_limit(_req("/?limit=-5")) == 1


def test_limit_clamps_above_max_to_500() -> None:
    assert HubLimitPagination().get_limit(_req("/?limit=99999")) == 500


def test_limit_passes_through_valid_value() -> None:
    assert HubLimitPagination().get_limit(_req("/?limit=42")) == 42


def test_paginated_response_shape_items_only() -> None:
    pager = HubLimitPagination()
    data = [{"id": i} for i in range(10)]
    page = pager.paginate_queryset(data, _req("/?limit=3"))
    assert page is not None
    response = pager.get_paginated_response(page)
    assert response.data == {"items": [{"id": 0}, {"id": 1}, {"id": 2}]}
    assert "count" not in response.data
    assert "next" not in response.data
    assert "previous" not in response.data


def test_end_to_end_envelope_wraps_paginated_response() -> None:
    """Pagination + envelope renderer together must produce:
    {"ok": true, "data": {"items": [...]}}
    """
    pager = HubLimitPagination()
    data = [{"id": i} for i in range(10)]
    page = pager.paginate_queryset(data, _req("/?limit=2"))
    assert page is not None
    response = pager.get_paginated_response(page)

    rendered = HubJSONRenderer().render(response.data)
    assert json.loads(rendered) == {
        "ok": True,
        "data": {"items": [{"id": 0}, {"id": 1}]},
    }
