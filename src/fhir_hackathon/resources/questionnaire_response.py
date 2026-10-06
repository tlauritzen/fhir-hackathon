from datetime import datetime

from fhir.resources.coding import Coding
from fhir.resources.extension import Extension
from fhir.resources.questionnaireresponse import (
    QuestionnaireResponse,
    QuestionnaireResponseItem,
    QuestionnaireResponseItemAnswer,
)
from fhir.resources.reference import Reference

PROFILE = (
    "http://hl7.dk/fhir/hackathons/"
    "StructureDefinition/TelemedicineQuestionnaireResponse"
)

EPISODE_OF_CARE_EXTENSION = (
    "http://hl7.org/fhir/StructureDefinition/workflow-episodeOfCare"
)

QUESTIONNAIRE = "http://hl7.org/fhir/Questionnaire/MentalHealthQuestionnaire"

MENTAL_HEALTH_CODES = (
    "http://hl7.dk/fhir/Hackathon-Sep-2022/CodeSystem/MentalHealthCodes"
)


def coded_answer(code: str, display: str) -> QuestionnaireResponseItemAnswer:
    return QuestionnaireResponseItemAnswer(
        valueCoding=Coding(
            system=MENTAL_HEALTH_CODES,
            code=code,
            display=display,
        )
    )


def question(
    link_id: str,
    text: str,
    code: str,
    display: str,
) -> QuestionnaireResponseItem:
    return QuestionnaireResponseItem(
        linkId=link_id,
        text=text,
        answer=[coded_answer(code, display)],
    )


def create_questionnaire_response(
    patient_id: str,
    episode_of_care_id: str,
) -> QuestionnaireResponse:
    patient = Reference(reference=f"Patient/{patient_id}")

    return QuestionnaireResponse(
        meta={"profile": [PROFILE]},
        extension=[
            Extension(
                url=EPISODE_OF_CARE_EXTENSION,
                valueReference=Reference(
                    reference=f"EpisodeOfCare/{episode_of_care_id}"
                ),
            )
        ],
        questionnaire=QUESTIONNAIRE,
        status="completed",
        subject=patient,
        authored=datetime.now().astimezone(),
        source=patient,
        item=[
            # Fællesskab
            QuestionnaireResponseItem(
                linkId="1",
                item=[
                    question(
                        "1.1",
                        "Venskaber",
                        "60e95414-b97d-4197-af85-d5efc5628e86",
                        "Jeg føler mig tæt på mine venner",
                    ),
                    question(
                        "1.2",
                        "Lyst til at være sammen med andre",
                        "48405c96-5f94-4ccf-b9ef-44579da052a8",
                        "Nogle få gange ugentligt har jeg lyst til at være sammen med andre",
                    ),
                    question(
                        "1.3",
                        "Kærlighed",
                        "1a705260-cf44-4dd8-83fb-994baf656a6a",
                        "Jeg føler mig ikke elsket",
                    ),
                ],
            ),
            # Daglige opgaver
            QuestionnaireResponseItem(
                linkId="2",
                item=[
                    question(
                        "2.1",
                        "Arbejde/skole forventning",
                        "6eb62a15-8b69-4940-9276-704a0a1c0a60",
                        "Jeg gør det, der forventes",
                    ),
                    question(
                        "2.2",
                        "Pres",
                        "14293f45-25fc-48a1-b8be-918d44009e91",
                        "Jeg klarer ikke mine daglige opgaver",
                    ),
                ],
            ),
            # Følelser
            QuestionnaireResponseItem(
                linkId="3",
                item=[
                    question(
                        "3.1",
                        "Oplagthed",
                        "a5341a86-677d-4d53-84a1-498dc1a4ed42",
                        "Jeg føler mig klar og frisk de fleste dage",
                    ),
                    question(
                        "3.2",
                        "Humør",
                        "b9453f69-31a2-4a67-a453-569d7cd9691a",
                        "Jeg er glad",
                    ),
                ],
            ),
        ],
    )
