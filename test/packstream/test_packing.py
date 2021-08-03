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


from pytest import mark, raises

from interchange.packstream import pack

from .common import (
    STR_S, STR_S_DATA,
    STR_M, STR_M_DATA,
    STR_L, STR_L_DATA,
    STR_XL,
    BYTEARRAY_S, BYTEARRAY_S_DATA,
    BYTEARRAY_M, BYTEARRAY_M_DATA,
    BYTEARRAY_L, BYTEARRAY_L_DATA,
    BYTEARRAY_XL,
    LIST_S, LIST_S_DATA,
    LIST_M, LIST_M_DATA,
    LIST_L, LIST_L_DATA,
    LIST_XL,
    DICT_S, DICT_S_DATA,
    DICT_M, DICT_M_DATA,
    DICT_L, DICT_L_DATA,
    DICT_XL,
)


def test_pack_null(benchmark):
    assert benchmark(pack, None) == b"\xC0"


def test_pack_true(benchmark):
    assert benchmark(pack, True) == b"\xC3"


def test_pack_false(benchmark):
    assert benchmark(pack, False) == b"\xC2"


def test_pack_int_xs(benchmark):
    assert benchmark(pack, 0) == b"\x00"


def test_pack_int_s(benchmark):
    assert benchmark(pack, -0x80) == b"\xC8\x80"


def test_pack_int_m(benchmark):
    assert benchmark(pack, 0x80) == b"\xC9\x00\x80"


def test_pack_int_l(benchmark):
    assert benchmark(pack, 0x8000) == b"\xCA\x00\x00\x80\x00"


def test_pack_int_xl(benchmark):
    assert benchmark(pack, 0x80000000) == b"\xCB\x00\x00\x00\x00\x80\x00\x00\x00"


def test_pack_int_pos_xxl():
    with raises(ValueError):
        pack(0x100000000000000000)


def test_pack_int_neg_xxl():
    with raises(ValueError):
        pack(-0x100000000000000000)


def test_pack_fp_pos_0(benchmark):
    assert benchmark(pack, float("+0.0")) == b"\xC1\x00\x00\x00\x00\x00\x00\x00\x00"


def test_pack_fp_neg_0(benchmark):
    assert benchmark(pack, float("-0.0")) == b"\xC1\x80\x00\x00\x00\x00\x00\x00\x00"


def test_pack_fp_pos_inf(benchmark):
    assert benchmark(pack, float("+inf")) == b"\xC1\x7F\xF0\x00\x00\x00\x00\x00\x00"


def test_pack_fp_neg_inf(benchmark):
    assert benchmark(pack, float("-inf")) == b"\xC1\xFF\xF0\x00\x00\x00\x00\x00\x00"


def test_pack_fp_nan(benchmark):
    assert benchmark(pack, float("nan")) == b"\xC1\x7F\xF8\x00\x00\x00\x00\x00\x00"


def test_pack_str_0(benchmark):
    assert benchmark(pack, "") == b"\x80"


def test_pack_str_xs(benchmark):
    assert benchmark(pack, "A") == b"\x81A"


def test_pack_str_s(benchmark):
    assert benchmark(pack, STR_S) == STR_S_DATA


def test_pack_str_m(benchmark):
    assert benchmark(pack, STR_M) == STR_M_DATA


def test_pack_str_l(benchmark):
    assert benchmark(pack, STR_L) == STR_L_DATA


def test_pack_str_xl():
    with raises(ValueError):
        _ = pack(STR_XL)


def test_pack_bytes_0(benchmark):
    assert benchmark(pack, bytearray()) == b"\xCC\x00"


def test_pack_bytes_s(benchmark):
    assert benchmark(pack, BYTEARRAY_S) == BYTEARRAY_S_DATA


def test_pack_bytes_m(benchmark):
    assert benchmark(pack, BYTEARRAY_M) == BYTEARRAY_M_DATA


def test_pack_bytes_l(benchmark):
    assert benchmark(pack, BYTEARRAY_L) == BYTEARRAY_L_DATA


def test_pack_byte_xl():
    with raises(ValueError):
        _ = pack(BYTEARRAY_XL)


def test_pack_list_0(benchmark):
    assert benchmark(pack, []) == b"\x90"


def test_pack_list_xs(benchmark):
    assert benchmark(pack, [0]) == b"\x91\x00"


def test_pack_list_s(benchmark):
    assert benchmark(pack, LIST_S) == LIST_S_DATA


def test_pack_list_m():
    assert pack(LIST_M) == LIST_M_DATA


def test_pack_list_l():
    assert pack(LIST_L) == LIST_L_DATA


def test_pack_list_xl():
    with raises(ValueError):
        _ = pack(LIST_XL)


def test_pack_dict_0(benchmark):
    assert benchmark(pack, {}) == b"\xA0"


def test_pack_dict_xs(benchmark):
    assert benchmark(pack, {"0": None}) == b"\xA1\x810\xC0"


def test_pack_dict_s(benchmark):
    assert benchmark(pack, DICT_S) == DICT_S_DATA


def test_pack_dict_m():
    assert pack(DICT_M) == DICT_M_DATA


def test_pack_dict_l():
    assert pack(DICT_L) == DICT_L_DATA


def test_pack_dict_xl():
    with raises(ValueError):
        _ = pack(DICT_XL)


def test_pack_dict_with_non_string_key():
    with raises(TypeError):
        _ = pack({object(): 1})


@mark.parametrize("version", [(1, 0), (2, 0)])
def test_packing_unknown_type(version):
    with raises(TypeError):
        _ = pack(object(), version=version)
