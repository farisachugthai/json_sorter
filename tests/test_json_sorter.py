#!/usr/bin/env python
"""Tests for `json_sorter` package."""
import json
from pathlib import Path

import pytest

from json_sorter.core import sort_json


def test_sort_json():
    test_data = Path.resolve(Path('./tests/data/settings.json'))
    fixed = sort_json(test_data)
    reloaded = json.loads(fixed)
    keys = list(reloaded.keys())
    assert keys[0] < keys[1]


if __name__ == "__main__":
    pytest.main()
