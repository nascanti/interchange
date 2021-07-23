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


from interchange.collections import PropertyDict


def test_equality():
    first = PropertyDict({"name": "Alice", "age": 33, "colours": ["red", "purple"]})
    second = PropertyDict({"name": "Alice", "age": 33, "colours": ["red", "purple"]})
    assert first == second


def test_inequality():
    first = PropertyDict({"name": "Alice", "age": 33, "colours": ["red", "purple"]})
    second = PropertyDict({"name": "Bob", "age": 44, "colours": ["blue", "purple"]})
    assert first != second


def test_getter():
    properties = PropertyDict({"name": "Alice"})
    assert properties["name"] == "Alice"


def test_getter_with_none():
    properties = PropertyDict({"name": "Alice"})
    assert properties["age"] is None


def test_setter():
    properties = PropertyDict({"name": "Alice"})
    properties["age"] = 33
    assert properties == {"name": "Alice", "age": 33}


def test_setter_with_none():
    properties = PropertyDict({"name": "Alice", "age": 33})
    properties["age"] = None
    assert properties == {"name": "Alice"}


def test_setter_with_none_for_non_existent():
    properties = PropertyDict({"name": "Alice"})
    properties["age"] = None
    assert properties == {"name": "Alice"}


def test_setdefault_without_default_with_existing():
    properties = PropertyDict({"name": "Alice", "age": 33})
    value = properties.setdefault("age")
    assert properties == {"name": "Alice", "age": 33}
    assert value == 33


def test_setdefault_without_default_with_non_existent():
    properties = PropertyDict({"name": "Alice"})
    value = properties.setdefault("age")
    assert properties == {"name": "Alice"}
    assert value is None


def test_setdefault_with_default_with_existing():
    properties = PropertyDict({"name": "Alice", "age": 33})
    value = properties.setdefault("age", 34)
    assert properties == {"name": "Alice", "age": 33}
    assert value == 33


def test_setdefault_with_default_with_non_existent():
    properties = PropertyDict({"name": "Alice"})
    value = properties.setdefault("age", 33)
    assert properties == {"name": "Alice", "age": 33}
    assert value == 33


def test_deleter():
    properties = PropertyDict({"name": "Alice", "age": 33})
    del properties["age"]
    assert properties == {"name": "Alice"}
