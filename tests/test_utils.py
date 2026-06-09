import asyncio
from datetime import datetime, timedelta

import pytest

from custom_components.webuntis.utils import utils


def test_is_different_same():
    a = [{"x": 1}, {"y": 2}]
    b = [{"y": 2}, {"x": 1}]
    assert not utils.is_different(a, b)


def test_is_different_diff_length():
    assert utils.is_different([{"a": 1}], [])


def test_compact_list_dict():
    t0 = datetime(2020, 1, 1, 8, 0)
    t1 = datetime(2020, 1, 1, 8, 30)
    t2 = datetime(2020, 1, 1, 9, 0)

    items = [
        {"start": t0, "end": t1, "lsnumber": 1, "code": "A"},
        {"start": t1, "end": t2, "lsnumber": 1, "code": "A"},
    ]

    res = utils.compact_list(items, list_type="dict", compact_tolerance=timedelta(minutes=0))
    assert len(res) == 1
    assert res[0]["start"] == t0 and res[0]["end"] == t2


@pytest.mark.asyncio
async def test_async_notify_success(monkeypatch):
    class DummyServices:
        async def async_call(self, domain, service, service_data=None, target=None, blocking=False):
            return None

    class DummyHass:
        def __init__(self):
            self.services = DummyServices()

    hass = DummyHass()

    ok = await utils.async_notify(hass, "notify.send_message", {"data": {"message": "hi"}})
    assert ok


@pytest.mark.asyncio
async def test_async_notify_invalid_service(monkeypatch):
    class DummyServices:
        async def async_call(self, domain, service, service_data=None, target=None, blocking=False):
            raise RuntimeError("boom")

    class DummyHass:
        def __init__(self):
            self.services = DummyServices()

    hass = DummyHass()

    ok = await utils.async_notify(hass, "badservice", {})
    assert not ok
