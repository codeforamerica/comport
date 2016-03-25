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
            date_edited=None
        ),
        ChartBlock(
            title="Complaints By Year",
            caption="",
            slug="complaints-by-year",
            dataset="complaints",
            content="Since 2009, citizens have submitted between 68 to 178 formal complaints about officers each year, with an average of 104 per year. A complaint is from one citizen, but may contain multiple allegations and/or be about multiple officers. This graph counts both formal and informal complaints.",
            date_updated=None,
            date_edited=None
        ),
        ChartBlock(
            title="Complaints By Month",
            caption="",
            slug="complaints-by-month",
            dataset="complaints",
            content="The current month shows complaints to date, so will not be a complete count until the month ends.",
            date_updated=None,
            date_edited=None
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
            date_edited=None
        ),
        ChartBlock(
            title="Complaints By Allegation Type",
            caption="",
            slug="complaints-by-allegation-type",
            dataset="complaints",
            content="""Complaints are mapped to the regulations that IMPD officers must follow. The most frequent complaints relate to interactions with citizens, such as rude language, followed by driving-related complaints.
This count is from January 2014 to present.""",
            date_updated=None,
            date_edited=None
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
            date_edited=None
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
            date_edited=None
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
            date_edited=None
        ),
        ChartBlock(
            title="Demographics of complainants and officers",
            caption="",
            slug="complaints-by-demographic",
            dataset="complaints",
            content="""**This table shows the race of complainants at left and officers at top in each complaint since January 2014.**

If a complaint names multiple officers, they are each counted here, so the numbers may be higher than total complaints filed. For example, if a citizen complaint submits allegations about both an Asian and a white officer, that would add one to both  the Asian and white officer columns for the complainant’s race.""",
            date_updated=None,
            date_edited=None
        ),
        ChartBlock(
            title="Complaints by Officer",
            caption="",
            slug="complaints-by-officer",
            dataset="complaints",
            content="""Racial Profiling is addressed in many classes throughout IMPD's academy. It is defined and prohibited in the cultural awareness class. It is defined and prohibited in the general order class as it is outlined in General Order 1.2, Racial Profiling.

IMPD trains on criminal law and its requirements pertaining to reasonable suspicion and probable cause. Ethical decision making is a topic of training as well. More on IMPD training will be available here soon.""",
            date_updated=None,
            date_edited=None
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
            date_edited=None
        ),

        ChartBlock(
            title="Use of force by precinct/district of incident",
            caption="",
            slug="uof-by-inc-district",
            dataset="use-of-force",
            content="""No content
            """,
            date_updated=None,
            date_edited=None
        ),

        ChartBlock(
            title="Use of Force by Type of Force",
            caption="",
            slug="uof-force-type",
            dataset="use-of-force",
            content="""No content
            """,
            date_updated=None,
            date_edited=None
        ),

        ChartBlock(
            title="Racial breakdown in use of force",
            caption="",
            slug="uof-race",
            dataset="use-of-force",
            content="""No content
            """,
            date_updated=None,
            date_edited=None
        ),

        ChartBlock(
            title="Use of Force Introduction",
            caption="",
            slug="uof-introduction",
            dataset="use-of-force",
            content="""No content
            """,
            date_updated=None,
            date_edited=None
        ),

        ChartBlock(
            title="Officer Involved Shooting Introduction",
            caption="",
            slug="ois-introduction",
            dataset="ois",
            content="""No content
            """,
            date_updated=None,
            date_edited=None
        ),

        ChartBlock(
            title="Officer Involved Shootings by District",
            caption="",
            slug="ois-by-inc-district",
            dataset="ois",
            content="""No content
            """,
            date_updated=None,
            date_edited=None
        ),

        ChartBlock(
            title="Officer Involved Shootings by Officer Weapon Used",
            caption="",
            slug="ois-weapon-type",
            dataset="ois",
            content="""No content
            """,
            date_updated=None,
            date_edited=None
        ),

        ChartBlock(
            title="Officer Involved Shootings by Officer and Resident Race",
            caption="",
            slug="ois-race",
            dataset="ois",
            content="""No content
            """,
            date_updated=None,
            date_edited=None
        ),
    ]
