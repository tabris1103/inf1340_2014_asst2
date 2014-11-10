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
    entry_list = parse_json_to_python_list(input_file)
    watch_list = parse_json_to_python_list(watchlist_file)
    country_list = parse_json_to_python_list(countries_file)

    # needs to have for loop to iterate the list
    for entry_record in entry_list:
        entry_decision_for_current_record = []

        #For each entry information, store them into the corresponding variables if the variable exists.
        try:
            first_name = valid_basic_info_availability(entry_record['first_name'])
            last_name = valid_basic_info_availability(entry_record['last_name'])
            birth_date = valid_basic_info_availability(entry_record['birth_date'])
            passport = valid_basic_info_availability(entry_record['passport'])
            home_city = valid_basic_info_availability(entry_record['home']['city'])
            home_region = valid_basic_info_availability(entry_record['home']['region'])
            home_country = valid_basic_info_availability(entry_record['home']['country'])
            from_city = valid_basic_info_availability(entry_record['from']['city'])
            from_region = valid_basic_info_availability(entry_record['from']['region'])
            from_country = valid_basic_info_availability(entry_record['from']['country'])
            entry_reason = valid_basic_info_availability(entry_record['entry_reason'])

            # store via variable only when via key is in the record
            if 'via' in entry_record:
                via_city = valid_basic_info_availability(entry_record['via']['city'])
                via_region = valid_basic_info_availability(entry_record['via']['region'])
                via_country = valid_basic_info_availability(entry_record['via']['country'])
            # store visa variable only when visa key is in the record
            if 'visa' in entry_record:
                visa_date = valid_basic_info_availability(entry_record['visa']['date'])
                visa_code = valid_basic_info_availability(entry_record['visa']['code'])
        except ValueError:
            basic_info_availability_decision = 'Reject'
        else:
            basic_info_availability_decision = 'Accept'

        #-- Check the date input format validity for each date field in the entry record
        if valid_passport_format(passport) is False:
            information_validity_decision = 'Reject'
        elif valid_date_format(birth_date) is False:
            information_validity_decision = 'Reject'
        elif 'visa' in entry_record:
            if valid_date_format(visa_date) is False:
                information_validity_decision = 'Reject'
            elif valid_visa_code_format(visa_code) is False:
                information_validity_decision = 'Reject'
            else:
                information_validity_decision = 'Accept'
        else:
            information_validity_decision = 'Accept'

        #-- Check whether the current entry record is in the watchlist, then decide to accept or send to secondary
        if is_in_watchlist(first_name, last_name, passport, watch_list):
            watchlist_decision = 'Secondary'
        else:
            watchlist_decision = 'Accept'

        # Check whether the current entry record is coming from or via country that has medical advisory
        # then decide to accept or send to quarantine
        if 'via' in entry_record:
            check_medical_advisory = has_medical_advisory(via_country, country_list) or \
                has_medical_advisory(from_country, country_list)
        else:
            check_medical_advisory = has_medical_advisory(from_country, country_list)

        medical_advisory_decision = 'Quarantine' if check_medical_advisory else 'Accept'

        # Check whether visa is required. If required, check whether entry record has correct visa information
        if is_visa_required(home_country, entry_reason, country_list):
            if 'visa' in entry_record:
                if valid_date_format(visa_date) and valid_visa_code_format(visa_code) and check_visa_expiry(visa_date):
                    visa_decision = 'Accept'
                else:
                    visa_decision = 'Reject'
            else:
                visa_decision = 'Reject'
        else:
            visa_decision = 'Accept'

        if entry_reason.lower() == 'returning' and home_country.upper() == 'KAN':
            return_entry_decision = 'Accept'
        else:
            return_entry_decision = 'N/A'

        # Compile each decision, then make final decision by the order of priority
        entry_decision_for_current_record.append(basic_info_availability_decision)
        entry_decision_for_current_record.append(return_entry_decision)
        entry_decision_for_current_record.append(watchlist_decision)
        entry_decision_for_current_record.append(visa_decision)
        entry_decision_for_current_record.append(medical_advisory_decision)
        entry_decision_for_current_record.append(information_validity_decision)

        print('info_complete_decision: ' + basic_info_availability_decision)
        print('return_entry_decision: ' + return_entry_decision)
        print('watchlist_decision: ' + watchlist_decision)
        print('visa_decision: ' + visa_decision)
        print('medical_advisory_decision: ' + medical_advisory_decision)
        print('info_validity_decision: ' + information_validity_decision)
        print(' ')

        if 'Quarantine' in entry_decision_for_current_record:
            entry_decision_list.append('Quarantine')
        elif 'Reject' in entry_decision_for_current_record:
            entry_decision_list.append('Reject')
        elif 'Secondary' in entry_decision_for_current_record:
            entry_decision_list.append('Secondary')
        elif 'Accept' in entry_decision_for_current_record:
            entry_decision_list.append('Accept')

    return entry_decision_list



def valid_passport_format(passport_number):
    """
    Checks whether a passports number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    passport_format = re.compile('^\w{5}-\w{5}-\w{5}-\w{5}-\w{5}$')

    if passport_format.match(passport_number):
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
    visa_format = re.compile('^\w{5}-\w{5}$')

    if visa_format.match(visa_code):
        return True
    else:
        return False
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
    medical_advisory = country_info_list[country_code]['medical_advisory']
    if len(medical_advisory) > 0:
        return True
    else:
        return False


def parse_json_to_python_list (json_file):
    """
    Parse JSON file to python list and return the parsed list.
    :param json_file: JSON file to be parsed
    :return:List, List file generated from parsed JSON file
    """
    json_file_reader = open(json_file, "r")
    file_contents = json_file_reader.read()
    parsed_list = json.loads(file_contents)
    json_file_reader.close()

    return parsed_list


def valid_basic_info_availability(key_value):
    """
    Check whether the person has all the required basic information available.
    :param entry_record: entry record to be checked for the basic information availability
    :return:True if all the information exists, False otherwise.
    """
    if key_value == "":
        raise ValueError("Field value is not complete!")
    else:
        return key_value

def is_visa_required(country_code, required_visa_type, country_list):
    """
    Check whether the country requires the transit/visitor visa or not
    :param country_code: Country Code - 3 Characters
    :param required_visa_type: Required Visa Type - transit/visit
    :param country_list: list of country with Visa requirement information
    :return: True if transit visa is required. False otherwise
    """
    if country_code == 'KAN':
        return False
    if required_visa_type.lower() == 'transit':
        if country_list[country_code]['transit_visa_required'] == '1':
            return True
        else:
            return False
    else:
        if country_list[country_code]['visitor_visa_required'] == '1':
            return True
        else:
            return False

def is_in_watchlist(first_name, last_name, passport_number, watchlist):
    """
    Check whether the provided personal information is in the provided watchlist
    :param first_name: first name to be checked
    :param last_name:  last name to be checked
    :param passport_number: passport number to be checked
    :param watchlist: watchlist to be checked against
    :return: True if match was found in the watchlist, False otherwise
    """
    in_watchlist = False
    for watchlist_record in watchlist:
        first_name_in_watchlist_record = watchlist_record['first_name']
        last_name_in_watchlist_record = watchlist_record['last_name']
        passport_num_in_watchlist_record = watchlist_record['passport']

        if ((first_name.upper() == first_name_in_watchlist_record.upper() and
            last_name.upper() == last_name_in_watchlist_record.upper())
                or passport_number == passport_num_in_watchlist_record):
            in_watchlist = True

    return in_watchlist
