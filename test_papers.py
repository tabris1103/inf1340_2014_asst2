#!/usr/bin/env python3

""" Module to test papers.py  """

__author__ = 'Shawn Jung & Jordan Rae'

# imports one per line
import pytest
from papers import decide


def test_basic():
    assert decide("test_returning_citizen.json", "watchlist.json", "countries.json") == ["Accept", "Accept"]
    assert decide("test_watchlist.json", "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_quarantine.json", "watchlist.json", "countries.json") == ["Quarantine"]


# Test case to see whether the program correctly catches the incompleteness of the required data
def test_required_info_availability():


# Test case to see whether the traveller's visa check functionality is performing correctly
def test_valid_visa():


# Testing Medical Advisory Check
def test_medical_advisory():

  
# Testing Secondary Processing Check
def test_secondary():
    assert decide("test_secondary.json", "watchlist.json", "countries.json") == ['Secondary', 'Secondary', 'Reject',
                                                                                 'Quarantine']


def test_files():
    with pytest.raises(FileNotFoundError):
        decide("test_returning_citizen.json", "", "countries.json")
    with pytest.raises(FileNotFoundError):
        decide("", "", "")
    with pytest.raises(FileNotFoundError):
        decide("test_returning_citizen.json", "test_watchlist.json", "")
    with pytest.raises(FileNotFoundError):
        decide("", "test_watchlist.json", "countries.json")


