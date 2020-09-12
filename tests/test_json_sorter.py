#!/usr/bin/env python
"""Tests for `json_sorter` package."""
import json
from pathlib import Path

import pytest

from json_sorter.core import sort_json, text_writer


def test_sort_json():
    test_data = Path.resolve(Path('./tests/data/settings.json'))
    fixed = sort_json(test_data)
    reloaded = json.loads(fixed)
    keys = list(reloaded.keys())
    assert keys[0] < keys[1]


def test_sort_json_logging(caplog):
    caplog.set_level(10)
    test_data = Path.resolve(Path('./tests/data/settings.json'))
    fixed = sort_json(test_data)
    assert len(caplog.records) == 1


def test_text_writer(tmp_path):
    file_to_check = tmp_path / "text_writer.log"
    text_writer("foo", output_file=file_to_check)
    assert Path(file_to_check).is_file()


def test_text_writer_logging(caplog, tmp_path):
    caplog.set_level(10)
    text_writer("foo", output_file=tmp_path / "text_writer_logging.log")
    assert len(caplog.records) == 1


if __name__ == "__main__":
    pytest.main()
