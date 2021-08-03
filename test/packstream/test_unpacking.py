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


from math import isnan

from pytest import raises

from interchange.packstream import unpack

from .common import (
    STR_S, STR_S_DATA,
    STR_M, STR_M_DATA,
    STR_L, STR_L_DATA,
    BYTEARRAY_S, BYTEARRAY_S_DATA,
    BYTEARRAY_M, BYTEARRAY_M_DATA,
    BYTEARRAY_L, BYTEARRAY_L_DATA,
    LIST_S, LIST_S_DATA,
    LIST_M, LIST_M_DATA,
    LIST_L, LIST_L_DATA,
    DICT_S, DICT_S_DATA,
    DICT_M, DICT_M_DATA,
    DICT_L, DICT_L_DATA,
)


def test_unpack_null(benchmark):
    assert next(benchmark(unpack, b"\xC0")) is None


def test_unpack_true(benchmark):
    assert next(benchmark(unpack, b"\xC3")) is True


def test_unpack_false(benchmark):
    assert next(benchmark(unpack, b"\xC2")) is False


def test_unpack_int_xs(benchmark):
    assert next(benchmark(unpack, b"\x00")) == 0


def test_unpack_int_s(benchmark):
    assert next(benchmark(unpack, b"\xC8\x80")) == -0x80


def test_unpack_int_m(benchmark):
    assert next(benchmark(unpack, b"\xC9\x00\x80")) == 0x80


def test_unpack_int_l(benchmark):
    assert next(benchmark(unpack, b"\xCA\x00\x00\x80\x00")) == 0x8000


def test_unpack_int_xl(benchmark):
    assert next(benchmark(unpack, b"\xCB\x00\x00\x00\x00\x80\x00\x00\x00")) == 0x80000000


def test_unpack_fp_pos_0(benchmark):
    assert next(benchmark(unpack, b"\xC1\x00\x00\x00\x00\x00\x00\x00\x00")) == float("+0.0")


def test_unpack_fp_neg_0(benchmark):
    assert next(benchmark(unpack, b"\xC1\x80\x00\x00\x00\x00\x00\x00\x00")) == float("-0.0")


def test_unpack_fp_pos_inf(benchmark):
    assert next(benchmark(unpack, b"\xC1\x7F\xF0\x00\x00\x00\x00\x00\x00")) == float("+inf")


def test_unpack_fp_neg_inf(benchmark):
    assert next(benchmark(unpack, b"\xC1\xFF\xF0\x00\x00\x00\x00\x00\x00")) == float("-inf")


def test_unpack_fp_nan(benchmark):
    assert isnan(next(benchmark(unpack, b"\xC1\x7F\xF8\x00\x00\x00\x00\x00\x00")))


def test_unpack_str_0(benchmark):
    assert next(benchmark(unpack, b"\x80")) == ""


def test_unpack_str_xs(benchmark):
    assert next(benchmark(unpack, b"\x81A")) == "A"


def test_unpack_str_s(benchmark):
    assert next(benchmark(unpack, STR_S_DATA)) == STR_S


def test_unpack_str_m(benchmark):
    assert next(benchmark(unpack, STR_M_DATA)) == STR_M


def test_unpack_str_l(benchmark):
    assert next(benchmark(unpack, STR_L_DATA)) == STR_L


def test_unpack_bytes_0(benchmark):
    assert next(benchmark(unpack, b"\xCC\x00")) == bytearray()


def test_unpack_bytes_s(benchmark):
    assert next(benchmark(unpack, BYTEARRAY_S_DATA)) == BYTEARRAY_S


def test_unpack_bytes_m(benchmark):
    assert next(benchmark(unpack, BYTEARRAY_M_DATA)) == BYTEARRAY_M


def test_unpack_bytes_l(benchmark):
    assert next(benchmark(unpack, BYTEARRAY_L_DATA)) == BYTEARRAY_L


def test_unpack_list_0(benchmark):
    assert next(benchmark(unpack, b"\x90")) == []


def test_unpack_list_xs(benchmark):
    assert next(benchmark(unpack, b"\x91\x00")) == [0]


def test_unpack_list_s(benchmark):
    assert next(benchmark(unpack, LIST_S_DATA)) == LIST_S


def test_unpack_list_m(benchmark):
    assert next(benchmark(unpack, LIST_M_DATA)) == LIST_M


def test_unpack_list_l(benchmark):
    assert next(benchmark(unpack, LIST_L_DATA)) == LIST_L


def test_unpack_dict_0(benchmark):
    assert next(benchmark(unpack, b"\xA0")) == {}


def test_unpack_dict_xs(benchmark):
    assert next(benchmark(unpack, b"\xA1\x810\xC0")) == {"0": None}


def test_unpack_dict_s(benchmark):
    assert next(benchmark(unpack, DICT_S_DATA)) == DICT_S


def test_unpack_dict_m(benchmark):
    assert next(benchmark(unpack, DICT_M_DATA)) == DICT_M


def test_unpack_dict_l(benchmark):
    assert next(benchmark(unpack, DICT_L_DATA)) == DICT_L


def test_unpack_unknown_marker():
    with raises(ValueError):
        _ = next(unpack(b"\xDF"))


def test_unpack_multiple():
    assert list(unpack(b"\x01\x02\x03")) == [1, 2, 3]
