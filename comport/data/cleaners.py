from titlecase import titlecase

RESIDENT_WEAPONS_LOOKUP = {
    "Suspect - Handgun": "Handgun",
    "Suspect - Knife": "Knife",
    "Suspect - Misc Weapon": "Misc Weapon",
    "Suspect - Rifle": "Rifle",
    "Suspect - Unarmed": "Unarmed"
}

OFFICER_FORCE_TYPE_LOOKUP = {
    "Baton": "Less Lethal-Baton",
    "Bean Bag": "Less Lethal-Bean Bag",
    "Body Weight Leverage": "Physical-Weight Leverage",
    "Canine bite": "Canine Bite",
    "CS Fogger": "Less Lethal-CS/OC",
    "Handcuffing": "Physical-Handcuffing",
    "Handgun": "Lethal-Handgun",
    "Hands, Fist, Feet": "Physical-Hands, Fist, Feet",
    "Joint Manipulation": "Physical-Joint/Pressure",
    "Less Lethal-Leg Sweep": "Physical-Leg Sweep",
    "Other Impact Weapon": "Less Lethal-Other",
    "Pepper Ball": "Less Lethal-Pepperball",
    "Personal CS/OC spray": "Less Lethal-Personal CS/OC spray",
    "Taser": "Less Lethal-Taser",
    "Vehicle": "Lethal-Vehicle"
}

RACE_LOOKUP = {
    "B": "Black"
}

GENDER_LOOKUP = {
    "F": "Female",
    "M": "Male"
}

CAPITALIZE_LIST = [
    "AWOL",
    "BUR",
    "BWC",
    "CD",
    "CDS",
    "CEW",
    "CID",
    "CN",
    "CPCO",
    "CS",
    "DDS",
    "DDU",
    "DT",
    "DUI",
    "DV",
    "DWI",
    "ECD",
    "ECW",
    "ED",
    "EEO",
    "FB",
    "FTO",
    "HIDTA",
    "IAD",
    "IID",
    "LGBT",
    "ND",
    "NED",
    "NW",
    "NWD",
    "OC",
    "ODE",
    "OID",
    "OIS",
    "OPR",
    "PA",
    "PC",
    "PDTA",
    "RATT",
    "SD",
    "SE",
    "SED",
    "SES",
    "SIS",
    "SOD",
    "SODD",
    "SOS",
    "SW",
    "SWAT",
    "SWD",
    "TD",
    "UC",
    "UOF",
    "VBLETA",
    "VCID",
    "VCS",
    "VRO",
    "VSC",
    "WATF",
    "WD"
]

CAPITALIZE_IGNORE_KEYS_LIST = [
    "opaqueId",
    "caseNumber",
    "occuredDate",
    "receivedDate",
    "completedDate",
    "residentIdentifier",
    "residentAge",
    "officerIdentifier",
    "officerYearsOfService"
]

class Cleaners(object):

    def resident_weapon_used(self, val):
        if val in RESIDENT_WEAPONS_LOOKUP:
            return RESIDENT_WEAPONS_LOOKUP[val]
        else:
            return val

    def officer_force_type(self, text):
        if text is not None and text in OFFICER_FORCE_TYPE_LOOKUP:
            return OFFICER_FORCE_TYPE_LOOKUP[text]
        return self.capitalize(text)

    def race(self, text):
        if not text:
            return None

        text = text.upper()

        if text in RACE_LOOKUP:
            return titlecase(RACE_LOOKUP[text])
        else:
            return titlecase(text)

    def sex(self, text):
        if not text:
            return None

        text = text.upper()

        if text in GENDER_LOOKUP:
            return titlecase(GENDER_LOOKUP[text])
        else:
            return titlecase(text)

    def number_to_string(self, value):
        ''' If it's a number, turn the passed value into a string, everything else is returned as-is.
        '''
        type_value = type(value)
        if type_value == int or type_value == float:
            return str(value)
        return value

    def string_to_integer(self, value):
        ''' Strings and floats are turned to integers, integers are returned as-is, everything else is None.
        '''
        if type(value) == str:
            try:
                value_int = int(value)
            except ValueError:
                try:
                    value_int = int(float(value))
                except ValueError:
                    value_int = None

            return value_int
        if type(value) == int:
            return value
        if type(value) == float:
            return int(value)
        return None

    def capitalize(self, value):
        def abbreviations(word, **kwargs):
            upd = word.upper()
            if upd in CAPITALIZE_LIST or upd.lstrip("(").rstrip(")") in CAPITALIZE_LIST:
                return upd

        if type(value) is not str:
            return value
        return titlecase(value.strip().lower(), callback=abbreviations)

    def capitalize_incident(self, incident):
        for key in list(incident.keys()):
            if key in CAPITALIZE_IGNORE_KEYS_LIST:
                continue

            incident[key] = self.capitalize(incident[key])

        return incident
