import json
from uuid import uuid4

import requests


class BlipRequest:
    def __init__(self, authorization) -> None:
        self.authorization: str = authorization
        self.url: str = "https://intelbras.http.msging.net/commands"
        self.headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Authorization": self.authorization,
        }

    def get_teams(self):
        payload = {
            "id": f"{uuid4()}",
            "to": "postmaster@desk.msging.net",
            "method": "get",
            "uri": "/teams",
        }

        response = requests.post(
            url=self.url, data=json.dumps(payload), headers=self.headers
        )

        return json.loads(response.content)

    def get_report_about_teams(self, begin_date: str, end_date: str):
        payload = {
            "id": f"{uuid4()}",
            "to": "postmaster@desk.msging.net",
            "method": "get",
            "uri": f"/analytics/reports/teams?beginDate={begin_date}&endDate={end_date}",
        }

        response = requests.post(
            url=self.url, data=json.dumps(payload), headers=self.headers
        )

        return json.loads(response.content)

    def get_agents_productivity(self, begin_date: str, end_date: str):
        payload = {
            "id": f"{uuid4()}",
            "to": "postmaster@desk.msging.net",
            "method": "get",
            "uri": f"/analytics/reports/attendants/productivity?beginDate={begin_date}&endDate={end_date}",
        }

        response = requests.post(
            url=self.url, data=json.dumps(payload), headers=self.headers
        )

        return json.loads(response.content)

    def get_agents_metrics(self):
        payload = {
            "id": f"{uuid4()}",
            "to": "postmaster@desk.msging.net",
            "method": "get",
            "uri": "/monitoring/attendants?version=2",
        }

        response = requests.post(
            url=self.url, data=json.dumps(payload), headers=self.headers
        )

        return json.loads(response.content)
