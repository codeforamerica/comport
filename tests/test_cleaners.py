# -*- coding: utf-8 -*-
from comport.data.cleaners import Cleaners, RESIDENT_WEAPONS_LOOKUP, OFFICER_FORCE_TYPE_LOOKUP, RACE_LOOKUP, GENDER_LOOKUP, CAPITALIZE_LIST, CAPITALIZE_IGNORE_KEYS_LIST
from titlecase import titlecase

class TestCleaners:

    def test_unknown_resident_weapon_returned(self):
        ''' Cleaning an unknown weapon returns the same value passed.
        '''
        cleaner = Cleaners()
        weapon = "Suspect - Lewd Nebulosity "
        cleaned = cleaner.resident_weapon_used(weapon)
        assert cleaned == weapon

    def test_known_resident_weapons_cleaned(self):
        ''' Cleaning known weapons returns the expected value.
        '''
        cleaner = Cleaners()
        for weapon in RESIDENT_WEAPONS_LOOKUP:
            check_weapon = cleaner.resident_weapon_used(weapon)
            assert check_weapon == RESIDENT_WEAPONS_LOOKUP[weapon]

    def test_unknown_officer_force_type_returned(self):
        ''' Cleaning an unknown weapon returns the same value passed.
        '''
        cleaner = Cleaners()
        force_type = "Bugbear Squeeze"
        cleaned = cleaner.officer_force_type(force_type)
        assert cleaned == force_type

    def test_known_officer_force_types_cleaned(self):
        ''' Cleaning known weapons returns the expected value.
        '''
        cleaner = Cleaners()
        for force_type in OFFICER_FORCE_TYPE_LOOKUP:
            check_force_type = cleaner.officer_force_type(force_type)
            assert check_force_type == OFFICER_FORCE_TYPE_LOOKUP[force_type]

    def test_unknown_race_returned(self):
        ''' Cleaning an unknown race returns the same value passed.
        '''
        cleaner = Cleaners()
        race = "Comet"
        cleaned = cleaner.race(race)
        assert cleaned == race

    def test_known_races_cleaned(self):
        ''' Cleaning known races returns the expected value.
        '''
        cleaner = Cleaners()
        for race in RACE_LOOKUP:
            check_race = cleaner.race(race)
            assert check_race == RACE_LOOKUP[race]

    def test_unknown_gender_returned(self):
        ''' Cleaning an unknown gender returns the same value passed.
        '''
        cleaner = Cleaners()
        gender = "Golf"
        cleaned = cleaner.sex(gender)
        assert cleaned == gender

    def test_known_genders_cleaned(self):
        ''' Cleaning known genders returns the expected value.
        '''
        cleaner = Cleaners()
        for gender in GENDER_LOOKUP:
            check_gender = cleaner.sex(gender)
            assert check_gender == GENDER_LOOKUP[gender]

    def test_capitalization(self):
        ''' A phrase is title-cased with expected exceptions.
        '''
        cleaner = Cleaners()
        in_sentence = "I thought I would sail about a little and see the watery part of the world"
        titlecased_sentence = titlecase(in_sentence)
        send = " ".join(i.lower() + " " + j.lower() for i, j in zip(in_sentence.split(" "), CAPITALIZE_LIST))
        check = " ".join(i + " " + j for i, j in zip(titlecased_sentence.split(" "), CAPITALIZE_LIST))
        result = cleaner.capitalize(send)
        assert check == result

    def test_captilization_handles_non_strings(self):
        ''' Non-strings passed to capitalize aren't altered.
        '''
        cleaner = Cleaners()
        send_int = 23
        send_float = 32.01
        send_list = ["I", "thought", "I", "would", "sail"]
        result_int = cleaner.capitalize(send_int)
        result_float = cleaner.capitalize(send_float)
        result_list = cleaner.capitalize(send_list)
        assert send_int == result_int
        assert send_float == result_float
        assert send_list == result_list

    def test_incident_capitalization(self):
        ''' Incident descriptions are title-cased with expected exceptions.
        '''
        cleaner = Cleaners()
        in_sentence = "It is a way I have of driving off the spleen and regulating the circulation"
        titlecased_sentence = titlecase(in_sentence)
        send = {}
        send["damp"] = in_sentence
        send["drizzly"] = in_sentence
        for key in CAPITALIZE_IGNORE_KEYS_LIST:
            send[key] = in_sentence

        result = cleaner.capitalize_incident(send)

        # values of keys not in the list should be titlecased
        assert result["damp"] == titlecased_sentence
        assert result["drizzly"] == titlecased_sentence
        # values of keys in the list should not be titlecased
        for key in CAPITALIZE_IGNORE_KEYS_LIST:
            assert result[key] == in_sentence

    def test_number_to_string(self):
        ''' Numbers are turned into strings.
        '''
        cleaner = Cleaners()
        in_int = 85
        in_float = 82.12
        in_string = "big frame, small spirit!"
        in_list = ["hands", "by", "the", "halyards"]
        in_none = None
        assert cleaner.number_to_string(in_int) == str(in_int)
        assert cleaner.number_to_string(in_float) == str(in_float)
        assert cleaner.number_to_string(in_string) == in_string
        assert cleaner.number_to_string(in_list) == in_list
        assert cleaner.number_to_string(in_none) is None

    def test_string_to_integer(self):
        ''' Strings are turned into integers.
        '''
        cleaner = Cleaners()
        in_string_success_int = '85'
        in_string_success_float = '33.34'
        in_int = 85
        in_float = 82.12
        in_string_fail = 'whaleman'
        in_list = ["hands", "by", "the", "halyards"]
        in_none = None
        assert cleaner.string_to_integer(in_string_success_int) == int(in_string_success_int)
        assert cleaner.string_to_integer(in_string_success_float) == int(float(in_string_success_float))
        assert cleaner.string_to_integer(in_int) == in_int
        assert cleaner.string_to_integer(in_float) == int(in_float)
        assert cleaner.string_to_integer(in_string_fail) is None
        assert cleaner.string_to_integer(in_list) is None
        assert cleaner.string_to_integer(in_none) is None
