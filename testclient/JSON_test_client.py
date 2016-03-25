import requests
import hashlib
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

    def hash(self, text, key="bildad"):
        ''' Return an MD5 hash of the combined text and key.
        '''
        if not text or not key:
            return ""
        m = hashlib.md5()
        m.update((str(text) + key).encode('utf-8'))
        return m.hexdigest()

    def make_complaints(self, count=1000):
        complaints = []
        for x in range(0, count):
            assignment = self.generate_assignment()
            allegation = self.generate_allegation()
            complaints.append({
                "opaqueId": self.hash(random_string(10)),
                "serviceType": self.generate_service_type(),
                "source": self.generate_source(),
                "occuredDate": random_date(datetime(2014, 1, 1), datetime(2016, 1, 1)).strftime("%Y-%m-%d 0:0:00"),
                "division": assignment["division"],
                "precinct": assignment["precinct"],
                "shift": assignment["shift"],
                "beat": assignment["beat"],
                "allegationType": allegation["allegationType"],
                "allegation": allegation["allegation"],
                "disposition": self.generate_disposition(),
                "residentRace": self.generate_race(),
                "residentSex": self.generate_sex(),
                "residentAge": str(random.randint(15, 70)),
                "officerIdentifier": self.hash(random_string(10)),
                "officerRace": self.generate_race(),
                "officerSex": self.generate_sex(),
                "officerAge": str(random.randint(23, 50)),
                "officerYearsOfService": str(random.randint(0, 27))
            })

        return complaints

    def make_uof(self, count=1000):
        incidents = []
        for x in range(0, count):
            assignment = self.generate_assignment()
            incidents.append({
                "opaqueId": self.hash(random_string(10)),
                "occuredDate": random_date(datetime(2014, 1, 1), datetime(2016, 1, 1)).strftime("%Y-%m-%d 0:0:00"),
                "occuredTime": "",
                "division": assignment["division"],
                "precinct": assignment["precinct"],
                "shift": assignment["shift"],
                "beat": assignment["beat"],
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
                "officerIdentifier": self.hash(random_string(10)),
                "officerRace": self.generate_race(),
                "officerSex": self.generate_sex(),
                "officerAge": str(random.randint(23, 50)),
                "officerYearsOfService": str(random.randint(0, 27)),
                "officerCondition": self.generate_condition()
            })

        return incidents

    def make_ois(self, count=1000):
        incidents = []
        for x in range(0, count):
            assignment = self.generate_assignment()
            incidents.append({
                "opaqueId": self.hash(random_string(10)),
                "serviceType": self.generate_service_type(),
                "occuredDate": random_date(datetime(2014, 1, 1), datetime(2016, 1, 1)).strftime("%Y-%m-%d 0:0:00"),
                "occuredTime": "",
                "division": assignment["division"],
                "precinct": assignment["precinct"],
                "shift": assignment["shift"],
                "beat": assignment["beat"],
                "disposition": self.generate_disposition(),
                "residentRace": self.generate_race(),
                "residentSex": self.generate_sex(),
                "residentAge": str(random.randint(15, 70)),
                "residentWeaponUsed": self.generate_ois_resident_force_type(),
                "residentCondition": self.generate_condition(),
                "officerIdentifier": self.hash(random_string(10)),
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
        allegation = random.choice([
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
        return {"allegationType": allegation[0], "allegation": allegation[1]}

    def generate_source(self):
        return random.choice(["CPCO (Formal)", "CPCO (Informal)"])

    def generate_service_type(self):
        return random.choice(
            ["Arresting", "Call for Service", "Code Inforcement",
                "Interviewing", "Restraining", "Transporting", None]
        )

    def generate_assignment(self):
        assignment = random.choice([
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
        ])
        return {"division": assignment[0], "precinct": assignment[1], "shift": assignment[2], "beat": assignment[3]}

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
