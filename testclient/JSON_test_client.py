import requests
import hashlib
import datetime
from dateutil.relativedelta import relativedelta
from comport.department.models import Extractor
from comport.utils import random_string, random_date
import random
import importlib

"""
HOW TO USE IN TESTS
-------------------
# import the library
from testclient.JSON_test_client import JSONTestClient

# create a test client
test_client = JSONTestClient()

# create ten rows of fake BPD-compatible Use Of Force data, with dates between Jan 1st, 2016 and August 1st, 2016
uof_data = test_client.make_uof(count=10, start_date=datetime.datetime(2016, 1, 1), end_date=datetime.datetime(2016, 8, 1), short_name="BPD")

# date range is optional, and defaults to Jan 1st 2014 - Jan 1st 2016
uof_data = test_client.make_uof(count=10, short_name="BPD")

# count defaults to 1000 and short_name defaults to "IMPD"
uof_data = test_client.make_uof()
"""

class JSONTestClient(object):

    def run(self, department, mutators=[]):
        baseurl = "http://localhost:5000/"
        password = "test"
        extractor, envs = Extractor.from_department_and_password(
            department=department, password=password)
        comport_username = extractor.username
        comport_password = password
        end_date = datetime.datetime.now()
        start_date = end_date - relativedelta(months=18)

        data = []

        # Assaults on officers mock data generation
        assaults = self.make_assaults(count=(900 + random.randint(0, 200)), start_date=start_date, end_date=end_date)

        for mutator in mutators:
            assaults = mutator.mutate(assaults)

        data.extend(assaults)

        print("* Adding {} fake assaults...".format(len(assaults)))

        for i in range(0, len(data), 100):
            chunk = data[i:i + 100]
            payload = {'data': chunk}

            url = baseurl + "data/assaults"

            print("- assaults {}-{}".format(i, i + len(chunk)))

            p = requests.post(url, auth=(comport_username,
                                         comport_password), json=payload)
            if p.status_code != 200:
                # print("error: %s" % p.text.encode("utf-8", "ignore"))
                print(p.status_code)

        data = []

        # Complaints on officers mock data generation
        complaints = self.make_complaints(count=(900 + random.randint(0, 200)), start_date=start_date, end_date=end_date)

        for mutator in mutators:
            complaints = mutator.mutate(complaints)

        data.extend(complaints)

        print("* Adding {} fake complaints...".format(len(complaints)))

        for i in range(0, len(data), 100):
            chunk = data[i:i + 100]
            payload = {'data': chunk}

            url = baseurl + "data/complaints"

            print("- complaints {}-{}".format(i, i + len(chunk)))

            p = requests.post(url, auth=(comport_username,
                                         comport_password), json=payload)
            if p.status_code != 200:
                print("error: %s" % p.text.encode("utf-8", "ignore"))

        data = []

        # Generating mock use of force data
        use_of_force_incidents = self.make_uof(count=(900 + random.randint(0, 200)), start_date=start_date, end_date=end_date)

        for mutator in mutators:
            use_of_force_incidents = mutator.mutate(use_of_force_incidents)

        data.extend(use_of_force_incidents)

        print("* Adding {} fake uof...".format(len(use_of_force_incidents)))

        for i in range(0, len(data), 100):
            chunk = data[i:i + 100]
            payload = {'data': chunk}

            url = baseurl + "data/UOF"

            print("- uof {}-{}".format(i, i + len(chunk)))

            p = requests.post(url, auth=(comport_username,
                                         comport_password), json=payload)
            if p.status_code != 200:
                print("error: %s" % p.text.encode("utf-8", "ignore"))

        data = []

        # Generating mock officer involved shooting data
        ois_incidents = self.make_ois(count=(900 + random.randint(0, 200)), start_date=start_date, end_date=end_date)

        for mutator in mutators:
            ois_incidents = mutator.mutate(ois_incidents)

        data.extend(ois_incidents)

        print("* Adding {} fake ois...".format(len(ois_incidents)))

        for i in range(0, len(data), 100):
            chunk = data[i:i + 100]
            payload = {'data': chunk}

            url = baseurl + "data/OIS"

            print("- ois {}-{}".format(i, i + len(chunk)))

            p = requests.post(url, auth=(comport_username,
                                         comport_password), json=payload)
            if p.status_code != 200:
                print("error: %s" % p.text.encode("utf-8", "ignore"))

    def hash(self, text, key="bildad"):
        ''' Return an MD5 hash of the combined text and key.
        '''
        if not text or not key:
            return ""
        m = hashlib.md5()
        m.update((str(text) + key).encode('utf-8'))
        return m.hexdigest()

    def make_complaints(self, count=1000, start_date=datetime.datetime(2014, 1, 1), end_date=datetime.datetime(2016, 1, 1), short_name="IMPD"):
        # get a reference to the incident class
        incident_class = getattr(importlib.import_module("comport.data.models"), "CitizenComplaint{}".format(short_name))
        # build a variable to csv header lookup from the csv schema
        key_list = [col[2] for col in incident_class.get_csv_schema()]

        # separate officer keys
        officer_keys = []
        incident_keys = []
        for key in key_list:
            if key.startswith("officer"):
                officer_keys.append(key)
            else:
                incident_keys.append(key)

        # make a smaller pool of officers so that it's possible to have more than one complaint per officer
        officers = []
        for x in range(0, count):
            officer = dict()
            for key in officer_keys:
                officer[key] = self.make_value(key, start_date=start_date, end_date=end_date, short_name=short_name)
            officers.append(officer)

        # build the complaints
        complaints = []
        for x in range(0, count):
            complaint = dict()
            for key in incident_keys:
                complaint[key] = self.make_value(key, start_date=start_date, end_date=end_date, short_name=short_name)
            complaint.update(random.choice(officers))
            complaints.append(complaint)

        return complaints

    def make_assaults(self, count=1000, start_date=datetime.datetime(2014, 1, 1), end_date=datetime.datetime(2016, 1, 1), short_name="IMPD"):
        # get a reference to the incident class
        incident_class = getattr(importlib.import_module("comport.data.models"), "AssaultOnOfficer{}".format(short_name))
        # build a variable to csv header lookup from the csv schema
        key_list = [col[2] for col in incident_class.get_csv_schema()]

        # separate officer keys
        officer_keys = []
        incident_keys = []
        for key in key_list:
            if key == "officerIdentifier":
                officer_keys.append(key)
            else:
                incident_keys.append(key)

        # make a smaller pool of officers so that it's possible to have more than one incident per officer
        officers = []
        for x in range(0, count):
            officer = dict()
            for key in officer_keys:
                officer[key] = self.make_value(key, start_date=start_date, end_date=end_date, short_name=short_name)
            officers.append(officer)

        # build the incidents
        incidents = []
        for x in range(0, count):
            incident = dict()
            for key in incident_keys:
                incident[key] = self.make_value(key, start_date=start_date, end_date=end_date, short_name=short_name)
            incident.update(random.choice(officers))
            incidents.append(incident)

        return incidents

    def make_uof(self, count=1000, start_date=datetime.datetime(2014, 1, 1), end_date=datetime.datetime(2016, 1, 1), short_name="IMPD"):
        # get a reference to the incident class
        incident_class = getattr(importlib.import_module("comport.data.models"), "UseOfForceIncident{}".format(short_name))
        # build a variable to csv header lookup from the csv schema
        key_list = [col[2] for col in incident_class.get_csv_schema()]

        incidents = []
        for x in range(0, count):
            incident = dict()
            for key in key_list:
                incident[key] = self.make_value(key, start_date=start_date, end_date=end_date, short_name=short_name)
            incidents.append(incident)

        return incidents

    def make_ois(self, count=1000, start_date=datetime.datetime(2014, 1, 1), end_date=datetime.datetime(2016, 1, 1), short_name="IMPD"):
        # get a reference to the incident class
        incident_class = getattr(importlib.import_module("comport.data.models"), "OfficerInvolvedShooting{}".format(short_name))
        # build a variable to csv header lookup from the csv schema
        key_list = [col[2] for col in incident_class.get_csv_schema()]

        incidents = []
        for x in range(0, count):
            incident = dict()
            for key in key_list:
                incident[key] = self.make_value(key, start_date=start_date, end_date=end_date, short_name=short_name)
            incidents.append(incident)

        return incidents

    def make_value(self, value_key, **kwargs):
        ''' make a convincing fake value for the key
        '''
        if value_key in ["arrestMade", "officerInjured", "officerKilled", "reportFiled", "residentInjured", "residentHospitalized", "officerHospitalized", "hasDisposition"]:
            return self.generate_bool()

        if value_key in ["opaqueId", "officerIdentifier", "residentIdentifier"]:
            return self.hash(random_string(10))

        if value_key in ["caseNumber"]:
            return self.generate_case_number()

        if value_key in ["officerRace", "residentRace"]:
            return self.generate_race()

        if value_key in ["officerSex", "residentSex"]:
            return self.generate_sex()

        if value_key in ["officerAge", "residentAge"]:
            return str(random.randint(23, 50))

        if value_key in ["officerCondition", "residentCondition"]:
            return self.generate_condition()

        if value_key == "officerYearsOfService":
            return str(random.randint(0, 27))

        if value_key == "serviceType":
            return self.generate_service_type()

        if value_key == "source":
            return self.generate_source()

        if value_key == "occuredDate":
            return random_date(kwargs['start_date'], kwargs['end_date']).strftime("%Y-%m-%d 0:0:00")

        if value_key == "occuredTime":
            return ""

        if value_key == "division":
            return self.generate_division(short_name=kwargs['short_name'])

        if value_key == "precinct":
            return self.generate_precinct()

        if value_key == "shift":
            return self.generate_shift()

        if value_key == "beat":
            return self.generate_beat()

        if value_key == "bureau":
            return self.generate_bureau(short_name=kwargs['short_name'])

        if value_key == "assignment":
            return self.generate_assignment()

        if value_key == "unit":
            return self.generate_unit()

        if value_key == "platoon":
            return self.generate_platoon()

        if value_key == "allegationType":
            return self.generate_allegation_type()

        if value_key == "allegation":
            return self.generate_allegation()

        if value_key == "disposition":
            return self.generate_disposition()

        if value_key == "officerForceType":
            return self.generate_officer_force_type()

        if value_key == "useOfForceReason":
            return self.generate_use_of_force_reason()

        if value_key == "arrestCharges":
            return self.generate_arrest_charges()

        if value_key == "residentWeaponUsed":
            return ""

    def generate_bool(self):
        return random.choice([True, False, None])

    def generate_case_number(self):
        return "{yr}J-{nm}".format(yr=str(random.randint(5, 20)).zfill(2), nm=str(random.randint(1, 1000)).zfill(4))

    def generate_sex(self):
        return random.choice([
            "Male",
            "Female",
            None
        ])

    def generate_race(self):
        return random.choice([
            "Black",
            "Unknown",
            "Hispanic",
            "White",
            "Bi-Racial",
            "White ",
            "Asian",
            "Other",
            None
        ])

    def generate_disposition(self):
        return random.choice(
            ["Inactivated",
             "Informational Purpose On",
             "No Violation",
             "Not Sustained",
             "Not within Policy",
             "Partially Sustained",
             "Sustained",
             "Unfounded/Exonerated",
             "Unfounded/False",
             "Unfounded/Not Involved",
             "Unfounded/Unwarranted",
             "Withdrawn",
             "Within policy",
             None
             ])

    def generate_assault_force_type(self):
        force_type = random.choice([
            'HANDS FIST FEET ETC',
            'OTHER DANGEROUS WEAPON',
            'FIREARM',
            'KNIFE OR CUTTING INSTRUMENT'
        ])
        return force_type

    def generate_assault_assignment(self):
        assignment = random.choice([
            'ONE MAN VEHICLE ASSISTED',
            'OTHER ASSISTED',
            'OTHER ALONE',
            'ONE MAN VEHICLE ALONE',
            'DETECTIVE OR SPECIAL ASSIGN ALONE',
            'TWO MAN VEHICLE',
            'DETECTIVE OR SPECIAL ASSIGN ASSISTED'
        ])
        return assignment

    def generate_assault_service_type(self):
        service_type = random.choice([
            'Handling, custody of prisoners',
            'Invest Suspicious persons or circumstances',
            'Mentally deranged',
            'All other',
            'Traffic pursuits and stops',
            'Attempting other arrests',
            'Ambush no warning',
            'Responding to Disturbance calls (man with gun etc)',
            'Civil disorder (riot, mass disobedience)',
            'Burglaries in progress or pursuing burglars',
            'Robberies in progress or pursuing robbers'
        ])
        return service_type

    def generate_allegation_type(self):
        return random.choice(
            ["Use of Force", "Violation of Any Rule", "Citizen Interaction", "Substandard Performance", "Detention/Arrest", "Vehicle Operation", "Investigative Procedures", "Conduct Unbecoming", "Search/Seizure", "Neglect of Duty", "Off-Duty Employment", "Prisoner Handling/Trans.", "Bias-Based Profiling", "Violation of Any Law", "Supv. Responsibilities", "Breach of Discipline", "Info. Security/Access", "Field Operations", "Failure to Cooperate", "Equipment and Uniforms", "Animal Incidents", "Unit or Section SOPs"]
        )

    def generate_allegation(self):
        return random.choice(
            ['Unreasonable Force (Hands, Fists, Feet)', 'Failure to obey all orders, rules, regulations, policies, and SOPs', 'Rude, discourteous, or insulting language', 'Unreasonable Force (Weapon)', 'Failure to properly investigate crash', 'No PC/suspicion for arrest/detention', 'Improper parking', 'Mistreatment of person in custody', 'Failure to request a supervisor to investigate a use of force incident', 'Aggressive or unsafe driving', 'Failure to make a report when approached by a citizen', 'Failure to conform to the department\'s rules, regulations, orders, policies, and SOPs while off duty', 'Speeding', 'Failure to take proper law enforcement action', 'Failure to provide name or badge number', 'Rude, discourteous, or insulting gesture(s)', 'Unreasonable Force (Handcuff Marks)', 'Misuse of Discretion', 'Improper warantless search', 'Illegal warrantless search', 'Act or ommission contrary to the obectives of the department', 'Improper use of weapon', 'Unreasonable Force (Less Lethal Weapon)', 'Misuse of emergency lights or siren', 'Failure to make crash report', 'Race', 'Working type of ODE prohibited by general order', 'Unreasonable search/seizure of cell phone', 'Failure to perform supervisory responsibility', 'Improper search of a member of the opposite sex', 'Improper strip search', 'Failure to secure property', 'Unreasonable Force (Other)', 'Taking official action in a personal dispute or incident involving a friend or relative while off duty', 'Failure to devote full attention to duties', 'Other moving traffic violation', 'Texting while driving', 'Failure to mark out of service at ODE location when required', 'Unauthorized dissimenation of official business, records or data of the department', 'Conduct detrimental to the efficient operation and/or general discipline of the department', 'Failure to appear for a scheduled court appearance', 'Failure to complete and incident report when necessary', 'Indecent or lewd language', 'Use of official position, badge, or credentials for personal advantage or to solicit goods, services, or gratuities.', 'Failure to improve performance', 'Theft', 'Working without an approved work permit', 'Failure to honor a subpoena for a court appearance or deposition', 'Failure to be truthful in an official report or correspondence', 'Unwarranted holding of property', 'Misuse of department or public property', 'Rude, demeaning, or affronting language', 'Submission of an inaccurate or incomplete report', 'Failure to log on duty when required', 'Rude, demeaning, or affronting gestures', 'Including false information in incident or crash report', 'Failure to truthfully answer questions specfically, directly, and narrowly', 'Violation of take-home vehicle restrictions', 'Intervening in the assigned case of another member', 'Improper weapon storage', 'Failure to take required action while off duty', 'Members shall obey all federal, state, and/or local laws.', 'Inappropriate uniform or appearance', 'Failure to submit evidence or property to property room as required', 'Unreasonable Force (Firearm)', 'Officer Involved Shooting (Animal Injured)', 'Infraction/ordinance violation', 'Failure to Release Property', 'Failure to complete required work promptly, accurately, or completely', 'Traffic stop without marked car or uniform', 'Intimidation/Improper Display of Police Authority', 'Failure to complete an incident report when necessary', 'Failure to take incident report while working ODE', 'Failure to make and turn in all reports promptly, accurately, and completely in conformity with department orders.', 'Failure to request a supervisor when a citizen desires to make a complaint', 'Indecent or lewd gestures(s)', 'Failure to perform duties which maintain satisfactory standards of efficiency/objectives of department.', 'National Origin', 'Detention/arrest in violation of Constitutional Rights.', 'Inability or unwillingness to perform assigned duties.', 'Unauthorized rider', 'Failure to properly handcuff prisoner', 'Improper posting on a social media website', 'Failure to request interpreter']
        )

    def generate_source(self):
        return random.choice(["CPCO (Formal)", "CPCO (Informal)"])

    def generate_service_type(self):
        return random.choice(
            ["Arresting", "Call for Service", "Code Inforcement",
                "Interviewing", "Restraining", "Transporting", None]
        )

    def generate_division(self, short_name="IMPD"):
        if short_name == "BPD":
            return random.choice(
                ["CID", "Patrol", "Administrative"]
            )

        if short_name == "LMPD":
            return random.choice(
                ["Training", "1st Division", "2nd Division", "3rd Division", "4th Division", "5th Division", "6th Division", "7th Division", "8th Division", "Patrol Bureau", "Special Operations"]
            )

        # IMPD
        return random.choice(
            ["Chiefs Staff Division", "Investigative Division", "Operational Bureau", "Operational Division", "Prof. Dev and Training", "Support Division"]
        )

    def generate_precinct(self):
        # IMPD
        return random.choice(
            ["Court Liaison", "Crime Prevention", "Detective Bureau", "First Precinct", "Fourth Precinct", "Logistical Support", "Second Precinct", "Special Investigations", "Special Operations", "Third Precinct", "VBLETA"]
        )

    def generate_shift(self):
        # IMPD
        return random.choice(
            ["A Shift", "Auto Theft Unit", "B Shift", "Bomb Squad", "C Shift", "C.O.P. Program", "Commanding Officer", "Computer Crimes", "Criminal Intelligence", "Day Beats", "Days Bikes", "Homicide Unit", "Instructor", "K 9 Unit", "Narcotics", "Night Beats", "Oceanfront", "Off Duty / LE", "SWAT Team", "Unknown", "Vice"]
        )

    def generate_beat(self):
        # IMPD
        return random.choice(
            ["Beat 14", "Beat 17", "Beat 19", "C.O.P.", "X20 Zone", "X21 Zone", "X22 Zone", "X23 Zone", "X24 Zone", "X25 Zone", "X26 Zone", "X27 Zone", "Days", "Evenings", "Off Duty", "Rotating", "Beat 20", "Beat 23", "X28 Zone", "X29 Zone", "Beat 15", "Beat 18", "Day Bikes", "MidNights", "Unknown"]
        )

    def generate_bureau(self, short_name="BPD"):
        if short_name == "LMPD":
            return random.choice(
                ["Administrative Bureau", "Patrol Bureau", "Support Bureau"]
            )

        # BPD
        return random.choice(
            ["Administrative", "Operational"]
        )

    def generate_assignment(self):
        # BPD
        return random.choice(
            ["Northeastern District", "Northern District", "Northwestern District", "Southeastern District", "Southwestern District", "Central District", "Eastern District", "Police Academy", "Southern District", "Western District", "Homicide Second"]
        )

    def generate_unit(self):
        # LMPD
        return random.choice(
            ["1st Division", "2nd Division", "3rd Division", "4th Division", "5th Division", "6th Division", "7th Division", "8th Division", "9th Division", "Canine Unit", "Training"]
        )

    def generate_platoon(self):
        # LMPD
        return random.choice(
            ["1st Platoon", "2nd Platoon", "3rd Platoon", "Bike Platoon", "Street Platoon 1", "Street Platoon 2", "Street Platoon 3", "Street Platoon 4", "Basic Academy"]
        )

    def generate_officer_force_type(self):
        return random.choice(
            ["Canine bite", "Hands, Fist, Feet", "Joint Manipulation", "Handcuffing",
             "", "Taser", "Body Weight Leverage", "Personal CS/OC spray", "Pepper Ball",
             "Bean Bag", "Other Impact Weapon", "Less Lethal-Taser", "Baton", "Handgun",
             "Physical-Weight Leverage", "Physical-Leg Sweep", "CS Fogger", "Less Lethal-CS/OC",
             "Physical-Kick", "Physical-Palm Strike", "Vehicle", "Less Lethal-Baton",
             "Physical-Knee Strike", "Physical-Fist Strike", "Physical-Joint/Pressure",
             "Physical-Elbow Strike", "Less Lethal-Leg Sweep", "Physical-Handcuffing",
             "Less Lethal-Bean Bag", "Physical-Take Down", "Physical-Push", "Less Lethal-Pepperball",
             "Less Lethal-Other", "Less Lethal-Burning CS", "Less Lethal-BPS Gas",
             "Less Lethal-Clearout OC", "Lethal-Handgun", None, None, None]
        )

    def generate_use_of_force_reason(self):
        return random.choice([
            "Resisting Arrest", "Fleeing",
            "Combative Suspect", "Non-Compliant",
            "Assaulting Citizen(s)", "Assaulting Officer(s)", None
        ])

    def generate_arrest_charges(self):
        return random.choice([
            "Resisting Law Enforcement (MA)", "Possession of Marijuana/Hash (MA)",
            "Criminal Mischief (MB)", "Battery (MA)",
            "Theft/Receiving Stolen Property (FD)", "Possession of Cocaine (FD)",
            "Resisting Law Enforcement (FD)", "Public Intoxication (MB)",
            "Resisting Law Enforcement (M)", "Public Intoxication",
            "Criminal Mischief (M)", "Battery (M)",
            "Domestic Battery (M)", "Disorderly Conduct",
            "Battery (F)", "Operating a Vehicle While Intoxicated (M)",
            "Criminal Trespass", "Resisting Law Enforcement (F)",
            "Immediate Detention", "Criminal Confinement",
            "Theft/Receiving Stolen Property", "Criminal Recklessness",
            "Possession of Marijuana/Hash (M)", "Robbery",
            "Possession of a Handgun (F)", "Battery by Bodily Waste",
            "Burglary", "Dealing in a Schedule or Controlled Substance",
            "Possession of Cocaine (F)", "Driving While Suspended",
            "Possession of Marijuana/Hash (F)", "Dealing in Methamphetamine",
            "Possession of Paraphernalia", "Possession of a Handgun (M)",
            "Aggravated Assault", "Domestic Battery (F)",
            "Disarming a Law Enforcement Officer", "Escape",
            "Strangulation", "Intimidation",
            "Shoplifting - Theft", "Stolen Vehicle",
            "Pointing a Firearm (F)", "Murder",
            "Operating a Vehicle with a BAC .08% to .15% (M)", "Public Indecency",
            "Possession of Controlled Substance", "Dealing Cocaine",
            "Dealing Marijuana", "Residential Entry",
            "Prostitution (M)", "Habitual Traffic Violator",
            "Operating a Vehicle with a BAC .15% or Higher (M)", "Operating a Vehicle While Intoxicated (F)",
            "Violation of Protective Order (M)", "Stalking",
            "Interfering with Reporting a Crime", "Animal Cruelty",
            "Carjacking", "Armed Robbery",
            "Mental Writ", "Leaving the Scene of a PD Crash",
            "Pointing a Firearm (M)", "Possession of Methamphetamine",
            "Criminal Mischief (F)", "Interfering with a Firefighter",
            "False Reporting", "Kidnapping",
            "Joyriding", "Ciminal Conversion",
            "Prostitution (F)", None, None, None
        ])

    def generate_condition(self):
        return random.choice([
            "No injuries noted or visible", "Canine Bite",
            "Minor Bleeding", "Laceration",
            "taser probe", "small puncture",
            "complaint of pain", "abrassion",
            "abrasion", "taser strike", "Swelling",
            "Internal Pain/Discomfort", "CSOC",
            "Abrasions", "scrapes", "unknwon",
            "difficulty breathing", "Probe strikes",
            "scratch to neck", "Bruising",
            "Prior Knee Injury", "Taser Prong entry wound", "minor scrape",
            "none apparant", "loss of skin", "Knife Wound",
            "Broken Bone", "probe strike",
            "taser prong", "tazer drive stun",
            "tazer probes", "Shoulder Pain",
            "Small cut on nose", "pepper spray",
            "redness and skin damage", "abraisons",
            "Taser prongs", "small red mark on cheek",
            "Pain to right hand", "taser probe strike",
            "Abrasion to cheek", "TASER PROBES",
            "none", "head injury", "road rash", "scratches/scrapes",
            "scratch to left cheek", "Unconsciousness",
            "shoulder pain reported later", "Small puncture from taser", "taser marks",
            "Minor Scrapes", "Major Scrapes", "TASER PRONG PUNCTURE", "probe mark", "Puncture from Tazer prong",
            "oc spray to eyes", "BLEEDING FROM PRIOR FIGHT", "oc sprayed", "none; possible minor bleedin",
            "cs spray", "REDNESS DUE TO OC/CS", "breathing complaint", "prongs from taser cartridge",
            "TASER PROBE HITS", "Soft Tissue", "busted tooth", "puncture wound/taser probe",
            "Taser Prong entry points", "unknown", "Puncture Wound From Probes", "No Injury", "Major Bleeding",
            "Chemical spray", "Small Minor Scrapes", "Broken Tooth"
        ])

    def generate_ois_resident_force_type(self):
        return random.choice(["Suspect - Handgun", "Suspect - Misc Weapon", "Suspect - Unarmed", "Suspect - Knife", "Suspect - Rifle"])

    def generate_ois_officer_force_type(self):
        return random.choice(["Duty Handgun", "IMPD - Duty Handgun", "IMPD - Shotgun", "IMPD - Patrol Rifle", "Personal Patrol Rifle", "Personal Shotgun"])

    def get_prebaked_assaults(self, first=0, last=0):
        ''' Return at most five non-random assaults '''
        if type(first) is not int:
            first = 0
        if type(last) is not int:
            last = 5
        return [
            {
                'opaqueId': '90607ab31c2114e987f7e458680a8f15',
                'officerIdentifier': '3ae9c4d0fb769fa5f295ecdad855b48b',
                'serviceType': 'Handling, Custody Of Prisoners',
                'forceType': 'Firearm',
                'assignment': 'One Man Vehical',
                'arrestMade': True,
                'officerInjured': False,
                'officerKilled': False,
                'reportFiled': False
            },
            {
                'opaqueId': '32423104dsfadf90607ab31c211',
                'officerIdentifier': '796a086d9da3d9a7eecb9289bc9e88c6',
                'serviceType': 'Mentally Deranged',
                'forceType': 'Hands Fist Feet Etc',
                'assignment': 'One Man Vehicle Assisted',
                'arrestMade': True,
                'officerInjured': True,
                'officerKilled': False,
                'reportFiled': False
            },
            {
                'opaqueId': 'ab83e472eed9f0c577bf022e28428920',
                'officerIdentifier': 'f9a4d4c2050981619f6a296b7eb73794',
                'serviceType': 'Invest Suspicious Persons Or Circumstances',
                'forceType': 'Other Dangerous Weapon',
                'assignment': 'One Alone',
                'arrestMade': False,
                'officerInjured': False,
                'officerKilled': False,
                'reportFiled': False
            },
            {
                'opaqueId': '0ab83e472eed9f0c577bf022e28428920',
                'officerIdentifier': 'd0318d57ca5ff55d27ff7cfb4575cd0b',
                'serviceType': 'Traffic Pursuits And Stops',
                'forceType': 'Hands Fist Feet Etc',
                'assignment': 'One Man Vehicle Assisted',
                'arrestMade': True,
                'officerInjured': False,
                'officerKilled': False,
                'reportFiled': True
            },
            {
                'opaqueId': '950919eb39e0172d0029feb2db469d23',
                'officerIdentifier': '5182b3dd18fa4e745678a2f529bf62c8',
                'serviceType': 'Ambush No Warning',
                'forceType': 'Other Dangerous Weapon',
                'assignment': 'One Man Vehicle',
                'arrestMade': False,
                'officerInjured': False,
                'officerKilled': False,
                'reportFiled': False
            }
        ][first:last]

    def get_prebaked_complaints(self, first=0, last=5):
        ''' Return at most five non-random complaints.
        '''
        if type(first) is not int:
            first = 0
        if type(last) is not int:
            last = 5
        return [{'opaqueId': 'd716e65e8efa304d7b80a36bbd55f664', 'officerRace': 'Other', 'shift': 'Auto Theft Unit', 'officerIdentifier': '90607ab31c2114e987f7e458680a8f15', 'occuredDate': '2014-08-20 0:0:00', 'officerAge': '32', 'precinct': 'Detective Bureau', 'officerSex': None, 'serviceType': None, 'division': 'Investigative Division', 'allegation': None, 'officerYearsOfService': '4', 'residentSex': 'Female', 'beat': 'Rotating', 'allegationType': None, 'residentAge': '56', 'source': 'CPCO (Informal)', 'residentRace': 'Black', 'disposition': 'Within policy'}, {'opaqueId': 'b078aa4a6c2b2c40febc1841e9e3fdf0', 'officerRace': 'Bi-Racial', 'shift': 'Day Beats', 'officerIdentifier': 'a6bc45622d6686b8d107a3b5663c426c', 'occuredDate': '2014-11-19 0:0:00', 'officerAge': '34', 'precinct': 'Second Precinct', 'officerSex': 'Male', 'serviceType': 'Code Inforcement', 'division': 'Operational Division', 'allegation': '', 'officerYearsOfService': '9', 'residentSex': 'Male', 'beat': 'Beat 20', 'allegationType': 'Neglect of Duty', 'residentAge': '36', 'source': 'CPCO (Formal)', 'residentRace': 'Hispanic', 'disposition': 'Unfounded/False'}, {'opaqueId': '950919eb39e0172d0029feb2db469d23', 'officerRace': None, 'shift': 'Auto Theft Unit', 'officerIdentifier': '6a98e68a80c7d07e17b15541d030769c', 'occuredDate': '2015-06-01 0:0:00', 'officerAge': '50', 'precinct': 'Detective Bureau', 'officerSex': 'Female', 'serviceType': 'Interviewing', 'division': 'Investigative Division', 'allegation': 'Failure to complete an incident report when necessary', 'officerYearsOfService': '27', 'residentSex': 'Male', 'beat': 'Rotating', 'allegationType': 'Citizen Interaction', 'residentAge': '51', 'source': 'CPCO (Informal)', 'residentRace': None, 'disposition': 'Not within Policy'}, {'opaqueId': '6155d7bdd819fa0a9c987a7f31fe03b4', 'officerRace': 'Black', 'shift': 'A Shift', 'officerIdentifier': 'ab83e472eed9f0c577bf022e28428920', 'occuredDate': '2014-01-17 0:0:00', 'officerAge': '47', 'precinct': 'First Precinct', 'officerSex': 'Male', 'serviceType': 'Interviewing', 'division': 'Operational Division', 'allegation': 'Taking official action in a personal dispute or incident involving a frilast or relative while off duty', 'officerYearsOfService': '18', 'residentSex': None, 'beat': 'X24 Zone', 'allegationType': 'Breach of Discipline', 'residentAge': '26', 'source': 'CPCO (Formal)', 'residentRace': 'White', 'disposition': None}, {'opaqueId': '6f334db17957ed14a8c72f982e2320c6', 'officerRace': 'Hispanic', 'shift': 'B Shift', 'officerIdentifier': 'b73d8ef8e3d890b8bea93eb0ddd7fb46', 'occuredDate': '2014-05-07 0:0:00', 'officerAge': '47', 'precinct': 'Crime Prevention', 'officerSex': None, 'serviceType': 'Interviewing', 'division': 'Operational Division', 'allegation': 'Mistreatment of person in custody', 'officerYearsOfService': '5', 'residentSex': None, 'beat': 'X27 Zone', 'allegationType': 'Use of Force', 'residentAge': '16', 'source': 'CPCO (Formal)', 'residentRace': 'Bi-Racial', 'disposition': 'Sustained'}][first:last]

    def get_prebaked_uof(self, first=0, last=5):
        ''' Return at most five non-random uof incidents.
        '''
        if type(first) is not int:
            first = 0
        if type(last) is not int:
            last = 5
        return [{'opaqueId': 'e61040650aeab567fa2ec83a89e8ff4a', 'officerAge': '50', 'residentHospitalized': False, 'precinct': None, 'useOfForceReason': 'Assaulting Citizen(s)', 'officerSex': 'Male', 'residentAge': '40', 'division': None, 'officerCondition': 'abraisons', 'officerYearsOfService': '27', 'residentWeaponUsed': 'Suspect - Unarmed', 'residentSex': 'Male', 'residentRace': 'Bi-Racial', 'occuredTime': '', 'residentCondition': 'redness and skin damage', 'residentInjured': None, 'officerRace': 'White ', 'shift': None, 'occuredDate': '2015-06-26 0:0:00', 'officerForceType': 'Body Weight Leverage', 'beat': None, 'serviceType': None, 'arrestMade': True, 'arrestCharges': 'Possession of Controlled Substance', 'officerInjured': None, 'officerIdentifier': 'a571abbed982bb06432c995d4095ed23', 'officerHospitalized': None, 'disposition': 'Unfounded/Exonerated'}, {'opaqueId': '66869c0f93eb973ac3a466130b344e1b', 'officerAge': '30', 'residentHospitalized': None, 'precinct': 'First Precinct', 'useOfForceReason': 'Combative Suspect', 'officerSex': 'Female', 'residentAge': '59', 'division': 'Operational Division', 'officerCondition': 'minor scrape', 'officerYearsOfService': '8', 'residentWeaponUsed': '', 'residentSex': 'Female', 'residentRace': 'Hispanic', 'occuredTime': '', 'residentCondition': 'head injury', 'residentInjured': True, 'officerRace': None, 'shift': 'A Shift', 'occuredDate': '2014-10-19 0:0:00', 'officerForceType': 'Personal CS/OC spray', 'beat': 'X20 Zone', 'serviceType': 'Arresting', 'arrestMade': False, 'arrestCharges': None, 'officerInjured': True, 'officerIdentifier': '88e632a5983b08d9ae472cf494349b53', 'officerHospitalized': True, 'disposition': 'Not Sustained'}, {'opaqueId': '51a82ea9f6365b5bf26521390fb62b24', 'officerAge': '31', 'residentHospitalized': True, 'precinct': 'First Precinct', 'useOfForceReason': None, 'officerSex': None, 'residentAge': '28', 'division': 'Operational Bureau', 'officerCondition': 'Unconsciousness', 'officerYearsOfService': '19', 'residentWeaponUsed': '', 'residentSex': 'Female', 'residentRace': 'White', 'occuredTime': '', 'residentCondition': 'complaint of pain', 'residentInjured': False, 'officerRace': 'Other', 'shift': 'C Shift', 'occuredDate': '2015-03-20 0:0:00', 'officerForceType': 'Physical-Joint/Pressure', 'beat': 'X25 Zone', 'serviceType': 'Interviewing', 'arrestMade': True, 'arrestCharges': 'Residential Entry', 'officerInjured': True, 'officerIdentifier': 'd049665fe632ae94dfb2253601e681ef', 'officerHospitalized': None, 'disposition': 'Sustained'}, {'opaqueId': '369e13f2efc0af97e3a57efc42c75480', 'officerAge': '29', 'residentHospitalized': False, 'precinct': 'Third Precinct', 'useOfForceReason': 'Fleeing', 'officerSex': 'Male', 'residentAge': '58', 'division': 'Operational Division', 'officerCondition': 'TASER PROBE HITS', 'officerYearsOfService': '25', 'residentWeaponUsed': '', 'residentSex': None, 'residentRace': 'Hispanic', 'occuredTime': '', 'residentCondition': 'complaint of pain', 'residentInjured': None, 'officerRace': None, 'shift': 'B Shift', 'occuredDate': '2014-05-01 0:0:00', 'officerForceType': 'Personal CS/OC spray', 'beat': 'X24 Zone', 'serviceType': 'Transporting', 'arrestMade': None, 'arrestCharges': 'Public Indecency', 'officerInjured': True, 'officerIdentifier': 'bf9304c06e6fa120aacad084a7db78f2', 'officerHospitalized': True, 'disposition': 'Within policy'}, {'opaqueId': 'a6d732ffd6130bc78dd7dd6376d23df1', 'officerAge': '45', 'residentHospitalized': None, 'precinct': 'Detective Bureau', 'useOfForceReason': None, 'officerSex': 'Female', 'residentAge': '55', 'division': 'Investigative Division', 'officerCondition': 'Small puncture from taser', 'officerYearsOfService': '25', 'residentWeaponUsed': '', 'residentSex': 'Female', 'residentRace': 'Hispanic', 'occuredTime': '', 'residentCondition': 'Taser prongs', 'residentInjured': False, 'officerRace': 'Asian', 'shift': 'Auto Theft Unit', 'occuredDate': '2014-07-22 0:0:00', 'officerForceType': 'Handgun', 'beat': 'Off Duty', 'serviceType': 'Transporting', 'arrestMade': False, 'arrestCharges': 'Public Intoxication (MB)', 'officerInjured': False, 'officerIdentifier': '981caf4ff6a430a44e6c0c957b31f281', 'officerHospitalized': False, 'disposition': 'Unfounded/Not Involved'}][first:last]

    def get_prebaked_ois(self, first=0, last=5):
        ''' Return at most five non-random ois incidents.
        '''
        if type(first) is not int:
            first = 0
        if type(last) is not int:
            last = 5
        return [{'opaqueId': 'f732197d9f28d25396873573e7067629', 'officerRace': 'White', 'shift': 'Auto Theft Unit', 'occuredDate': '2015-08-09 0:0:00', 'residentCondition': 'Puncture from Tazer prong', 'officerForceType': 'Duty Handgun', 'precinct': 'Detective Bureau', 'officerSex': 'Female', 'serviceType': 'Transporting', 'division': 'Investigative Division', 'officerAge': '36', 'officerCondition': 'pepper spray', 'officerYearsOfService': 27, 'residentWeaponUsed': 'Suspect - Unarmed', 'beat': 'Evenings', 'residentSex': 'Male', 'residentAge': '26', 'officerIdentifier': '5182b3dd18fa4e745678a2f529bf62c7', 'residentRace': None, 'occuredTime': '', 'disposition': 'Sustained'}, {'opaqueId': '9bc285abcf5741d826387ecb994a62d0', 'officerRace': 'Asian', 'shift': 'C Shift', 'occuredDate': '2015-03-30 0:0:00', 'residentCondition': 'BLEEDING FROM PRIOR FIGHT', 'officerForceType': 'Duty Handgun', 'precinct': 'First Precinct', 'officerSex': 'Male', 'serviceType': None, 'division': 'Operational Bureau', 'officerAge': '32', 'officerCondition': 'oc sprayed', 'officerYearsOfService': 13, 'residentWeaponUsed': 'Suspect - Handgun', 'beat': 'X25 Zone', 'residentSex': None, 'residentAge': '24', 'officerIdentifier': 'd0318d57ca5ff55d27ff7cfb4575cd0a', 'residentRace': 'Asian', 'occuredTime': '', 'disposition': 'Inactivated'}, {'opaqueId': '665db18373624c41d004ea5c4e3df8f9', 'officerRace': 'White', 'shift': 'A Shift', 'occuredDate': '2015-02-20 0:0:00', 'residentCondition': 'Taser Prong entry points', 'officerForceType': 'Duty Handgun', 'precinct': 'Second Precinct', 'officerSex': 'Male', 'serviceType': 'Code Inforcement', 'division': 'Operational Division', 'officerAge': '49', 'officerCondition': 'Major Scrapes', 'officerYearsOfService': 25, 'residentWeaponUsed': 'Suspect - Knife', 'beat': 'Beat 17', 'residentSex': 'Male', 'residentAge': '19', 'officerIdentifier': 'f9a4d4c2050981619f6a296b7eb73793', 'residentRace': None, 'occuredTime': '', 'disposition': 'Unfounded/Unwarranted'}, {'opaqueId': 'e14b23c8b5a1d03901291061b611b62e', 'officerRace': 'Unknown', 'shift': 'A Shift', 'occuredDate': '2014-06-07 0:0:00', 'residentCondition': 'abrassion', 'officerForceType': 'IMPD - Shotgun', 'precinct': 'Fourth Precinct', 'officerSex': None, 'serviceType': 'Code Inforcement', 'division': 'Operational Division', 'officerAge': '42', 'officerCondition': 'Shoulder Pain', 'officerYearsOfService': 1, 'residentWeaponUsed': 'Suspect - Misc Weapon', 'beat': 'X24 Zone', 'residentSex': 'Female', 'residentAge': '46', 'officerIdentifier': '796a086d9da3d9a7eecb9289bc9e88c5', 'residentRace': 'Black', 'occuredTime': '', 'disposition': 'Informational Purpose On'}, {'opaqueId': 'b77f4e3b867fa02078acb95aff11001b', 'officerRace': None, 'shift': 'A Shift', 'occuredDate': '2015-02-15 0:0:00', 'residentCondition': 'Swelling', 'officerForceType': 'IMPD - Duty Handgun', 'precinct': 'First Precinct', 'officerSex': None, 'serviceType': 'Arresting', 'division': 'Operational Division', 'officerAge': '47', 'officerCondition': 'prongs from taser cartridge', 'officerYearsOfService': 15, 'residentWeaponUsed': 'Suspect - Rifle', 'beat': 'X20 Zone', 'residentSex': None, 'residentAge': '22', 'officerIdentifier': '3ae9c4d0fb769fa5f295ecdad855b48a', 'residentRace': 'White ', 'occuredTime': '', 'disposition': 'Partially Sustained'}][first:last]
