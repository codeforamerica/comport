import random
import math
from datetime import datetime, timedelta
from comport.utils import random_string, random_date

class MissingDataMutator:
    do_not_mutate = ['opaqueId']

    def __init__(self, percent=1):
        self.percent = percent

    def drop_data(self, incident):
        for x in range(0, math.floor(len(incident) * self.percent)):
            field_to_drop = random.choice(list(incident.keys()))
            if field_to_drop not in self.do_not_mutate:
                incident[field_to_drop] = None
        return incident

    def mutate(self, incidents):
        return list(map(self.drop_data,incidents))

class EmptyDataMutator:
    do_not_mutate = ['opaqueId']

    def __init__(self, percent=1):
        self.percent = percent

    def drop_data(self, incident):
        for x in range(0, math.floor(len(incident) * self.percent)):
            field_to_drop = random.choice(list(incident.keys()))
            if field_to_drop not in self.do_not_mutate:
                incident[field_to_drop] = random.choice(["", " "])
        return incident

    def mutate(self, incidents):
        return list(map(self.drop_data,incidents))

class FuzzedDataMutator:
    do_not_mutate = ['opaqueId','occuredDate']

    def __init__(self, percent=1):
        self.percent = percent

    def alter_data(self, incident):
        for x in range(0, math.floor(len(incident) * self.percent)):
            field_to_drop = random.choice(list(incident.keys()))
            if field_to_drop not in self.do_not_mutate:
                incident[field_to_drop] = random_string(random.randint(0, 140))
        return incident

    def mutate(self, incidents):
        return list(map(self.alter_data,incidents))

class KnownBadDataMutator:
    def alter_data(self, incident):
        incident["officerRace"] = random.choice(["b", "B"])
        incident["residentRace"] = random.choice(["b", "B"])
        incident["residentSex"] = random.choice(["m", "M", "f", "F"])
        incident["officerSex"] = random.choice(["m", "M", "f", "F"])
        incident["division"] = random.choice(["OPERATIONS DIVISION", "HOMELAND SECURITY DIVISION", ])
        incident["precinct"] = random.choice(["HOMELAND SECURITY BUREAU/TRAFFIC", "NORTH DISTRICT", "NORTHWEST DISTRICT"])
        incident["shift"] = random.choice(["Dt Day Shift", "SW Day Shift", "HUMAN TRAFFICKING", "DT LATE TACT FOOT AND BICYCLE", "NW Middle Shift", "Ed Late Tactical Shift","NW DETECTIVE SECTION","Fto Section"])
        incident["beat"] = random.choice(["NW Day Shift 2Nd RC", "Ed Narcotics Unit","9TH RECRUIT CLASS","WEST DAY TACT NARCOTICS","SE Day Shift"])
        return incident

    def mutate(self, incidents):
        return list(map(self.alter_data,incidents))

class CasingMutator:
    do_not_mutate = ['opaqueId','occuredDate','officerYearsOfService']

    def __init__(self, percent=1):
        self.percent = percent

    def alter_data(self, incident):
        for x in range(0, math.floor(len(incident) * self.percent)):
            field_to_drop = random.choice(list(incident.keys()))
            if field_to_drop not in self.do_not_mutate and incident[field_to_drop] is not None:
                incident[field_to_drop] = ''.join(random.choice((str.upper,str.lower))(x) for x in incident[field_to_drop] )
        return incident

    def mutate(self, incidents):
        return list(map(self.alter_data,incidents))

class CondenisngDateMutator:

    def alter_data(self, incident):
        incident["occuredDate"] = random_date(datetime.now() - timedelta(weeks=52), datetime.now() - timedelta(weeks=26)).strftime("%Y-%m-%d 0:0:00")

        return incident

    def mutate(self, incidents):
        return list(map(self.alter_data,incidents))

class GapDateMutator:

    def alter_data(self, incident):
        if (random.random() > 1/12):
            incident["occuredDate"] = random_date(datetime.now() - timedelta(weeks=52), datetime.now() - timedelta(weeks=26)).strftime("%Y-%m-%d 0:0:00")
        else:
            incident["occuredDate"] = random_date(datetime.now() - timedelta(weeks=1), datetime.now()).strftime("%Y-%m-%d 0:0:00")
        return incident

    def mutate(self, incidents):
        return list(map(self.alter_data,incidents))
