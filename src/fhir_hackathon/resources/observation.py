from datetime import datetime

from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.extension import Extension
from fhir.resources.observation import Observation
from fhir.resources.period import Period
from fhir.resources.quantity import Quantity
from fhir.resources.reference import Reference

SLEEP_PROFILE = "http://hl7.dk/fhir/hackathons/StructureDefinition/SleepObservation"

EPISODE_OF_CARE_EXTENSION = (
    "http://hl7.org/fhir/StructureDefinition/workflow-episodeOfCare"
)

PHYSICAL_ACTIVITY_PROFILE = (
    "http://hl7.dk/fhir/hackathons/StructureDefinition/PhysicalActivityObservation"
)


def create_observation(
    patient_id: str,
    episode_of_care_id: str,
    hours: float,
    start: datetime,
    end: datetime,
    code: str,
    sleep_profile: bool = True,
) -> Observation:
    patient_reference = Reference(reference=f"Patient/{patient_id}")
    if sleep_profile:
        return Observation(
            meta={
                "profile": [SLEEP_PROFILE]
                if sleep_profile
                else [PHYSICAL_ACTIVITY_PROFILE]
            },
            extension=[
                Extension(
                    url=EPISODE_OF_CARE_EXTENSION,
                    valueReference=Reference(
                        reference=f"EpisodeOfCare/{episode_of_care_id}"
                    ),
                )
            ],
            status="final",
            code=CodeableConcept(
                coding=[
                    Coding(
                        system="http://snomed.info/sct",
                        code=code,
                        display="Duration of sleep",
                    )
                ]
            ),
            subject=patient_reference,
            effectivePeriod=Period(
                start=start,
                end=end,
            ),
            performer=[patient_reference],
            valueQuantity=Quantity(
                value=hours,
            ),
        )
    else:
        return Observation(
            meta={
                "profile": [SLEEP_PROFILE]
                if sleep_profile
                else [PHYSICAL_ACTIVITY_PROFILE]
            },
            extension=[
                Extension(
                    url=EPISODE_OF_CARE_EXTENSION,
                    valueReference=Reference(
                        reference=f"EpisodeOfCare/{episode_of_care_id}"
                    ),
                )
            ],
            status="final",
            code=CodeableConcept(
                coding=[
                    Coding(
                        system="http://snomed.info/sct",
                        code=code,
                        display="Duration of sleep",
                    )
                ]
            ),
            subject=patient_reference,
            effectivePeriod=Period(
                start=start,
                end=end,
            ),
            performer=[patient_reference],
        )
