# -*- coding: utf-8 -*-
from comport.data.cleaners import Cleaners, RESIDENT_WEAPONS_LOOKUP, OFFICER_FORCE_TYPE_LOOKUP, RACE_LOOKUP, GENDER_LOOKUP, CAPITALIZE_LIST, CAPITALIZE_IGNORE_LIST

class TestCleaners:

    def test_unknown_resident_weapon_returned(self):
        ''' Cleaning an unknown weapon returns the same value passed.
        '''
        weapon = "Suspect - Lewd Nebulosity "
        cleaned = Cleaners.resident_weapon_used(weapon)
        assert cleaned == weapon

    def test_known_resident_weapons_cleaned(self):
        ''' Cleaning known weapons returns the expected value.
        '''
        for weapon in RESIDENT_WEAPONS_LOOKUP:
            check_weapon = Cleaners.resident_weapon_used(weapon)
            assert check_weapon == RESIDENT_WEAPONS_LOOKUP[weapon]

    def test_unknown_officer_force_type_returned(self):
        ''' Cleaning an unknown weapon returns the same value passed.
        '''
        force_type = "Bugbear Squeeze"
        cleaned = Cleaners.officer_force_type(force_type)
        assert cleaned == force_type

    def test_known_officer_force_types_cleaned(self):
        ''' Cleaning known weapons returns the expected value.
        '''
        for force_type in OFFICER_FORCE_TYPE_LOOKUP:
            check_force_type = Cleaners.officer_force_type(force_type)
            assert check_force_type == OFFICER_FORCE_TYPE_LOOKUP[force_type]

    def test_unknown_race_returned(self):
        ''' Cleaning an unknown race returns the same value passed.
        '''
        race = "Comet"
        cleaned = Cleaners.race(race)
        assert cleaned == race

    def test_known_races_cleaned(self):
        ''' Cleaning known races returns the expected value.
        '''
        for race in RACE_LOOKUP:
            check_race = Cleaners.race(race)
            assert check_race == RACE_LOOKUP[race]

    def test_unknown_gender_returned(self):
        ''' Cleaning an unknown gender returns the same value passed.
        '''
        gender = "Golf"
        cleaned = Cleaners.sex(gender)
        assert cleaned == gender

    def test_known_genders_cleaned(self):
        ''' Cleaning known genders returns the expected value.
        '''
        for gender in GENDER_LOOKUP:
            check_gender = Cleaners.sex(gender)
            assert check_gender == GENDER_LOOKUP[gender]
