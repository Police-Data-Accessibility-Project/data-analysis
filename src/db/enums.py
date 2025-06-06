"""
These define enums used primarily for
internal representation in the database
and which are otherwise not used in the logic
"""

from enum import Enum


class ErrorType(Enum):
    SCRAPE = "scrape"
    PARSE = "parse"

class RecordTypeFine(Enum):
    POLICIES_AND_CONTRACTS = "Policies & Contracts"
    NOT_CRIMINAL_JUSTICE_RELATED = "Not Criminal Justice Related"
    MEDIA_BULLETINS = "Media Bulletins"
    POOR_DATA_SOURCE = "Poor Data Source"
    RESOURCES = "Resources"
    PERSONNEL_RECORDS = "Personnel Records"
    CONTACT_INFO_AND_AGENCY_META = "Contact Info & Agency Meta"
    MISC_POLICE_ACTIVITY = "Misc Police Activity"
    ARREST_RECORDS = "Arrest Records"
    DISPATCH_LOGS = "Dispatch Logs"
    WANTED_PERSONS = "Wanted Persons"
    LIST_OF_DATA_SOURCES = "List of Data Sources"
    COMPLAINTS_AND_MISCONDUCT = "Complaints & Misconduct"
    DAILY_ACTIVITY_LOGS = "Daily Activity Logs"
    TRAINING_AND_HIRING_INFO = "Training & Hiring Info"
    ANNUAL_AND_MONTHLY_REPORTS = "Annual & Monthly Reports"
    CALLS_FOR_SERVICE = "Calls for Service"
    OFFICER_INVOLVED_SHOOTINGS = "Officer Involved Shootings"
    CRIME_MAPS_AND_REPORTS = "Crime Maps & Reports"
    COURT_CASES = "Court Cases"
    RECORDS_REQUEST_INFO = "Records Request Info"
    ACCIDENT_REPORTS = "Accident Reports"
    INCIDENT_REPORTS = "Incident Reports"
    DISPATCH_RECORDINGS = "Dispatch Recordings"
    GEOGRAPHIC = "Geographic"
    SEX_OFFENDER_REGISTRY = "Sex Offender Registry"
    CRIME_STATISTICS = "Crime Statistics"
    FIELD_CONTACTS = "Field Contacts"
    SURVEYS = "Surveys"
    USE_OF_FORCE_REPORTS = "Use of Force Reports"
    INCARCERATION_RECORDS = "Incarceration Records"
    CITATIONS = "Citations"
    BOOKING_REPORTS = "Booking Reports"
    STOPS = "Stops"
    OTHER = "Other"
    VEHICLE_PURSUITS = "Vehicle Pursuits"
    BUDGETS_AND_FINANCES = "Budgets & Finances"

class RecordTypeCoarse(Enum):
    INFO_ABOUT_AGENCIES = "Info About Agencies"
    NOT_CRIMINAL_JUSTICE_RELATED = "Not Criminal Justice Related"
    AGENCY_PUBLISHED_RESOURCES = "Agency-Published Resources"
    POOR_DATA_SOURCE = "Poor Data Source"
    INFO_ABOUT_OFFICERS = "Info About Officers"
    POLICE_AND_PUBLIC_INTERACTIONS = "Police & Public Interactions"
    JAILS_AND_COURTS_SPECIFIC = "Jails & Courts Specific"
    OTHER = "Other"