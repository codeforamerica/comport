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

SEX_LOOKUP = {
    "F": "Female",
    "M": "Male"
}

CAPITALIZE_LIST = [
    "NW",
    "SE",
    "ED",
    "DT",
    "FTO",
    "ND",
    "SW",
    "DWI",
    "VBLETA",
    "ODE",
    "PC"
]

CAPITALIZE_IGNORE_LIST = [
    "opaqueId",
    "officerYearsOfService"
]

class Cleaners:

    def resident_weapon_used(val):
        if val in RESIDENT_WEAPONS_LOOKUP:
            return RESIDENT_WEAPONS_LOOKUP[val]
        else:
            return val

    def officer_force_type(text):
        if text is not None and text in OFFICER_FORCE_TYPE_LOOKUP:
            return OFFICER_FORCE_TYPE_LOOKUP[text]
        return text

    def race(text):
        if not text:
            return None

        text = text.upper()

        if text in RACE_LOOKUP:
            return titlecase(RACE_LOOKUP[text])
        else:
            return titlecase(text)

    def sex(text):
        if not text:
            return None

        text = text.upper()

        if text in SEX_LOOKUP:
            return titlecase(SEX_LOOKUP[text])
        else:
            return titlecase(text)

    def capitalize(value):
        def abbreviations(word, **kwargs):
            if word.upper() in CAPITALIZE_LIST:
                return word.upper()

        if value is None or isinstance(value, list):
            return value
        return titlecase(value.strip().lower(), callback=abbreviations)

    def capitalize_incident(incident):
        for key in list(incident.keys()):
            if key in CAPITALIZE_IGNORE_LIST:
                continue

            incident[key] = Cleaners.capitalize(incident[key])

        return incident
