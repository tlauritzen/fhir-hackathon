"""A fictional Patient without a CPR number or contact details."""

from fhir.resources.humanname import HumanName
from fhir.resources.identifier import Identifier
from fhir.resources.patient import Patient

# A private test identifier namespace, not a CodeSystem or national identifier.
PATIENT_IDENTIFIER_SYSTEM = "https://example.org/fhir-hackathon/patient-identifiers"
PATIENT_IDENTIFIER_VALUE = "hl7-dk-telemedicine-fake-patient-001"


def create_test_patient() -> Patient:
    """Build and validate a generic R4 Patient; no profile compliance is claimed."""
    return Patient(
        active=True,
        identifier=[
            Identifier(system=PATIENT_IDENTIFIER_SYSTEM, value=PATIENT_IDENTIFIER_VALUE)
        ],
        name=[HumanName(family="HackathonTest", given=["FictionalPatient"])],
    )


def create_patient(family, given, identifier_value) -> Patient:
    """Build and validate a generic R4 Patient; no profile compliance is claimed."""
    return Patient(
        active=True,
        identifier=[
            Identifier(system=PATIENT_IDENTIFIER_SYSTEM, value=identifier_value)
        ],
        name=[HumanName(family=family, given=[given])],
    )
