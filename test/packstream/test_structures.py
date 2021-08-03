#!/usr/bin/env python
# -*- encoding: utf-8 -*-

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


from datetime import date, time, datetime, timedelta

from pytest import mark, raises
from pytz import utc, FixedOffset

from interchange.geo import CartesianPoint, WGS84Point, Point
from interchange.packstream import pack
from interchange.time import Date, Time, DateTime, Duration

from .common import pack_and_unpack


@mark.parametrize("cls", [date, Date])
def test_date(cls):
    b, unpacked = pack_and_unpack(cls(1970, 1, 1), version=(2, 0))
    assert b == b"\xB1D\x00"
    assert unpacked == Date(1970, 1, 1)


@mark.parametrize("cls", [time, Time])
def test_naive_time(cls):
    b, unpacked = pack_and_unpack(cls(0, 0, 0), version=(2, 0))
    assert b == b"\xB1t\x00"
    assert unpacked == Time(0, 0, 0)


@mark.parametrize("cls", [time, Time])
def test_aware_time(cls):
    b, unpacked = pack_and_unpack(cls(0, 0, 0, tzinfo=utc), version=(2, 0))
    assert b == b"\xB2T\x00\x00"
    assert unpacked == Time(0, 0, 0, tzinfo=utc)


@mark.parametrize("cls", [datetime, DateTime])
def test_naive_datetime(cls):
    b, unpacked = pack_and_unpack(cls(1970, 1, 1, 0, 0, 0), version=(2, 0))
    assert b == b"\xB2d\x00\x00"
    assert unpacked == DateTime(1970, 1, 1, 0, 0, 0)


@mark.parametrize("cls", [datetime, DateTime])
def test_datetime_with_named_timezone(cls):
    b, unpacked = pack_and_unpack(cls(1970, 1, 1, 0, 0, 0, tzinfo=utc), version=(2, 0))
    assert b == b"\xB3f\x00\x00\x83UTC"
    assert unpacked == DateTime(1970, 1, 1, 0, 0, 0, tzinfo=utc)


@mark.parametrize("cls", [datetime, DateTime])
def test_datetime_with_timezone_offset(cls):
    b, unpacked = pack_and_unpack(cls(1970, 1, 1, 0, 0, 0, tzinfo=FixedOffset(1)),
                                  version=(2, 0))
    assert b == b"\xB3F\x00\x00\x3C"
    assert unpacked == DateTime(1970, 1, 1, 0, 0, 0, tzinfo=FixedOffset(1))


@mark.parametrize("cls", [timedelta, Duration])
def test_timedelta_and_duration(cls):
    b, unpacked = pack_and_unpack(cls(), version=(2, 0))
    assert b == b"\xB4E\x00\x00\x00\x00"
    assert unpacked == Duration()


@mark.parametrize("cls,srid", [(CartesianPoint, 7203), (WGS84Point, 4326)])
def test_2d_point(cls, srid):
    b, unpacked = pack_and_unpack(cls((0, 0)), version=(2, 0))
    assert b == b"\xB3X" + pack(srid) + b"\x00\x00"
    assert unpacked == cls((0, 0))


@mark.parametrize("cls,srid", [(CartesianPoint, 9157), (WGS84Point, 4979)])
def test_3d_point(cls, srid):
    b, unpacked = pack_and_unpack(cls((0, 0, 0)), version=(2, 0))
    assert b == b"\xB4Y" + pack(srid) + b"\x00\x00\x00"
    assert unpacked == cls((0, 0, 0))


def test_4d_point():
    with raises(ValueError):
        _ = pack(Point((0, 0, 0, 0)), version=(2, 0))
