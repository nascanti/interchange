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


from collections import OrderedDict

from six import text_type

from interchange.packstream import Packer, unpack


def pack_and_unpack(value, version=()):
    packer = Packer(version=version)
    packer.pack(value)
    b = packer.packed()
    unpacked = next(unpack(b))
    return b, unpacked


def assert_packable(value, b, protocol_version=()):
    assert pack_and_unpack(value, protocol_version) == (b, value)


class FakeString(text_type):

    def __init__(self, size):
        super(FakeString, self).__init__()
        self.size = size

    def __len__(self):
        return self.size

    def __getitem__(self, item):
        return '\u0000'

    def encode(self, encoding="utf-8", errors="strict"):
        return FakeBytes(self.size)


class FakeBytes(bytes):

    def __init__(self, size):
        super(FakeBytes, self).__init__()
        self.size = size

    def __len__(self):
        return self.size


class FakeByteArray(bytearray):

    def __init__(self, size):
        super(FakeByteArray, self).__init__()
        self.size = size

    def __len__(self):
        return self.size


class FakeList(list):

    def __init__(self, size):
        super(FakeList, self).__init__()
        self.size = size

    def __len__(self):
        return self.size


class FakeDict(OrderedDict):

    def __init__(self, size):
        super(FakeDict, self).__init__()
        self.size = size

    def __len__(self):
        return self.size


STR_S = "A" * 0x10
STR_S_DATA = b"\xD0\x10" + b"A" * 0x10

STR_M = "A" * 0x100
STR_M_DATA = b"\xD1\x01\x00" + b"A" * 0x100

STR_L = "A" * 0x10000
STR_L_DATA = b"\xD2\x00\x01\x00\x00" + b"A" * 0x10000

STR_XL = FakeString(0x100000000)

BYTEARRAY_S = bytearray([0] * 0x10)
BYTEARRAY_S_DATA = b"\xCC\x10" + b"\x00" * 0x10

BYTEARRAY_M = bytearray([0] * 0x100)
BYTEARRAY_M_DATA = b"\xCD\x01\x00" + b"\x00" * 0x100

BYTEARRAY_L = bytearray([0] * 0x10000)
BYTEARRAY_L_DATA = b"\xCE\x00\x01\x00\x00" + b"\x00" * 0x10000

BYTEARRAY_XL = FakeByteArray(0x100000000)

LIST_S = [0] * 0x10
LIST_S_DATA = b"\xD4\x10" + b"\x00" * 0x10

LIST_M = [0] * 0x100
LIST_M_DATA = b"\xD5\x01\x00" + b"\x00" * 0x100

LIST_L = [0] * 0x10000
LIST_L_DATA = b"\xD6\x00\x01\x00\x00" + b"\x00" * 0x10000

LIST_XL = FakeList(0x100000000)

DICT_S_KEYS = ["%02X" % _ for _ in range(0x10)]
DICT_S = OrderedDict.fromkeys(DICT_S_KEYS)
DICT_S_DATA = (bytearray([0xD8, 0x10]) +
               b"".join(b"\x82" + key.encode("utf-8") + b"\xC0"
                        for key in DICT_S_KEYS))

DICT_M_KEYS = ["%02X" % i for i in range(0x100)]
DICT_M = OrderedDict.fromkeys(DICT_M_KEYS)
DICT_M_DATA = (bytearray([0xD9, 0x01, 0x00]) +
               b"".join(b"\x82" + key.encode("utf-8") + b"\xC0"
                        for key in DICT_M_KEYS))

DICT_L_KEYS = ["%04X" % i for i in range(0x10000)]
DICT_L = OrderedDict.fromkeys(DICT_L_KEYS)
DICT_L_DATA = (bytearray([0xDA, 0x00, 0x01, 0x00, 0x00]) +
               b"".join(b"\x84" + key.encode("utf-8") + b"\xC0"
                        for key in DICT_L_KEYS))

DICT_XL = FakeDict(0x100000000)
