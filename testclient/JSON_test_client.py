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
            chunk=data[i:i + 100]
            payload={'month': 0, 'year': 0, 'data': chunk}

            url=baseurl + "data/complaints"
            p=requests.post(url, auth = (comport_username,
                            comport_password), json = payload)
            if p.status_code != 200:
                print("error: %s" % p.text.encode("utf-8", "ignore"))

    def make_complaints(self):
        complaints = []
        for x in range(0, 100):
            assignment = self.generate_assignment()
            allegation = self.generate_allegation()
            complaints.append({
                "opaqueId": random_string(10),
                "occuredDate": random_date(datetime(2014, 1, 1), datetime(2016, 1, 1)).strftime("%Y-%m-%d 0:0:00"),
                "division": assignment[0],
                "precinct": assignment[1],
                "shift": assignment[2],
                "beat": assignment[3],
                "serviceType": self.generate_service_type(),
                "source": self.generate_source(),
                "allegationType": allegation[0],
                "allegation": allegation[1],
                "disposition": self.generate_disposition(),
                "residentRace": self.generate_race(),
                "residentSex": self.generate_sex(),
                "residentAge": str(random.randint(15, 70)),
                "officerRace": self.generate_race(),
                "officerSex": self.generate_sex(),
                "officerAge": str(random.randint(23, 50)),
                "officerIdentifier": random_string(10),
                "officerYearsOfService": random.randint(23, 50)
            })
        return complaints

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
            [None,None]
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







        #
        #
        #
        #
        #
        # with open("/Users/chrisreade/comport/data/testdata/complaints/complaints.csv", 'rt') as f:
        #     reader=csv.DictReader(f)
        #
        #     data=[]
        #
        #     for complaint in reader:
        #         officer_identifier=hash(complaint.get("OFFNUM", None))
        #         opaque_id=hash(complaint.get("INCNUM", None))
        #
        #         print(opaque_id)
        #
        #         data.append({
        #             "opaqueId": opaque_id,
        #             "occuredDate": parse_csv_date(complaint.get("OCCURRED_DT", None)),
        #             "division": complaint.get("UDTEXT24A", None),
        #             "precinct": complaint.get("UDTEXT24B", None),
        #             "shift": complaint.get("UDTEXT24C", None),
        #             "beat": complaint.get("UDTEXT24D", None),
        #             "serviceType": complaint.get("SERVICE_TYPE", None),
        #             "source": complaint.get("SOURCE", None),
        #             "allegationType": complaint.get("ALG_CLASS", None),
        #             "allegation": complaint.get("ALLEGATION", None),
        #             "disposition": complaint.get("FINDING", None),
        #             "residentRace": complaint.get("RACE", None),
        #             "residentSex": complaint.get("SEX", None),
        #             "residentAge": complaint.get("CIT_AGE", None),
        #             "officerRace": complaint.get("OFF_RACE", None),
        #             "officerSex": complaint.get("OFF_SEX", None),
        #             "officerAge": complaint.get("OFF_AGE", None),
        #             "officerIdentifier": officer_identifier,
        #             "officerYearsOfService": complaint.get("OFF_YR_EMPLOY", None),
        #             }
        #         )
        #
        #     for i in range(0, len(data), 100):
        #         chunk=data[i:i + 100]
        #         payload={'month': 0, 'year': 0, 'data': chunk}
        #
        #         url=baseurl + "data/complaints"
        #         p=requests.post(url, auth = (comport_username,
        #                         comport_password), json = payload)
        #         if p.status_code != 200:
        #             print("error: %s" % p.text.encode("utf-8", "ignore"))
        #
        #
        # with open("/Users/chrisreade/comport/data/testdata/UOF/uof.csv", 'rt') as f:
        #     reader=csv.DictReader(f)
        #
        #     data=[]
        #
        #     for incident in reader:
        #         officer_identifier=hash(incident.get("OFFNUM", None))
        #         opaque_id=hash(incident.get("INCNUM", None))
        #
        #         print(opaque_id)
        #
        #         data.append({
        #                 "opaqueId": opaque_id,
        #                 "occuredDate": parse_csv_date(incident.get("OCCURRED_DT", None)),
        #                 "division": incident.get("UDTEXT24A", None),
        #                 "precinct": incident.get("UDTEXT24B", None),
        #                 "shift": incident.get("UDTEXT24C", None),
        #                 "beat": incident.get("UDTEXT24D", None),
        #                 "disposition": incident.get("DISPOSITION", None),
        #                 "censusTract": None,
        #                 "residentWeaponUsed": None,
        #                 "officerForceType": incident.get("UOF_FORCE_TYPE", None),
        #                 "serviceType": incident.get("SERVICE_TYPE", None),
        #                 "arrestMade": incident.get("CIT_ARRESTED", None),
        #                 "arrestCharges": incident.get("CITCHARGE_TYPE", None),
        #                 "residentInjured": incident.get("CIT_INJURED", None),
        #                 "residentHospitalized": incident.get("CIT_HOSPITAL", None),
        #                 "officerInjured": incident.get("OFF_INJURED", None),
        #                 "officerHospitalized": incident.get("OFF_HOSPITAL", None),
        #                 "useOfForceReason": incident.get("UOF_REASON", None),
        #                 "residentRace": incident.get("RACE", None),
        #                 "officerRace": incident.get("OFF_RACE", None),
        #                 "residentSex": incident.get("SEX", None),
        #                 "officerSex": incident.get("OFF_SEX", None),
        #                 "officerIdentifier": officer_identifier,
        #                 "officerYearsOfService": incident.get("OFF_YR_EMPLOY", None),
        #                 "officerAge": incident.get("OFF_AGE", None),
        #                 "residentAge": incident.get("CIT_AGE", None),
        #                 "officerCondition": incident.get("OFF_COND_TYPE", None),
        #                 "residentCondition": incident.get("CIT_COND_TYPE", None)
        #             }
        #         )
        #
        #     for i in range(0, len(data), 100):
        #         chunk=data[i:i + 100]
        #         payload={'month': 0, 'year': 0, 'data': chunk}
        #
        #         url=baseurl + "data/UOF"
        #         p=requests.post(url, auth = (comport_username,
        #                         comport_password), json = payload)
        #         if p.status_code != 200:
        #             print("error: %s" % p.text.encode("utf-8", "ignore"))
        #
        # with open("/Users/chrisreade/comport/data/testdata/OIS/ois.csv", 'rt') as f:
        #     reader=csv.DictReader(f)
        #
        #     data=[]
        #
        #     for incident in reader:
        #         officer_identifier=hash(incident.get("OFFNUM", None))
        #         opaque_id=hash(incident.get("INCNUM", None))
        #
        #         print(opaque_id)
        #
        #         data.append({
        #                 "opaqueId": opaque_id,
        #                 "occuredDate": parse_csv_date(incident.get("OCCURRED_DT", None)),
        #                 "division": incident.get("UDTEXT24A", None),
        #                 "precinct": incident.get("UDTEXT24B", None),
        #                 "shift": incident.get("UDTEXT24C", None),
        #                 "beat": incident.get("UDTEXT24D", None),
        #                 "disposition": incident.get("DISPOSITION", None),
        #                 "censusTract": None,
        #                 "officerWeaponUsed": incident.get("WEAPON_TYPE", None),
        #                 "residentWeaponUsed": incident.get("CIT_WEAPON_TYPE", None),
        #                 "serviceType": incident.get("SERVICE_TYPE", None),
        #                 "residentRace": incident.get("RACE", None),
        #                 "officerRace": incident.get("OFF_RACE", None),
        #                 "residentSex": incident.get("SEX", None),
        #                 "officerSex": incident.get("OFF_SEX", None),
        #                 "officerIdentifier": officer_identifier,
        #                 "officerYearsOfService": incident.get("OFF_YR_EMPLOY", None),
        #                 "officerAge": incident.get("OFF_AGE", None),
        #                 "residentAge": incident.get("CIT_AGE", None),
        #                 "officerCondition": incident.get("OFF_COND_TYPE", None),
        #                 "residentCondition": incident.get("CIT_COND_TYPE", None)
        #             }
        #         )
        #
        #     for i in range(0, len(data), 100):
        #         chunk=data[i:i + 100]
        #         payload={'month': 0, 'year': 0, 'data': chunk}
        #
        #         url=baseurl + "data/OIS"
        #         p=requests.post(url, auth = (comport_username,
        #                         comport_password), json = payload)
        #         if p.status_code != 200:
        #             print("error: %s" % p.text.encode("utf-8", "ignore"))
