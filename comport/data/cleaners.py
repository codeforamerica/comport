from titlecase import titlecase

class Cleaners:
    def resident_weapon_used(val):
        weapons_used = {
            "Suspect - Handgun": "Handgun",
            "Suspect - Knife" : "Knife",
            "Suspect - Misc Weapon": "Misc Weapon",
            "Suspect - Rifle" : "Rifle",
            "Suspect - Unarmed": "Unarmed"
        }

        if val in weapons_used:
            return weapons_used[val]
        else:
            return val

    def officer_force_type(text):
        prefix_map = {
            "Baton":"Less Lethal-Baton",
            "Bean Bag":"Less Lethal-Bean Bag",
            "Body Weight Leverage":"Physical-Weight Leverage",
            "Canine bite":"Canine Bite",
            "CS Fogger":"Less Lethal-CS/OC",
            "Handcuffing":"Physical-Handcuffing",
            "Handgun":"Lethal-Handgun",
            "Hands, Fist, Feet":"Physical-Hands, Fist, Feet",
            "Joint Manipulation":"Physical-Joint/Pressure",
            "Less Lethal-Leg Sweep":"Physical-Leg Sweep",
            "Other Impact Weapon":"Less Lethal-Other",
            "Pepper Ball":"Less Lethal-Pepperball",
            "Personal CS/OC spray":"Less Lethal-Personal CS/OC spray",
            "Taser":"Less Lethal-Taser",
            "Vehicle":"Lethal-Vehicle"
        }
        if text is not None and text in prefix_map:
            return prefix_map[text]
        return text

    def race(text):
        race_map = {
            "B": "Black"
        }

        if not text:
            return None

        text = text.upper()

        if text in race_map:
            return titlecase(race_map[text])
        else:
            return titlecase(text)

    def sex(text):
        sex_map = {
            "F": "Female",
            "M": "Male"
        }

        if not text:
            return None

        text = text.upper()

        if text in sex_map:
            return titlecase(sex_map[text])
        else:
            return titlecase(text)



    def capitalize(value):
        def abbreviations(word, **kwargs):
           if word.upper() in ('NW', 'SE', 'ED', 'DT', 'FTO', 'ND', 'SW', "DWI", "VBLETA", "ODE", "PC"):
             return word.upper()

        if value is None or isinstance(value, list):
            return value
        return titlecase(value.strip().lower(), callback=abbreviations)

    def capitalize_incident(incident):
        keys_to_ignore = ["opaqueId", "officerYearsOfService"]

        for key in list(incident.keys()):
            if key in keys_to_ignore:
                continue

            incident[key] = Cleaners.capitalize(incident[key])

        return incident
