#!/usr/bin/env python3

""" Module to test papers.py  """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import pytest
from papers import decide


def test_basic():
    assert decide("test_returning_citizen.json", "watchlist.json", "countries.json") == ["Accept", "Accept"]
    assert decide("test_watchlist.json", "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_quarantine.json", "watchlist.json", "countries.json") == ["Quarantine"]


def test_files():
    with pytest.raises(FileNotFoundError):
        decide("test_returning_citizen.json", "", "countries.json")
    with pytest.raises(FileNotFoundError):
        decide("", "", "")
    with pytest.raises(FileNotFoundError):
        decide("test_returning_citizen.json", "test_watchlist.json", "")
    with pytest.raises(FileNotFoundError):
        decide("", "test_watchlist.json", "countries.json")

# add functions for other tests

