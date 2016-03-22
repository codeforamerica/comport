import csv
import requests
import json
import hashlib
import glob
from titlecase import titlecase
from datetime import datetime
from comport.department.models import Extractor
from comport.utils import random_string, random_date
import random


class JSONTestClient(object):

    def run(self, department, mutators=[]):
        baseurl = "http://localhost:5000/"
        password = "test"
        extractor, envs = Extractor.from_department_and_password(
            department=department, password=password)
        comport_username = extractor.username
        comport_password = password

        data = []

        complaints = self.make_complaints()

        for mutator in mutators:
            complaints = mutator.mutate(complaints)

        data.extend(complaints)

        for i in range(0, len(data), 100):
            chunk = data[i:i + 100]
            payload = {'data': chunk}

            url = baseurl + "data/complaints"

            print(payload)

            p = requests.post(url, auth=(comport_username,
                                         comport_password), json=payload)
            if p.status_code != 200:
                print("error: %s" % p.text.encode("utf-8", "ignore"))

        data = []

        use_of_force_incidents = self.make_uof()

        for mutator in mutators:
            use_of_force_incidents = mutator.mutate(use_of_force_incidents)

        data.extend(use_of_force_incidents)

        for i in range(0, len(data), 100):
            chunk = data[i:i + 100]
            payload = {'data': chunk}

            url = baseurl + "data/UOF"

            print(payload)

            p = requests.post(url, auth=(comport_username,
                                         comport_password), json=payload)
            if p.status_code != 200:
                print("error: %s" % p.text.encode("utf-8", "ignore"))

        data = []

        ois_incidents = self.make_ois()

        for mutator in mutators:
            ois_incidents = mutator.mutate(ois_incidents)

        data.extend(ois_incidents)

        for i in range(0, len(data), 100):
            chunk = data[i:i + 100]
            payload = {'data': chunk}

            url = baseurl + "data/OIS"

            print(payload)

            p = requests.post(url, auth=(comport_username,
                                         comport_password), json=payload)
            if p.status_code != 200:
                print("error: %s" % p.text.encode("utf-8", "ignore"))

    def make_complaints(self, count=1000):
        complaints = []
        for x in range(0, count):
            assignment = self.generate_assignment()
            allegation = self.generate_allegation()
            complaints.append({
                "opaqueId": random_string(10),
                "serviceType": self.generate_service_type(),
                "source": self.generate_source(),
                "occuredDate": random_date(datetime(2014, 1, 1), datetime(2016, 1, 1)).strftime("%Y-%m-%d 0:0:00"),
                "division": assignment[0],
                "precinct": assignment[1],
                "shift": assignment[2],
                "beat": assignment[3],
                "allegationType": allegation[0],
                "allegation": allegation[1],
                "disposition": self.generate_disposition(),
                "residentRace": self.generate_race(),
                "residentSex": self.generate_sex(),
                "residentAge": str(random.randint(15, 70)),
                "officerIdentifier": random_string(10),
                "officerRace": self.generate_race(),
                "officerSex": self.generate_sex(),
                "officerAge": str(random.randint(23, 50)),
                "officerYearsOfService": random.randint(0, 27)
            })

        return complaints

    def make_uof(self, count=1000):
        incidents = []
        for x in range(0, count):
            assignment = self.generate_assignment()
            incidents.append({
                "opaqueId": random_string(10),
                "occuredDate": random_date(datetime(2014, 1, 1), datetime(2016, 1, 1)).strftime("%Y-%m-%d 0:0:00"),
                "occuredTime": "",
                "division": assignment[0],
                "precinct": assignment[1],
                "shift": assignment[2],
                "beat": assignment[3],
                "disposition": self.generate_disposition(),
                "officerForceType": self.generate_officer_force_type(),
                "useOfForceReason": self.generate_use_of_force_reason(),
                "serviceType": self.generate_service_type(),
                "arrestMade": self.generate_bool(),
                "arrestCharges": self.generate_arrest_charges(),
                "residentWeaponUsed": "",
                "residentInjured": self.generate_bool(),
                "residentHospitalized": self.generate_bool(),
                "officerInjured": self.generate_bool(),
                "officerHospitalized": self.generate_bool(),
                "residentRace": self.generate_race(),
                "residentSex": self.generate_sex(),
                "residentAge": str(random.randint(15, 70)),
                "residentCondition": self.generate_condition(),
                "officerIdentifier": random_string(10),
                "officerRace": self.generate_race(),
                "officerSex": self.generate_sex(),
                "officerAge": str(random.randint(23, 50)),
                "officerYearsOfService": random.randint(0, 27),
                "officerCondition": self.generate_condition()
            })

        return incidents

    def make_ois(self, count=1000):
        incidents = []
        for x in range(0, count):
            assignment = self.generate_assignment()
            incidents.append({
                "opaqueId": random_string(10),
                "serviceType": self.generate_service_type(),
                "occuredDate": random_date(datetime(2014, 1, 1), datetime(2016, 1, 1)).strftime("%Y-%m-%d 0:0:00"),
                "occuredTime": "",
                "division": assignment[0],
                "precinct": assignment[1],
                "shift": assignment[2],
                "beat": assignment[3],
                "disposition": self.generate_disposition(),
                "residentRace": self.generate_race(),
                "residentSex": self.generate_sex(),
                "residentAge": str(random.randint(15, 70)),
                "residentWeaponUsed": self.generate_ois_resident_force_type(),
                "residentCondition": self.generate_condition(),
                "officerIdentifier": random_string(10),
                "officerForceType": self.generate_ois_officer_force_type(),
                "officerRace": self.generate_race(),
                "officerSex": self.generate_sex(),
                "officerAge": str(random.randint(23, 50)),
                "officerYearsOfService": random.randint(0, 27),
                "officerCondition": self.generate_condition()
            })

        return incidents

    def generate_bool(self):
        return random.choice([True, False, None])

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

    def generate_allegation(self):
        return random.choice([
            ['Use of Force', 'Unreasonable Force (Hands, Fists, Feet)'],
            ['Violation of Any Rule',
             'Failure to obey all orders, rules, regulations, policies, and SOPs'],
            ['Citizen Interaction', 'Rude, discourteous, or insulting language'],
            ['Use of Force', 'Unreasonable Force (Weapon)'],
            ['Substandard Performance', 'Failure to properly investigate crash'],
            ['Detention/Arrest', 'No PC/suspicion for arrest/detention'],
            ['Vehicle Operation', 'Improper parking'],
            ['Use of Force', 'Mistreatment of person in custody'],
            ['Investigative Procedures', ''],
            ['Conduct Unbecoming', ''],
            ['Search/Seizure', ''],
            ['Substandard Performance', ''],
            ['Violation of Any Rule', ''],
            ['Neglect of Duty',
                'Failure to request a supervisor to investigate a use of force incident'],
            ['Vehicle Operation', 'Aggressive or unsafe driving'],
            ['Vehicle Operation', ''],
            ['Citizen Interaction',
                'Failure to make a report when approached by a citizen'],
            ['Violation of Any Rule', 'Failure to conform to the department\'s rules, regulations, orders, policies, and SOPs while off duty'],
            ['Vehicle Operation', 'Speeding'],
            ['Neglect of Duty', 'Failure to take proper law enforcement action'],
            ['Citizen Interaction', 'Failure to provide name or badge number'],
            ['Citizen Interaction',
                'Rude, discourteous, or insulting gesture(s)'],
            ['Off-Duty Employment', ''],
            ['Use of Force', 'Unreasonable Force (Handcuff Marks)'],
            ['Neglect of Duty', 'Misuse of Discretion'],
            ['Search/Seizure', 'Improper warantless search'],
            ['Search/Seizure', 'Illegal warrantless search'],
            ['Substandard Performance',
                'Act or ommission contrary to the obectives of the department'],
            ['Use of Force', 'Improper use of weapon'],
            ['Use of Force', 'Unreasonable Force (Less Lethal Weapon)'],
            ['Prisoner Handling/Trans.', 'Mistreatment of person in custody'],
            ['Vehicle Operation', 'Misuse of emergency lights or siren'],
            ['Citizen Interaction', 'Failure to make crash report'],
            ['Bias-Based Profiling', 'Race'],
            ['Violation of Any Law', ''],
            ['Off-Duty Employment', 'Working type of ODE prohibited by general order'],
            ['Search/Seizure', 'Unreasonable search/seizure of cell phone'],
            ['Supv. Responsibilities', 'Failure to perform supervisory responsibility'],
            ['Search/Seizure', 'Improper search of a member of the opposite sex'],
            ['Search/Seizure', 'Improper strip search'],
            ['Neglect of Duty', ''],
            ['Neglect of Duty', 'Failure to secure property'],
            ['Use of Force', 'Unreasonable Force (Other)'],
            ['Breach of Discipline', 'Taking official action in a personal dispute or incident involving a friend or relative while off duty'],
            ['Neglect of Duty', 'Failure to devote full attention to duties'],
            ['Vehicle Operation', 'Other moving traffic violation'],
            ['Vehicle Operation', 'Texting while driving'],
            ['Off-Duty Employment',
                'Failure to mark out of service at ODE location when required'],
            ['Info. Security/Access',
             'Unauthorized dissimenation of official business, records or data of the department'],
            ['Detention/Arrest', ''],
            ['Breach of Discipline',
             'Conduct detrimental to the efficient operation and/or general discipline of the department'],
            ['Neglect of Duty', 'Failure to appear for a scheduled court appearance'],
            ['Investigative Procedures',
                'Failure to complete and incident report when necessary'],
            ['Neglect of Duty', 'Failure to complete and incident report when necessary'],
            ['Field Operations', ''],
            ['Citizen Interaction', 'Indecent or lewd language'],
            ['Conduct Unbecoming', 'Use of official position, badge, or credentials for personal advantage or to solicit goods, services, or gratuities.'],
            ['Breach of Discipline', 'Failure to improve performance'],
            ['Violation of Any Law', 'Theft'],
            ['Off-Duty Employment', 'Working without an approved work permit'],
            ['Neglect of Duty',
                'Failure to honor a subpoena for a court appearance or deposition'],
            ['Failure to Cooperate',
                'Failure to be truthful in an official report or correspondence'],
            ['Neglect of Duty', 'Unwarranted holding of property'],
            ['Substandard Performance', 'Misuse of department or public property'],
            ['Substandard Performance',
                'Failure to complete and incident report when necessary'],
            ['Citizen Interaction', 'Rude, demeaning, or affronting language'],
            ['Substandard Performance',
                'Submission of an inaccurate or incomplete report'],
            ['Off-Duty Employment', 'Failure to log on duty when required'],
            ['Citizen Interaction', 'Rude, demeaning, or affronting gestures'],
            ['Investigative Procedures',
                'Including false information in incident or crash report'],
            ['Failure to Cooperate',
             'Failure to truthfully answer questions specfically, directly, and narrowly'],
            ['Vehicle Operation', 'Violation of take-home vehicle restrictions'],
            ['Substandard Performance',
             'Conduct detrimental to the efficient operation and/or general discipline of the department'],
            ['Conduct Unbecoming', 'Intervening in the assigned case of another member'],
            ['Failure to Cooperate',
                'Including false information in incident or crash report'],
            ['Equipment and Uniforms', 'Improper weapon storage'],
            ['Neglect of Duty', 'Failure to take required action while off duty'],
            ['Violation of Any Law',
                'Members shall obey all federal, state, and/or local laws.'],
            ['Vehicle Operation', 'Inappropriate uniform or appearance'],
            ['Substandard Performance',
             'Failure to submit evidence or property to property room as required'],
            ['Use of Force', 'Unreasonable Force (Firearm)'],
            ['Animal Incidents', 'Unreasonable Force (Firearm)'],
            ['Animal Incidents', 'Officer Involved Shooting (Animal Injured)'],
            ['Conduct Unbecoming', 'Rude, demeaning, or affronting language'],
            ['Substandard Performance', 'No PC/suspicion for arrest/detention'],
            ['Investigative Procedures',
                'Submission of an inaccurate or incomplete report'],
            ['Violation of Any Law', 'Infraction/ordinance violation'],
            ['Citizen Interaction', 'Unreasonable Force (Firearm)'],
            ['Search/Seizure', 'Unwarranted holding of property'],
            ['Citizen Interaction', 'Failure to Release Property'],
            ['Substandard Performance',
             'Failure to complete required work promptly, accurately, or completely'],
            ['Citizen Interaction', 'Traffic stop without marked car or uniform'],
            ['Neglect of Duty',
                'Failure to complete required work promptly, accurately, or completely'],
            ['Conduct Unbecoming', 'Intimidation/Improper Display of Police Authority'],
            ['Neglect of Duty', 'Failure to complete an incident report when necessary'],
            ['Citizen Interaction',
                'Failure to complete an incident report when necessary'],
            ['Substandard Performance', 'Failure to take proper law enforcement action'],
            ['Off-Duty Employment', 'Failure to take incident report while working ODE'],
            ['Neglect of Duty', 'Failure to make and turn in all reports promptly, accurately, and completely in conformity with department orders.'],
            ['Citizen Interaction',
             'Failure to request a supervisor when a citizen desires to make a complaint'],
            ['Citizen Interaction', 'Indecent or lewd gestures(s)'],
            ['Substandard Performance',
             'Failure to perform duties which maintain satisfactory standards of efficiency/objectives of department.'],
            ['Bias-Based Profiling', 'National Origin'],
            ['Detention/Arrest', 'Detention/arrest in violation of Constitutional Rights.'],
            ['Citizen Interaction',
                'Act or ommission contrary to the obectives of the department'],
            ['Unit or Section SOPs', ''],
            ['Substandard Performance',
                'Inability or unwillingness to perform assigned duties.'],
            ['Vehicle Operation', 'Unauthorized rider'],
            ['Prisoner Handling/Trans.', 'Failure to properly handcuff prisoner'],
            ['Conduct Unbecoming', 'Improper posting on a social media website'],
            ['Substandard Performance', 'Failure to make and turn in all reports promptly, accurately, and completely in conformity with department orders.'],
            ['Citizen Interaction', 'Failure to request interpreter'],
            [None, None]
        ])

    def generate_source(self):
        return random.choice(["CPCO (Formal)", "CPCO (Informal)"])

    def generate_service_type(self):
        return random.choice(
            ["Arresting", "Call for Service", "Code Inforcement",
                "Interviewing", "Restraining", "Transporting", None]
        )

    def generate_assignment(self):
        return random.choice([
            ["Chiefs Staff Division", "Court Liaison", "", ""],
            ["Investigative Division", "Crime Prevention", "C Shift", ""],
            ["Investigative Division", "Detective Bureau",
                "Auto Theft Unit", "Evenings"],
            ["Investigative Division", "Detective Bureau",
                "Auto Theft Unit", "Off Duty"],
            ["Investigative Division", "Detective Bureau",
                "Auto Theft Unit", "Rotating"],
            ["Investigative Division", "Detective Bureau",
                "Homicide  Unit", "Evenings"],
            ["Investigative Division", "Detective Bureau",
                "Homicide  Unit", "Rotating"],
            ["Investigative Division", "First Precinct", "A Shift", "X21 Zone"],
            ["Investigative Division", "First Precinct", "A Shift", "X22 Zone"],
            ["Investigative Division", "First Precinct", "B Shift", "X26 Zone"],
            ["Investigative Division", "Second Precinct", "Day Beats", "Beat 19"],
            ["Investigative Division", "Special Investigations",
                "Computer Crimes", "Days"],
            ["Investigative Division", "Special Investigations",
                "Computer Crimes", "Evenings"],
            ["Investigative Division", "Special Investigations",
                "Criminal Intelligence", "Days"],
            ["Investigative Division", "Special Investigations", "Day Beats", "Beat 19"],
            ["Investigative Division", "Special Investigations", "K 9 Unit", "Days"],
            ["Investigative Division", "Special Investigations", "Narcotics", "Days"],
            ["Investigative Division", "Special Investigations", "Vice", "Evenings"],
            ["Operational Bureau", "First Precinct", "C Shift", "X25 Zone"],
            ["Operational Bureau", "Fourth Precinct", "C.O.P. Program", "Days"],
            ["Operational Bureau", "Fourth Precinct", "Unknown", "Unknown"],
            ["Operational Bureau", "Second Precinct", "B Shift", "X20 Zone"],
            ["Operational Bureau", "Second Precinct", "Day Beats", "Beat 18"],
            ["Operational Bureau", "Second Precinct", "Day Beats", "Beat 19"],
            ["Operational Bureau", "Third Precinct", "C Shift", "X26 Zone"],
            ["Operational Division", "Crime Prevention", "B Shift", "X27 Zone"],
            ["Operational Division", "Detective Bureau", "Auto Theft Unit", "Days"],
            ["Operational Division", "First Precinct", "A Shift", "X20 Zone"],
            ["Operational Division", "First Precinct", "A Shift", "X22 Zone"],
            ["Operational Division", "First Precinct", "A Shift", "X23 Zone"],
            ["Operational Division", "First Precinct", "A Shift", "X24 Zone"],
            ["Operational Division", "First Precinct", "A Shift", "X25 Zone"],
            ["Operational Division", "First Precinct", "A Shift", "X26 Zone"],
            ["Operational Division", "First Precinct", "A Shift", "X27 Zone"],
            ["Operational Division", "First Precinct", "B Shift", "Beat 20"],
            ["Operational Division", "First Precinct", "B Shift", "X20 Zone"],
            ["Operational Division", "First Precinct", "B Shift", "X21 Zone"],
            ["Operational Division", "First Precinct", "B Shift", "X22 Zone"],
            ["Operational Division", "First Precinct", "B Shift", "X23 Zone"],
            ["Operational Division", "First Precinct", "B Shift", "X24 Zone"],
            ["Operational Division", "First Precinct", "B Shift", "X26 Zone"],
            ["Operational Division", "First Precinct", "B Shift", "X27 Zone"],
            ["Operational Division", "First Precinct", "B Shift", "X28 Zone"],
            ["Operational Division", "First Precinct", "C Shift", "X20 Zone"],
            ["Operational Division", "First Precinct", "C Shift", "X21 Zone"],
            ["Operational Division", "First Precinct", "C Shift", "X23 Zone"],
            ["Operational Division", "First Precinct", "C Shift", "X24 Zone"],
            ["Operational Division", "First Precinct", "C Shift", "X25 Zone"],
            ["Operational Division", "Fourth Precinct", "A Shift", "X20 Zone"],
            ["Operational Division", "Fourth Precinct", "A Shift", "X22 Zone"],
            ["Operational Division", "Fourth Precinct", "A Shift", "X24 Zone"],
            ["Operational Division", "Fourth Precinct", "B Shift", "Beat 23"],
            ["Operational Division", "Fourth Precinct", "B Shift", "X25 Zone"],
            ["Operational Division", "Fourth Precinct", "B Shift", "X27 Zone"],
            ["Operational Division", "Fourth Precinct", "C Shift", "Beat 20"],
            ["Operational Division", "Fourth Precinct", "C Shift", "Beat 23"],
            ["Operational Division", "Fourth Precinct", "C Shift", "X20 Zone"],
            ["Operational Division", "Fourth Precinct", "C Shift", "X21 Zone"],
            ["Operational Division", "Fourth Precinct", "C Shift", "X22 Zone"],
            ["Operational Division", "Fourth Precinct", "C Shift", "X25 Zone"],
            ["Operational Division", "Fourth Precinct", "C Shift", "X27 Zone"],
            ["Operational Division", "Fourth Precinct",
                "Commanding Officer", "Days"],
            ["Operational Division", "Second Precinct", "A Shift", "Beat 14"],
            ["Operational Division", "Second Precinct", "A Shift", "Beat 17"],
            ["Operational Division", "Second Precinct", "A Shift", "Beat 19"],
            ["Operational Division", "Second Precinct", "A Shift", "X20 Zone"],
            ["Operational Division", "Second Precinct", "B Shift", "X20 Zone"],
            ["Operational Division", "Second Precinct", "B Shift", "X23 Zone"],
            ["Operational Division", "Second Precinct", "B Shift", "X25 Zone"],
            ["Operational Division", "Second Precinct", "C Shift", "X22 Zone"],
            ["Operational Division", "Second Precinct", "Day Beats", ""],
            ["Operational Division", "Second Precinct", "Day Beats", "Beat 15"],
            ["Operational Division", "Second Precinct", "Day Beats", "Beat 19"],
            ["Operational Division", "Second Precinct", "Day Beats", "Beat 20"],
            ["Operational Division", "Second Precinct", "Days Bikes", "Beat 19"],
            ["Operational Division", "Second Precinct", "Days Bikes", "Evenings"],
            ["Operational Division", "Second Precinct", "Night Beats", "Beat 19"],
            ["Operational Division", "Second Precinct", "Night Beats", "Evenings"],
            ["Operational Division", "Second Precinct", "Oceanfront", "Day Bikes"],
            ["Operational Division", "Second Precinct", "Off Duty / LE", "Evenings"],
            ["Operational Division", "Special Investigations", "B Shift", "X20 Zone"],
            ["Operational Division", "Special Investigations", "Bomb Squad", "Beat 20"],
            ["Operational Division", "Special Operations", "Bomb Squad", "Rotating"],
            ["Operational Division", "Special Operations", "SWAT Team", "	"],
            ["Operational Division", "Special Operations", "SWAT Team", "MidNights"],
            ["Operational Division", "Special Operations", "SWAT Team", "Rotating"],
            ["Operational Division", "Third Precinct", "A Shift", "C.O.P."],
            ["Operational Division", "Third Precinct", "B Shift", "X22 Zone"],
            ["Operational Division", "Third Precinct", "B Shift", "X24 Zone"],
            ["Operational Division", "Third Precinct", "C Shift", "X26 Zone"],
            ["Operational Division", "Third Precinct", "C Shift", "X29 Zone"],
            ["Prof. Dev and Training", "VBLETA", "Instructor", "Days"],
            ["Support Division", "Logistical Support", "A Shift", ""],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]
        ]
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
        return random.choice(["Suspect - Handgun","Suspect - Misc Weapon",
        "Suspect - Unarmed","Suspect - Knife","Suspect - Rifle"])

    def generate_ois_officer_force_type(self):
        return random.choice(["Duty Handgun","IMPD - Duty Handgun","IMPD - Shotgun",
            "IMPD - Patrol Rifle","Personal Patrol Rifle","Personal Shotgun"
        ])
