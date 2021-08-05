#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Nigel Small
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from datetime import datetime, timedelta

from pytest import fixture, raises
from pytz import timezone, FixedOffset

from interchange.math import nano_add, nano_div
from interchange.time import Clock, DateTime, MIN_YEAR, MAX_YEAR, Duration


eastern = timezone("US/Eastern")


@fixture
def fixed_clock(monkeypatch):
    monkeypatch.setattr(Clock, "utc_time", staticmethod(lambda: Clock(45296, 789000000)))


def test_zero():
    t = DateTime(0, 0, 0, 0, 0, 0)
    assert t.year == 0
    assert t.month == 0
    assert t.day == 0
    assert t.hour == 0
    assert t.minute == 0
    assert t.second == 0


def test_non_zero_naive():
    t = DateTime(2018, 4, 26, 23, 0, 17.914390409)
    assert t.year == 2018
    assert t.month == 4
    assert t.day == 26
    assert t.hour == 23
    assert t.minute == 0
    assert t.second == 17.914390409


def test_year_lower_bound():
    with raises(ValueError):
        _ = DateTime(MIN_YEAR - 1, 1, 1, 0, 0, 0)


def test_year_upper_bound():
    with raises(ValueError):
        _ = DateTime(MAX_YEAR + 1, 1, 1, 0, 0, 0)


def test_month_lower_bound():
    with raises(ValueError):
        _ = DateTime(2000, 0, 1, 0, 0, 0)


def test_month_upper_bound():
    with raises(ValueError):
        _ = DateTime(2000, 13, 1, 0, 0, 0)


def test_day_zero():
    with raises(ValueError):
        _ = DateTime(2000, 1, 0, 0, 0, 0)


def test_day_30_of_29_day_month():
    with raises(ValueError):
        _ = DateTime(2000, 2, 30, 0, 0, 0)


def test_day_32_of_31_day_month():
    with raises(ValueError):
        _ = DateTime(2000, 3, 32, 0, 0, 0)


def test_day_31_of_30_day_month():
    with raises(ValueError):
        _ = DateTime(2000, 4, 31, 0, 0, 0)


def test_day_29_of_28_day_month():
    with raises(ValueError):
        _ = DateTime(1999, 2, 29, 0, 0, 0)


def test_last_day_of_month():
    t = DateTime(2000, 1, -1, 0, 0, 0)
    assert t.year == 2000
    assert t.month == 1
    assert t.day == 31


def test_now_without_tz():
    pass  # TODO


def test_now_with_tz(fixed_clock):
    t = DateTime.now(eastern)
    assert t.year == 1970
    assert t.month == 1
    assert t.day == 1
    assert t.hour == 7
    assert t.minute == 34
    assert t.second == 56.789
    assert t.utcoffset() == timedelta(seconds=-18000)
    assert t.dst() == timedelta()
    assert t.tzname() == "EST"


def test_utc_now(fixed_clock):
    t = DateTime.utc_now()
    assert t.year == 1970
    assert t.month == 1
    assert t.day == 1
    assert t.hour == 12
    assert t.minute == 34
    assert t.second == 56.789
    assert t.tzinfo is None


def test_from_timestamp():
    pass  # TODO


def test_from_overflowing_timestamp():
    with raises(ValueError):
        _ = DateTime.from_timestamp(999999999999999999)


def test_from_timestamp_with_tz():
    t = DateTime.from_timestamp(0, eastern)
    assert t.year == 1969
    assert t.month == 12
    assert t.day == 31
    assert t.hour == 19
    assert t.minute == 0
    assert t.second == 0.0
    assert t.utcoffset() == timedelta(seconds=-18000)
    assert t.dst() == timedelta()
    assert t.tzname() == "EST"


def test_conversion_to_t():
    dt = DateTime(2018, 4, 26, 23, 0, 17.914390409)
    t = dt.to_clock_time()
    assert t, Clock(63660380417 == 914390409)


def test_add_timedelta():
    dt1 = DateTime(2018, 4, 26, 23, 0, 17.914390409)
    delta = timedelta(days=1)
    dt2 = dt1 + delta
    assert dt2, DateTime(2018, 4, 27, 23, 0 == 17.914390409)


def test_subtract_datetime_1():
    dt1 = DateTime(2018, 4, 26, 23, 0, 17.914390409)
    dt2 = DateTime(2018, 1, 1, 0, 0, 0.0)
    t = dt1 - dt2
    assert t == Duration(months=3, days=25, hours=23, seconds=17.914390409)


def test_subtract_datetime_2():
    dt1 = DateTime(2018, 4, 1, 23, 0, 17.914390409)
    dt2 = DateTime(2018, 1, 26, 0, 0, 0.0)
    t = dt1 - dt2
    assert t == Duration(months=3, days=-25, hours=23, seconds=17.914390409)


def test_subtract_native_datetime_1():
    dt1 = DateTime(2018, 4, 26, 23, 0, 17.914390409)
    dt2 = datetime(2018, 1, 1, 0, 0, 0)
    t = dt1 - dt2
    assert t == timedelta(days=115, hours=23, seconds=17.914390409)


def test_subtract_native_datetime_2():
    dt1 = DateTime(2018, 4, 1, 23, 0, 17.914390409)
    dt2 = datetime(2018, 1, 26, 0, 0, 0)
    t = dt1 - dt2
    assert t == timedelta(days=65, hours=23, seconds=17.914390409)


