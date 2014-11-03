#!/usr/bin/env python3

""" Computer-based immigration office for Kanadia """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import re
import datetime
from datetime import date
import json


def decide(input_file, watchlist_file, countries_file):
    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains cases to decide
    :param watchlist_file: The name of a JSON formatted file that contains names and passport numbers on a watchlist
    :param countries_file: The name of a JSON formatted file that contains country data, such as whether
        an entry or transit visa is required, and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are: "Accept", "Reject", "Secondary", and "Quarantine"
    """

    entry_decision_list = []
    #Check the existence of the file


    # needs to have for loop to iterate the list
        #For each entry information, store them into the corresponding variables


        # via info variables - set the via information availability to false
        # if there's no via key in the entry record


        # Visa info variables - set the Viaa information availability to false
        # if there's no Visa key in the entry record

        # Check the input format validity for each field in the entry record

        # Check whether the current entry record is in the watchlist, then decide to accept or send to secondary

        # Check whether the current entry record is coming from or via country that has medical advisory
        # then decide to accept or send to quarantine

        # Check whether visa is required. If required, check whether entry record has correct visa information

        # Compile each decision, then make final decision by the order of priority

    return entry_decision_list


def valid_passport_format(passport_number):
    """
    Checks whether a pasport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    passport_format = re.compile('.{5}-.{5}-.{5}-.{5}-.{5}')

    if passport_format.match(passport_number) and re.match('^[a-zA-Z0-9-]+$', passport_number) is not None\
            and len(passport_number.replace('-', '')) == 25:
        return True
    else:
        return False


def valid_date_format(date_string):
    """
    Checks whether a date has the format YYYY-mm-dd in numbers
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def valid_visa_code_format(visa_code):
    """
    Checks whether the given Visa code has a valid format
    :param visa_code: Visa code to be checked
    :return: Boolean True if Visa format is valid, False otherwise
    """

def check_visa_expiry(visa_date):
    """
    Checks whether the given Visa is expired or not (Visa must be less than 2 years old)
    :param visa_date: Visa date to be checked
    :return: Boolean True if Visa date is less than 2 years old, False otherwise
    """

    # Get today's date, then subtract 2 years from it using try/except clause
    # to consider leap year.
    today_date = datetime.date.today()
    try:
        two_years_ago_from_today = today_date.replace(year=today_date.year - 2)
    except ValueError:
        two_years_ago_from_today = today_date + (date(today_date.year - 2, 1, 1) - date(today_date.year, 1, 1))

    visa_date = datetime.datetime.strptime(visa_date, '%Y-%m-%d')

    time_difference_in_days = (visa_date.date() - two_years_ago_from_today).days
    if time_difference_in_days > 0:
        return True
    else:
        return False

def has_medical_advisory(country_code, country_info_list):
    """
    Check whether the given country (country code) has a medical advisory alert
    :param country_code: Country Code - 3 letters
    :param country_info_list: List that contains medical advisory information for each country
    :return: Boolean True if country is under medical advisory, False otherwise.
    """



def parse_json_to_python_list (json_file):
    """
    Parse JSON file to python list and return the parsed list.
    :param json_file: JSON file to be parsed
    :return:List, List file generated from parsed JSON file
    """
    return parsed_list

def valid_basic_info_availability(entry_record):
    """
    Check whether the person has all the required basic information available.
    :param entry_record: entry record to be checked for the basic information availability
    :return:True if all the information exists, False otherwise.
    """

    return False

def is_visa_required(country_code, required_visa_type, country_list):
    """
    Check whether the country requires the transit/visitor visa or not
    :param country_code: Country Code - 3 Characters
    :param required_visa_type: Required Visa Type - transit/visit
    :param country_list: list of country with Visa requirement information
    :return: True if transit visa is required. False otherwise
    """

def is_in_watchlist(first_name, last_name, passport_number, watchlist):
    """
    Check whether the provided personal information is in the provided watchlist
    :param first_name: first name to be checked
    :param last_name:  last name to be checked
    :param passport_number: passport number to be checked
    :param watchlist: watchlist to be checked against
    :return: True if match was found in the watchlist, False otherwise
    """
