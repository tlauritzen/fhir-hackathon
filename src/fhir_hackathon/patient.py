from fhir.resources.patient import Patient
import requests

patient_obj = {
    "resourceType": "Patient",
    "name": [{
        "use": "official",
        "family": "Testesen",
        "given": ["Testy"],
    }],
    "gender": "male",
    "telecom": [{
        "system": "email",
        "value": "testy@testesen.dk",
    }]
}

patient = Patient(**patient_obj)

patient_json_str = patient.model_dump_json(indent=2)
print(patient_json_str)

endpoint = "https://hapi.fhir.org/baseR4"

response = requests.post(endpoint + "/Patient", json=patient.model_dump())
patient_obj = response.json()
print(patient_obj)
patient = Patient(**patient_obj)
print(patient.id)

response = requests.delete(f"{endpoint}/Patient/{patient.id}")