from datetime import datetime

from fhir.resources.episodeofcare import EpisodeOfCare
from fhir.resources.period import Period
from fhir.resources.reference import Reference

CARE_PROFILE = (
    "http://hl7.dk/fhir/hackathons/StructureDefinition/TelemedicineEpisodeOfCare"
)

EPISODE_OF_CARE_EXTENSION = (
    "http://hl7.org/fhir/StructureDefinition/workflow-episodeOfCare"
)

PHYSICAL_ACTIVITY_PROFILE = (
    "http://hl7.dk/fhir/hackathons/StructureDefinition/PhysicalActivityObservation"
)


def create_care_episode(
    patient_id: str,
    start: datetime,
    end: datetime,
) -> EpisodeOfCare:
    patient_reference = Reference(reference=f"Patient/{patient_id}")
    return EpisodeOfCare(
        # id="HackathonEpisodeOfCare001",
        meta={"profile": [CARE_PROFILE]},
        status="active",
        patient=patient_reference,
        period=Period(
            start=start,
            end=end,
        ),
    )
