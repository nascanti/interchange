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


import random
from collections import OrderedDict
from struct import pack_into as struct_pack_into

from .common import assert_packable


def test_inline_integer():
    for i in range(-16, 128):
        assert_packable(i, bytes(bytearray([i % 0x100])))


def test_8bit_integer():
    for i in range(-128, -16):
        assert_packable(i, bytes(bytearray([0xC8, i % 0x100])))


def test_16bit_negative_integer():
    for i in range(-0x8000, -0x80):
        data = bytearray([0xC9, 0, 0])
        struct_pack_into(">h", data, 1, i)
        assert_packable(i, data)


def test_16bit_positive_integer():
    for i in range(0x80, 0x8000):
        data = bytearray([0xC9, 0, 0])
        struct_pack_into(">h", data, 1, i)
        assert_packable(i, data)


def test_32bit_negative_integer():
    for i in range(-0x80000000, -0x8000, 100001):
        data = bytearray([0xCA, 0, 0, 0, 0])
        struct_pack_into(">i", data, 1, i)
        assert_packable(i, data)


def test_32bit_positive_integer():
    for i in range(0x8000, 0x80000000, 100001):
        data = bytearray([0xCA, 0, 0, 0, 0])
        struct_pack_into(">i", data, 1, i)
        assert_packable(i, data)


def test_64bit_negative_integer():
    for i in range(-0x8000000000000000, -0x80000000, 1000000000000001):
        data = bytearray([0xCB, 0, 0, 0, 0, 0, 0, 0, 0])
        struct_pack_into(">q", data, 1, i)
        assert_packable(i, data)


def test_64bit_positive_integer():
    for i in range(0x80000000, 0x8000000000000000, 1000000000000001):
        data = bytearray([0xCB, 0, 0, 0, 0, 0, 0, 0, 0])
        struct_pack_into(">q", data, 1, i)
        assert_packable(i, data)


def test_float():
    random.seed(0)
    for _ in range(10000):
        n = random.uniform(-1e10, 1e10)
        data = bytearray([0xC1, 0, 0, 0, 0, 0, 0, 0, 0])
        struct_pack_into(">d", data, 1, n)
        assert_packable(n, data)


def test_inline_unicode_string():
    for n in range(16):
        s = "A" * n
        data = bytearray([0x80 + n]) + s.encode("utf-8")
        assert_packable(s, data)


def test_small_string():
    for n in range(16, 256):
        s = "A" * n
        data = bytearray([0xD0, n]) + s.encode("utf-8")
        assert_packable(s, data)


def test_small_byte_array():
    for n in range(16, 256):
        b = bytearray(n)
        data = bytearray([0xCC, n]) + b
        assert_packable(b, data)


def test_inline_list():
    for n in range(16):
        s = [0] * n
        data = bytearray([0x90 + n]) + b"\x00" * n
        assert_packable(s, data)


def test_small_list():
    for n in range(16, 256):
        b = [0] * n
        data = bytearray([0xD4, n]) + b"\x00" * n
        assert_packable(b, data)


def test_inline_dict():
    for n in range(16):
        keys = ["%02X" % i for i in range(n)]
        s = OrderedDict.fromkeys(keys)
        data = bytearray([0xA0 + n]) + b"".join(b"\x82" + key.encode("utf-8") + b"\xC0"
                                                for key in keys)
        assert_packable(s, data)


def test_small_dict():
    for n in range(16, 256):
        keys = ["%02X" % i for i in range(n)]
        b = OrderedDict.fromkeys(keys)
        data = bytearray([0xD8, n]) + b"".join(b"\x82" + key.encode("utf-8") + b"\xC0"
                                               for key in keys)
        assert_packable(b, data)
