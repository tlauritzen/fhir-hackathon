"""A minimal synchronous FHIR R4 REST client."""

import os
import re
from pathlib import Path

import requests
from dotenv import load_dotenv
from fhir.resources import construct_fhir_element
from fhir.resources.resource import Resource


def get_fhir_base_url() -> str:
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
    url = os.getenv("FHIR_BASE_URL", "").strip().rstrip("/")

    return url


class FHIRClient:
    """Send and receive R4 models. Use as a context manager to close the Session."""

    def __init__(
        self,
        base_url: str,
        session: requests.Session | None = None,
        timeout: tuple[float, float] = (5, 30),
    ):
        self.base_url = base_url.rstrip("/")
        self.session = session if session is not None else requests.Session()
        self.timeout = timeout

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

    @staticmethod
    def _path(resource_type: str, resource_id: str | None = None) -> str:
        if not re.fullmatch(r"[A-Z][A-Za-z0-9]*", resource_type):
            raise ValueError("Invalid FHIR resource type.")
        if resource_id is None:
            return resource_type
        if not re.fullmatch(r"[A-Za-z0-9.-]{1,64}", resource_id):
            raise ValueError("Invalid FHIR resource ID.")
        return f"{resource_type}/{resource_id}"

    def _request(self, method: str, path: str, **kwargs) -> Resource | None:
        headers = {
            "Accept": "application/fhir+json",
            "Content-Type": "application/fhir+json",
        }
        if method in {"POST", "PUT"}:
            headers["Prefer"] = "return=representation"
        response = self.session.request(
            method,
            f"{self.base_url}/{path}",
            headers=headers,
            timeout=self.timeout,
            **kwargs,
        )
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise
        if response.status_code == 204 or not response.content:
            return None
        data = response.json()
        return construct_fhir_element(data["resourceType"], data)

    def capability_statement(self):
        return self._request("GET", "metadata")

    def create(self, resource: Resource):
        return self._request(
            "POST",
            self._path(resource.resource_type),
            data=resource.json(exclude_none=True),
        )

    def read(self, resource_type: str, resource_id: str):
        return self._request("GET", self._path(resource_type, resource_id))

    def search(self, resource_type: str, **params):
        return self._request("GET", self._path(resource_type), params=params)

    def update(self, resource: Resource):
        if not resource.id:
            raise ValueError("Updating a resource requires its server ID.")
        return self._request(
            "PUT",
            self._path(resource.resource_type, resource.id),
            data=resource.json(exclude_none=True),
        )

    def delete(self, resource_type: str, resource_id: str):
        return self._request("DELETE", self._path(resource_type, resource_id))
