# -*- coding: utf-8 -*-
from .models import ChartBlock

class ChartBlockDefaults:
    defaults = [
        ChartBlock(
            title="Open Data Introduction",
            caption="",
            slug="introduction",
            dataset="introduction",
            content="""We believe that being transparent about our work will help us better serve the people of Indianapolis, and that being accountable to our citizens will allow us to work together to improve relationships between IMPD and Indianapolis residents.

[Here](http://www.socrata.com) is a link to the City's open data portal and open data policy
            """,
            date_updated=None,
            date_edited=None,
            order=0
        ),
        ChartBlock(
            title="Complaints By Year",
            caption="",
            slug="complaints-by-year",
            dataset="complaints",
            content="Since 2009, citizens have submitted between 68 to 178 formal complaints about officers each year, with an average of 104 per year. A complaint is from one citizen, but may contain multiple allegations and/or be about multiple officers. This graph counts both formal and informal complaints.",
            date_updated=None,
            date_edited=None,
            order=0
        ),
        ChartBlock(
            title="Complaints By Month",
            caption="",
            slug="complaints-by-month",
            dataset="complaints",
            content="The current month shows complaints to date, so will not be a complete count until the month ends.",
            date_updated=None,
            date_edited=None,
            order=0
        ),
        ChartBlock(
            title="Complaints By Allegation",
            caption="",
            slug="complaints-by-allegation",
            dataset="complaints",
            content="""
Allegations in complaints fall into a number of classes.  For example, the allegation class citizen interaction contains specific allegations such as rude, demeaning and affronting language, and failure to provide name or badge number.
            """,
            date_updated=None,
            date_edited=None,
            order=0
        ),
        ChartBlock(
            title="Complaints By Allegation Type",
            caption="",
            slug="complaints-by-allegation-type",
            dataset="complaints",
            content="""Complaints are mapped to the regulations that IMPD officers must follow. The most frequent complaints relate to interactions with citizens, such as rude language, followed by driving-related complaints.
This count is from January 2014 to present.""",
            date_updated=None,
            date_edited=None,
            order=0
        ),
        ChartBlock(
            title="Complaints By Disposition",
            caption="",
            slug="complaints-by-disposition",
            dataset="complaints",
            content="""
Information about [the complaint investigation process](http://www.indy.gov/eGov/City/DPS/CPCO/Pages/faq.aspx#4) is available on the [CPCO FAQ page](http://www.indy.gov/eGov/City/DPS/CPCO/Pages/faq).
Each complaint may contain multiple allegations, such as rudeness and inappropriate language. Each allegation receives separate findings.
There are four possible findings:

**Sustained** means that the majority of the evidence proved that the allegation occurred and was in violation of a department policy.  When allegations are sustained, appropriate disciplinary action will be taken.

**Not sustained** means there was no majority of evidence to prove or disprove the allegation.

**Exonerated** means the majority of the evidence proved the allegation occurred, but it was within department policy.

**Unfounded** means the majority of the evidence disproved that the allegation occurred.

All findings remain on an officer’s personnel record.

Complaints that are still being investigated are shown as **unspecified** in this chart.
            """,
            date_updated=None,
            date_edited=None,
            order=0
        ),
        ChartBlock(
            title="Complaints By Precinct",
            caption="",
            slug="complaints-by-precinct",
            dataset="complaints",
            content="""IMPD serves [six districts](http://www.indy.gov/eGov/City/DPS/IMPD/Enforcement/Districts/Pages/home.aspx) within Indianapolis.  There are also branches with specific focus areas.

North District:  209, 916 population; 78.5 square miles

East District:  145,489 population; 49.9 square miles

Northwest District:  143,395 population; 66.2 square miles

Downtown District:  12,929 population; 3.6 square miles

Southeast District:  175,812 population; 84.9 square miles

Southwest District: 136,680 population; 80.8 square miles

Population information is from 2010 census data.
""",
            date_updated=None,
            date_edited=None,
            order=0
        ),
        ChartBlock(
            title="Officer Demographics",
            caption="",
            slug="officer-demographics",
            dataset="all",
            content="""
This chart shows the number of officers who have received one or more complaints since January 2014.
**As of September 2015, there were 1,583 officers employed by IMPD. Approximately 1,190 officers have not received complaints since January 2014, which is about 75%.**
This chart shows both Formal and Informal complaints, so some numbers appear larger than expected.
            """,
            date_updated=None,
            date_edited=None,
            order=0
        ),
        ChartBlock(
            title="Demographics of complainants and officers",
            caption="",
            slug="complaints-by-demographic",
            dataset="complaints",
            content="""**This table shows the race of complainants at left and officers at top in each complaint since January 2014.**

If a complaint names multiple officers, they are each counted here, so the numbers may be higher than total complaints filed. For example, if a citizen complaint submits allegations about both an Asian and a white officer, that would add one to both  the Asian and white officer columns for the complainant’s race.""",
            date_updated=None,
            date_edited=None,
            order=0
        ),
        ChartBlock(
            title="Complaints by Officer",
            caption="",
            slug="complaints-by-officer",
            dataset="complaints",
            content="""Racial Profiling is addressed in many classes throughout IMPD's academy. It is defined and prohibited in the cultural awareness class. It is defined and prohibited in the general order class as it is outlined in General Order 1.2, Racial Profiling.

IMPD trains on criminal law and its requirements pertaining to reasonable suspicion and probable cause. Ethical decision making is a topic of training as well. More on IMPD training will be available here soon.""",
            date_updated=None,
            date_edited=None,
            order=0
        ),
        ChartBlock(
            title="Introduction to Complaints Data",
            caption="",
            slug="complaints-introduction",
            dataset="complaints",
            content="""This page is an Alpha prototype and is subject to change. We're absolutely interested in feedback from all users. Please email us at [Indy@codeforamerica.org](mailto:Indy@codeforamerica.org) or check out our twitter at [@projectcomport](https://twitter.com/projectcomport). This open data project is the result of a partnership between the Indianapolis Department of Public Safety and Code for America. It opens data that CPCO and IMPD have been collecting internally, but that has not been shared publicly before.

**About the Citizens’ Police Complaint Office**

The Citizens' Police Complaint Office (CPCO) is an office, independent of the Indianapolis Metropolitan Police Department, created by City Ordinance. It affords citizens of Indianapolis who believe they have been treated improperly by an IMPD officer the opportunity to have their complaints articulated and investigated.

The Citizens' Police Complaint Board is a twelve member board consisting of nine civilian voting members and three non-voting police officers. These members are appointed by the City-County Council, the Mayor, and the Fraternal Order of Police (FOP) and have the task of reviewing all formal cases filed in the CPCO.

More information about the complaint process is available at the [CPCO website](http://www.indy.gov/egov/city/dps/cpco/pages/home.aspx) and [FAQ](http://www.indy.gov/eGov/City/DPS/CPCO/Pages/faq.aspx).

In 2015, the Citizens Police Complaint Office has done a large amount of outreach to let more people know that our office exists to hear and investigate their grievances, as well as made it easier to submit complaints online. The CPCO has also worked to decrease the average time from when a formal complaint is submitted to when it is discussed at a hearing by our Citizens Police Complaint Board. In 2013, the average was 9-18 months – In 2014, it was down to 5 months, and the 2015 average is under three months. We strive to treat complainants individually and fairly regardless of the nature of their complaint.

[The Indianapolis Ordinance that established the CPCO is Chapter 251, Article 1, Division 3](https://www.municode.com/library/in/indianapolis_-_marion_county/codes/code_of_ordinances?nodeId=TITIORAD_CH251DEPUSA_ARTIINGE_DIV3CIPOCOPR).

**Why we're sharing this data - transparency to build trust**

We believe that being transparent about our work will help us better serve the people of Indianapolis, and that being accountable to our citizens will allow us to work together to improve relationships between IMPD and Indianapolis residents.

**What you can do with this data**

We have done some initial analysis on this dataset, though there are many other ways the data can be compared and analyzed. The underlying data is available [here](https://www.projectcomport.org/department/IMPD/schema/complaints) for public use.""",
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Use of force by precinct/district of incident",
            caption="",
            slug="uof-by-inc-district",
            dataset="use-of-force",
            content="""No content
            """,
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Use of Force by Type of Force",
            caption="",
            slug="uof-force-type",
            dataset="use-of-force",
            content="""No content
            """,
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Racial breakdown in use of force",
            caption="",
            slug="uof-race",
            dataset="use-of-force",
            content="""No content
            """,
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Use of Force Introduction",
            caption="",
            slug="uof-introduction",
            dataset="use-of-force",
            content="""No content
            """,
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Officer Involved Shooting Introduction",
            caption="",
            slug="ois-introduction",
            dataset="ois",
            content="""No content
            """,
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Officer Involved Shootings by District",
            caption="",
            slug="ois-by-inc-district",
            dataset="ois",
            content="""No content
            """,
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Officer Involved Shootings by Officer Weapon Used",
            caption="",
            slug="ois-weapon-type",
            dataset="ois",
            content="""No content
            """,
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Officer Involved Shootings by Officer and Resident Race",
            caption="",
            slug="ois-race",
            dataset="ois",
            content="""No content
            """,
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Introduction to Assaults Data",
            caption="",
            slug="assaults-introduction",
            dataset="assaults",
            content="""TK""",
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Assaults By Service Type",
            caption="",
            slug="assaults-by-service-type",
            dataset="assaults",
            content="""TK""",
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Assaults By Force Type",
            caption="",
            slug="assaults-by-force-type",
            dataset="assaults",
            content="""TK""",
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Assaults by Officer",
            caption="",
            slug="assaults-by-officer",
            dataset="assaults",
            content="""TK""",
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Intro",
            dataset="intros",
            slug="uof-schema-introduction",
            content="Please Note: IMPD started using a new database and process for collecting this data in Summer 2014. Entries prior to July 2014 were entered in to the database from an older paper form, so they may not be consistent with entries after Summer 2014.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Disclaimer",
            dataset="footer",
            slug="uof-schema-disclaimer",
            content='''DISCLAIMER OF LIABILITY: The City voluntarily provides the data on this website as a service to the public. The City retains ownership of any data or documents that originate with City, and the data may not be sold, published, or exchanged for commercial purposes. The City no representation, either implied or expressed, as to the content, accuracy, or completeness of any of the data provided at this website. The City makes this data available on an “as is” basis and explicitly disclaims any representations and warranties.

RESERVATION OF RIGHTS: The City reserves the right to discontinue availability of content on this website at any time and for any reason. The City also reserves the right to claim or seek to protect any intellectual property rights in any of the information, images, software, or processes displayed or used at this website. The data provided on this website does not grant anyone any title or right to any patent, copyright, trademark or other intellectual property rights that the City may have in any of the information, images, software, or processes displayed or used at this website.

INDEMNIFICATION: To the fullest extent permitted by law, any user of the data provided at this website shall defend, indemnify, hold harmless the City, its officers, officials and employees from any claim, loss, damage, injury, or liability of any kind (including, without limitation, incidental and consequential damages, court costs, attorneys’ fees and costs of investigation), that arise directly or indirectly, in whole or in part, from that user’s use of this data, including any secondary or derivative use of the information provided herein.''',
            caption="",
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Footer",
            dataset="footer",
            slug="uof-schema-footer",
            content="*Officer Call data represents the number of calls for service from residents that officers responded to plus the number of times officers themselves initiated a response.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Id",
            dataset="",
            slug="uof-schema-field-id",
            content="This is a hashed unique identifier for a given incident. Incidents may contain multiple uses of force. When that is the case, there will be multiple entries for one incident number.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Occurred Date",
            dataset="",
            slug="uof-schema-field-occurred-date",
            content="The date that the incident occurred.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=1
        ),

        ChartBlock(
            title="Division",
            dataset="",
            slug="uof-schema-field-division",
            content="This is the Division that the officer was assigned to at time of the incident, such as Criminal Investigation or Administration.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=2
        ),

        ChartBlock(
            title="District",
            dataset="",
            slug="uof-schema-field-district",
            content="This is the District, such as East District or NW District, or Branch, such as Homicide or Robbery, that the officer was assigned to at the time of the incident.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=3
        ),

        ChartBlock(
            title="Shift",
            dataset="",
            slug="uof-schema-field-shift",
            content="This is the shift, such as Day or Late shift, or section, such as crash investigation section, that the officer was assigned to at the time of the incident.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=4
        ),

        ChartBlock(
            title="Beat",
            dataset="",
            slug="uof-schema-field-beat",
            content="Some shifts contain this secondary level of detail on the officer's assignment.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=5
        ),

        ChartBlock(
            title="Use of Force Reason",
            dataset="",
            slug="uof-schema-field-use-of-force-reason",
            content="The reason the officer used force, such as Assaulting Officer(s) or Combative Suspect.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=6
        ),

        ChartBlock(
            title="Officer Force Type",
            dataset="",
            slug="uof-schema-field-officer-force-type",
            content='''In Indianapolis, kinds of force are categorized as physical if the officer uses their body, less lethal if the officer uses a weapon that's commonly considered non-lethal, or lethal if the officer uses a firearm, knife or vehicle. The types of force counted are:

- Physical: Elbow Strike, Fist Strike, Handcuffing, Joint/Pressure, Kick, Knee Strike, Leg Sweep, Other, Palm Strike, Take Down, Weight Leverage
- Less Lethal: Baton, Bean Bag, BPS Gas, Burning CS, Clearout OC, CS Fogger, CS Grenade, CS/OC, Flash Bang, Other, Pepperball, Taser
- Lethal: Handgun, Knife, Rifle, Shotgun, Sniper Rifle, Sub Machine Gun, Vehicle
- Canine Bite is the only use of force type that doesn’t fall within the three types.''',
            caption="",
            date_updated=None,
            date_edited=None,
            order=7
        ),

        ChartBlock(
            title="Disposition",
            dataset="",
            slug="uof-schema-field-disposition",
            content="If there was an investigation and ruling on the incident, it will be noted here.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=8
        ),

        ChartBlock(
            title="Service Type",
            dataset="",
            slug="uof-schema-field-service-type",
            content="The reason for the interaction, such as Traffic Stop or Call for Service.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=9
        ),

        ChartBlock(
            title="Arrest Made",
            dataset="",
            slug="uof-schema-field-arrest-made",
            content="Whether the resident was arrested as part of the incident.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=10
        ),

        ChartBlock(
            title="Arrest Charges",
            dataset="",
            slug="uof-schema-field-arrest-charges",
            content="If the resident was arrested as part of the incident, what they were charged with.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=11
        ),

        ChartBlock(
            title="Resident Injured",
            dataset="",
            slug="uof-schema-field-resident-injured",
            content="TRUE if the resident was injured during the incident, FALSE if the resident was not injured.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=12
        ),

        ChartBlock(
            title="Resident Hospitalized",
            dataset="",
            slug="uof-schema-field-resident-hospitalized",
            content="TRUE if the resident was hospitalized during the incident, FALSE if the resident was not hospitalized.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=13
        ),

        ChartBlock(
            title="Resident Condition",
            dataset="",
            slug="uof-schema-field-resident-condition",
            content="Injuries the resident sustained, if any, such as Complaint of Pain or Laceration.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=14
        ),

        ChartBlock(
            title="Officer Injured",
            dataset="",
            slug="uof-schema-field-officer-injured",
            content="TRUE if the officer was injured during the incident, FALSE if the officer was not injured.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=15
        ),

        ChartBlock(
            title="Officer Hospitalized",
            dataset="",
            slug="uof-schema-field-officer-hospitalized",
            content="TRUE if the officer was hospitalized during the incident, FALSE if the officer was not hospitalized.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=16
        ),

        ChartBlock(
            title="Officer Condition",
            dataset="",
            slug="uof-schema-field-officer-condition",
            content="Injuries the officer sustained, if any, such as Minor Bleeding.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=17
        ),

        ChartBlock(
            title="Resident Race",
            dataset="",
            slug="uof-schema-field-resident-race",
            content="The resident's race, with the following categories: Asian, Bi-racial, Black, Hispanic, Unknown, White.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=18
        ),

        ChartBlock(
            title="Resident Sex",
            dataset="",
            slug="uof-schema-field-resident-sex",
            content="The resident's gender.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=19
        ),

        ChartBlock(
            title="Resident Age",
            dataset="",
            slug="uof-schema-field-resident-age",
            content="The resident's age at the time of the incident, if known.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=20
        ),

        ChartBlock(
            title="Officer Race",
            dataset="",
            slug="uof-schema-field-officer-race",
            content="The officer's race, with the following categories: Asian, Bi-racial, Black, Hispanic, Unknown, White.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=21
        ),

        ChartBlock(
            title="Officer Sex",
            dataset="",
            slug="uof-schema-field-officer-sex",
            content="The officer's gender.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=22
        ),

        ChartBlock(
            title="Officer Age",
            dataset="",
            slug="uof-schema-field-officer-age",
            content="The officer's age at the time of the incident.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=23
        ),

        ChartBlock(
            title="Officer Years of Service",
            dataset="",
            slug="uof-schema-field-officer-years-of-service",
            content="The number of years the officer had been employed by IMPD at the time of the incident.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=24
        ),

        ChartBlock(
            title="Officer Identifier",
            dataset="",
            slug="uof-schema-field-officer-identifier",
            content="This is a hashed identifier used to identify the officer within this data, for example to see if an officer has received multiple complaints.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=25
        ),

        ChartBlock(
            title="Intro",
            dataset="intros",
            slug="complaints-schema-introduction",
            content="Please Note: The CPCO started using a new database and process for collecting this data in January 2014. Entries prior to January 2014 were entered into an older paper form, so they are unavailable in this dataset at this time.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Id",
            dataset="",
            slug="complaints-schema-field-id",
            content="This is a hashed unique identifier for a given complaint. Complaints may contain multiple allegations. When that is the case, there will be multiple entries for one incident number.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Occurred Date",
            dataset="",
            slug="complaints-schema-field-occurred-date",
            content="The date that the incident occurred.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=1
        ),

        ChartBlock(
            title="Division",
            dataset="",
            slug="complaints-schema-field-division",
            content="This is the Division that the officer was assigned to at time of the incident, such as Criminal Investigation or Administration.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=2
        ),

        ChartBlock(
            title="District",
            dataset="",
            slug="complaints-schema-field-district",
            content="This is the District, such as East District or NW District, or Branch, such as Homicide or Robbery, that the officer was assigned to at the time of the incident.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=3
        ),

        ChartBlock(
            title="Shift",
            dataset="",
            slug="complaints-schema-field-shift",
            content="This is the shift, such as Day or Late shift, or section, such as crash investigation section, that the officer was assigned to at the time of the incident.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=4
        ),

        ChartBlock(
            title="Beat",
            dataset="",
            slug="complaints-schema-field-beat",
            content="Some shifts contain this secondary level of detail on the officer's assignment.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=5
        ),

        ChartBlock(
            title="Service Type",
            dataset="",
            slug="complaints-schema-field-service-type",
            content="The reason for the interaction, such as Traffic Stop or Call for Service.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=6
        ),

        ChartBlock(
            title="Source",
            dataset="",
            slug="complaints-schema-field-source",
            content="Who received the complaint and whether it was categorized as formal or informal.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=7
        ),

        ChartBlock(
            title="Allegation Type",
            dataset="",
            slug="complaints-schema-field-allegation-type",
            content="Allegations in complaints fall into a number of classes. Some classes of allegations are: Citizen Interactions, Bias Based Policing and Use of Force.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=8
        ),

        ChartBlock(
            title="Allegation",
            dataset="",
            slug="complaints-schema-field-allegation",
            content="Allegations are tied to the regulations and standards which Officers are held to. Examples are: rude, demeaning and affronting language, and failure to provide name or badge number, which both fall under the allegation class of citizen interaction.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=9
        ),

        ChartBlock(
            title="Finding",
            dataset="",
            slug="complaints-schema-field-finding",
            content='''Each complaint may contain multiple allegations, such as rudeness and inappropriate language. Each allegation receives separate findings. There are four possible findings:

- Sustained means that the investigation agreed with the allegation in the complaint. When allegations are sustained, the Chief of Police will take the appropriate disciplinary action.
- Not sustained means that the investigation did not find evidence to prove or disprove the complaint. If allegations are found to be not sustained, the officer's name is submitted to IMPD's Early Warning system.
- Exonerated means the incident happened, but it was lawful and proper.
- Unfounded means that the incident happened, however not as detailed in the complaint.

Complaints that are still being investigated will be blank in this column.''',
            caption="",
            date_updated=None,
            date_edited=None,
            order=10
        ),

        ChartBlock(
            title="Resident Race",
            dataset="",
            slug="complaints-schema-field-resident-race",
            content="The resident's race, with the following categories: Asian, Bi-racial, Black, Hispanic, Unknown, White.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=11
        ),

        ChartBlock(
            title="Resident Sex",
            dataset="",
            slug="complaints-schema-field-resident-sex",
            content="The resident's gender.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=12
        ),

        ChartBlock(
            title="Resident Age",
            dataset="",
            slug="complaints-schema-field-resident-age",
            content="The resident's age at the time of the incident, if known.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=13
        ),

        ChartBlock(
            title="Officer Race",
            dataset="",
            slug="complaints-schema-field-officer-race",
            content="The officer's race, with the following categories: Asian, Bi-racial, Black, Hispanic, Unknown, White.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=14
        ),

        ChartBlock(
            title="Officer Sex",
            dataset="",
            slug="complaints-schema-field-officer-sex",
            content="The officer's gender.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=15
        ),

        ChartBlock(
            title="Officer Age",
            dataset="",
            slug="complaints-schema-field-officer-age",
            content="The officer's age at the time of the incident.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=16
        ),

        ChartBlock(
            title="Officer Years of Service",
            dataset="",
            slug="complaints-schema-field-officer-years-of-service",
            content="The number of years the officer had been employed by IMPD at the time of the incident.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=17
        ),

        ChartBlock(
            title="Officer Identifier",
            dataset="",
            slug="complaints-schema-field-officer-identifier",
            content="This is a hashed identifier used to identify the officer within this data, for example to see if an officer has received multiple complaints.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=18
        ),

        ChartBlock(
            title="FOOTER",
            dataset="footer",
            slug="complaints-schema-footer",
            content="*Officer Call data represents the number of calls for service from residents that officers responded to plus the number of times officers themselves initiated a response.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="DISCLAIMER",
            dataset="disclaimer",
            slug="complaints-schema-disclaimer",
            content='''DISCLAIMER OF LIABILITY: The City voluntarily provides the data on this website as a service to the public. The City retains ownership of any data or documents that originate with City, and the data may not be sold, published, or exchanged for commercial purposes. The City no representation, either implied or expressed, as to the content, accuracy, or completeness of any of the data provided at this website.  The City makes this data available on an “as is” basis and explicitly disclaims any representations and warranties.

RESERVATION OF RIGHTS: The City reserves the right to discontinue availability of content on this website at any time and for any reason.  The City also reserves the right to claim or seek to protect any intellectual property rights in any of the information, images, software, or processes displayed or used at this website. The data provided on this website does not grant anyone any title or right to any patent, copyright, trademark or other intellectual property rights that the City may have in any of the information, images, software, or processes displayed or used at this website.

INDEMNIFICATION: To the fullest extent permitted by law, any user of the data provided at this website shall defend, indemnify,  hold harmless the City, its officers, officials and employees from any claim, loss, damage, injury, or liability of any kind (including, without limitation, incidental and consequential damages, court costs, attorneys’ fees and costs of investigation), that arise directly or indirectly, in whole or in part, from that user’s use of this data, including any secondary or derivative use of the information provided herein.''',
            caption="",
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Intro",
            dataset="intros",
            slug="assaults-schema-introduction",
            content="This is Assaults on Officers intro text.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Id",
            dataset="",
            slug="assaults-schema-field-id",
            content="This is a hashed unique identifier for a given incident.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=0
        ),


        ChartBlock(
            title="Officer Identifier",
            dataset="",
            slug="assaults-schema-field-officer-identifier",
            content="This is a hashed identifier used to identify the officer within this data, for example to see if an officer has been involved in multiple assaults.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=1
        ),

        ChartBlock(
            title="Service Type",
            dataset="",
            slug="assaults-schema-field-service-type",
            content="The reason for the interaction, such as Traffic Stop or Call for Service.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=2
        ),

        ChartBlock(
            title="Force Type",
            dataset="",
            slug="assaults-schema-field-force-type",
            content="The type of weapon used against the officer.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=3
        ),

        ChartBlock(
            title="Assignment",
            dataset="",
            slug="assaults-schema-field-assignment",
            content="The type of vehicle the officers were in.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=4
        ),

        ChartBlock(
            title="Arrest Made",
            dataset="",
            slug="assaults-schema-field-arrest-made",
            content="True if the person assaulting the officer was arrested.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=5
        ),

        ChartBlock(
            title="Officer Injured",
            dataset="",
            slug="assaults-schema-field-officer-injured",
            content="True if officer was injured during the incident.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=6
        ),

        ChartBlock(
            title="Officer Killed",
            dataset="",
            slug="assaults-schema-field-officer-killed",
            content="True if officer was killed during the incident.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=7
        ),

        ChartBlock(
            title="Report Filed",
            dataset="",
            slug="assaults-schema-field-report-filed",
            content="True if a report was filed about the incident.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=8
        ),

        ChartBlock(
            title="FOOTER",
            dataset="footer",
            slug="assaults-schema-footer",
            content="*Officer Call data represents the number of calls for service from residents that officers responded to plus the number of times officers themselves initiated a response.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="DISCLAIMER",
            dataset="disclaimer",
            slug="assaults-schema-disclaimer",
            content='''DISCLAIMER OF LIABILITY: The City voluntarily provides the data on this website as a service to the public. The City retains ownership of any data or documents that originate with City, and the data may not be sold, published, or exchanged for commercial purposes. The City no representation, either implied or expressed, as to the content, accuracy, or completeness of any of the data provided at this website.  The City makes this data available on an “as is” basis and explicitly disclaims any representations and warranties.

RESERVATION OF RIGHTS: The City reserves the right to discontinue availability of content on this website at any time and for any reason.  The City also reserves the right to claim or seek to protect any intellectual property rights in any of the information, images, software, or processes displayed or used at this website. The data provided on this website does not grant anyone any title or right to any patent, copyright, trademark or other intellectual property rights that the City may have in any of the information, images, software, or processes displayed or used at this website.

INDEMNIFICATION: To the fullest extent permitted by law, any user of the data provided at this website shall defend, indemnify,  hold harmless the City, its officers, officials and employees from any claim, loss, damage, injury, or liability of any kind (including, without limitation, incidental and consequential damages, court costs, attorneys’ fees and costs of investigation), that arise directly or indirectly, in whole or in part, from that user’s use of this data, including any secondary or derivative use of the information provided herein.''',
            caption="",
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Intro",
            dataset="intros",
            slug="ois-schema-introduction",
            content="Please Note: IMPD started using a new database and process for collecting this data in Summer 2014. Entries prior to July 2014 were entered in to the database from an older paper form, so they may not be consistent with entries after Summer 2014.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Footer",
            dataset="footer",
            slug="ois-schema-footer",
            content="*Officer Call data represents the number of calls for service from residents that officers responded to plus the number of times officers themselves initiated a response.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Disclaimer",
            dataset="disclaimer",
            slug="ois-schema-disclaimer",
            content='''DISCLAIMER OF LIABILITY: The City voluntarily provides the data on this website as a service to the public. The City retains ownership of any data or documents that originate with City, and the data may not be sold, published, or exchanged for commercial purposes. The City no representation, either implied or expressed, as to the content, accuracy, or completeness of any of the data provided at this website. The City makes this data available on an “as is” basis and explicitly disclaims any representations and warranties.

RESERVATION OF RIGHTS: The City reserves the right to discontinue availability of content on this website at any time and for any reason. The City also reserves the right to claim or seek to protect any intellectual property rights in any of the information, images, software, or processes displayed or used at this website. The data provided on this website does not grant anyone any title or right to any patent, copyright, trademark or other intellectual property rights that the City may have in any of the information, images, software, or processes displayed or used at this website.

INDEMNIFICATION: To the fullest extent permitted by law, any user of the data provided at this website shall defend, indemnify, hold harmless the City, its officers, officials and employees from any claim, loss, damage, injury, or liability of any kind (including, without limitation, incidental and consequential damages, court costs, attorneys’ fees and costs of investigation), that arise directly or indirectly, in whole or in part, from that user’s use of this data, including any secondary or derivative use of the information provided herein.''',
            caption="",
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Id",
            dataset="",
            slug="ois-schema-field-id",
            content="This is a hashed unique identifier for a given incident. Incidents may contain multiple uses of force. When that is the case, there will be multiple entries for one incident number.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=0
        ),

        ChartBlock(
            title="Occurred Date",
            dataset="",
            slug="ois-schema-field-occurred-date",
            content="The date that the incident occurred.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=1
        ),

        ChartBlock(
            title="Division",
            dataset="",
            slug="ois-schema-field-division",
            content="This is the Division that the officer was assigned to at time of the incident, such as Criminal Investigation or Administration.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=2
        ),

        ChartBlock(
            title="District",
            dataset="",
            slug="ois-schema-field-district",
            content="This is the District, such as East District or NW District, or Branch, such as Homicide or Robbery, that the officer was assigned to at the time of the incident.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=3
        ),

        ChartBlock(
            title="Shift",
            dataset="",
            slug="ois-schema-field-shift",
            content="This is the shift, such as Day or Late shift, or section, such as crash investigation section, that the officer was assigned to at the time of the incident.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=4
        ),

        ChartBlock(
            title="Beat",
            dataset="",
            slug="ois-schema-field-beat",
            content="Some shifts contain this secondary level of detail on the officer's assignment.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=5
        ),

        ChartBlock(
            title="Disposition",
            dataset="",
            slug="ois-schema-field-disposition",
            content="If there was an investigation and ruling on the incident, it will be noted here.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=6
        ),

        ChartBlock(
            title="Resident Weapon Used",
            dataset="",
            slug="ois-schema-field-resident-weapon-used",
            content="The weapon the resident had at the time of the incident, if any.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=7
        ),

        ChartBlock(
            title="Officer Weapon Used",
            dataset="",
            slug="ois-schema-field-officer-weapon-used",
            content="The firearm type the officer used in the incident, and whether it was a duty or personal weapon.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=8
        ),

        ChartBlock(
            title="Service Type",
            dataset="",
            slug="ois-schema-field-service-type",
            content="The reason for the interaction, such as Traffic Stop or Call for Service.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=9
        ),

        ChartBlock(
            title="Resident Condition",
            dataset="",
            slug="ois-schema-field-resident-condition",
            content="Injuries the resident sustained, if any, such as Complaint of Pain or Laceration.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=10
        ),

        ChartBlock(
            title="Officer Condition",
            dataset="",
            slug="ois-schema-field-officer-condition",
            content="Injuries the officer sustained, if any, such as Minor Bleeding.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=11
        ),

        ChartBlock(
            title="Resident Race",
            dataset="",
            slug="ois-schema-field-resident-race",
            content="The resident's race, with the following categories: Asian, Bi-racial, Black, Hispanic, Unknown, White.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=12
        ),

        ChartBlock(
            title="Resident Sex",
            dataset="",
            slug="ois-schema-field-resident-sex",
            content="The resident's gender.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=13
        ),

        ChartBlock(
            title="Resident Age",
            dataset="",
            slug="ois-schema-field-resident-age",
            content="The resident's age at the time of the incident, if known.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=14
        ),

        ChartBlock(
            title="Officer Race",
            dataset="",
            slug="ois-schema-field-officer-race",
            content="The officer's race, with the following categories: Asian, Bi-racial, Black, Hispanic, Unknown, White.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=15
        ),

        ChartBlock(
            title="Officer Sex",
            dataset="",
            slug="ois-schema-field-officer-sex",
            content="The officer's gender.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=16
        ),


        ChartBlock(
            title="Officer Age",
            dataset="",
            slug="ois-schema-field-officer-age",
            content="The officer's age at the time of the incident.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=17
        ),

        ChartBlock(
            title="Officer Years of Service",
            dataset="",
            slug="ois-schema-field-officer-years-of-service",
            content="The number of years the officer had been employed by IMPD at the time of the incident.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=18
        ),

        ChartBlock(
            title="Officer Identifier",
            dataset="",
            slug="ois-schema-field-officer-identifier",
            content="This is a hashed identifier used to identify the officer within this data, for example to see if an officer has received multiple complaints.",
            caption="",
            date_updated=None,
            date_edited=None,
            order=19
        )
    ]