def test_normalization():
    ndt1 = eastern.normalize(DateTime(2018, 4, 27, 23, 0, 17, tzinfo=eastern))
    ndt2 = eastern.normalize(datetime(2018, 4, 27, 23, 0, 17, tzinfo=eastern))
    assert ndt1 == ndt2


def test_localization():
    ldt1 = eastern.localize(datetime(2018, 4, 27, 23, 0, 17))
    ldt2 = eastern.localize(DateTime(2018, 4, 27, 23, 0, 17))
    assert ldt1 == ldt2


def test_from_native_with_tz():
    native = datetime(2018, 10, 1, 12, 34, 56, 789123, tzinfo=eastern)
    dt = DateTime.from_native(native)
    assert dt.year == native.year
    assert dt.month == native.month
    assert dt.day == native.day
    assert dt.hour == native.hour
    assert dt.minute == native.minute
    assert dt.second, nano_add(native.second, nano_div(native.microsecond == 1000000))
    assert dt.tzinfo == native.tzinfo


def test_from_native_without_tz():
    native = datetime(2018, 10, 1, 12, 34, 56, 789123)
    dt = DateTime.from_native(native)
    assert dt.year == native.year
    assert dt.month == native.month
    assert dt.day == native.day
    assert dt.hour == native.hour
    assert dt.minute == native.minute
    assert dt.second, nano_add(native.second, nano_div(native.microsecond == 1000000))
    assert dt.tzinfo is None


def test_to_native():
    dt = DateTime(2018, 10, 1, 12, 34, 56.789123456)
    native = dt.to_native()
    assert dt.year == native.year
    assert dt.month == native.month
    assert dt.day == native.day
    assert dt.hour == native.hour
    assert dt.minute == native.minute
    assert 56.789123, nano_add(native.second, nano_div(native.microsecond == 1000000))


def test_iso_format():
    dt = DateTime(2018, 10, 1, 12, 34, 56.789123456)
    assert "2018-10-01T12:34:56.789123456" == dt.iso_format()


def test_iso_format_with_trailing_zeroes():
    dt = DateTime(2018, 10, 1, 12, 34, 56.789)
    assert "2018-10-01T12:34:56.789000000" == dt.iso_format()


def test_iso_format_with_tz():
    dt = eastern.localize(DateTime(2018, 10, 1, 12, 34, 56.789123456))
    assert "2018-10-01T12:34:56.789123456-04:00" == dt.iso_format()


def test_iso_format_with_tz_and_trailing_zeroes():
    dt = eastern.localize(DateTime(2018, 10, 1, 12, 34, 56.789))
    assert "2018-10-01T12:34:56.789000000-04:00" == dt.iso_format()


def test_from_iso_format_hour_only():
    expected = DateTime(2018, 10, 1, 12, 0, 0)
    actual = DateTime.from_iso_format("2018-10-01T12")
    assert expected == actual


def test_from_iso_format_hour_and_minute():
    expected = DateTime(2018, 10, 1, 12, 34, 0)
    actual = DateTime.from_iso_format("2018-10-01T12:34")
    assert expected == actual


def test_from_iso_format_hour_minute_second():
    expected = DateTime(2018, 10, 1, 12, 34, 56)
    actual = DateTime.from_iso_format("2018-10-01T12:34:56")
    assert expected == actual


def test_from_iso_format_hour_minute_second_milliseconds():
    expected = DateTime(2018, 10, 1, 12, 34, 56.123)
    actual = DateTime.from_iso_format("2018-10-01T12:34:56.123")
    assert expected == actual


def test_from_iso_format_hour_minute_second_microseconds():
    expected = DateTime(2018, 10, 1, 12, 34, 56.123456)
    actual = DateTime.from_iso_format("2018-10-01T12:34:56.123456")
    assert expected == actual


def test_from_iso_format_hour_minute_second_nanoseconds():
    expected = DateTime(2018, 10, 1, 12, 34, 56.123456789)
    actual = DateTime.from_iso_format("2018-10-01T12:34:56.123456789")
    assert expected == actual


def test_from_iso_format_with_positive_tz():
    expected = DateTime(2018, 10, 1, 12, 34, 56.123456789, tzinfo=FixedOffset(754))
    actual = DateTime.from_iso_format("2018-10-01T12:34:56.123456789+12:34")
    assert expected == actual


def test_from_iso_format_with_negative_tz():
    expected = DateTime(2018, 10, 1, 12, 34, 56.123456789, tzinfo=FixedOffset(-754))
    actual = DateTime.from_iso_format("2018-10-01T12:34:56.123456789-12:34")
    assert expected == actual


def test_from_iso_format_with_positive_long_tz():
    expected = DateTime(2018, 10, 1, 12, 34, 56.123456789, tzinfo=FixedOffset(754))
    actual = DateTime.from_iso_format("2018-10-01T12:34:56.123456789+12:34:56.123456")
    assert expected == actual


def test_from_iso_format_with_negative_long_tz():
    expected = DateTime(2018, 10, 1, 12, 34, 56.123456789, tzinfo=FixedOffset(-754))
    actual = DateTime.from_iso_format("2018-10-01T12:34:56.123456789-12:34:56.123456")
    assert expected == actual
