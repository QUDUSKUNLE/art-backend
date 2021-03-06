# Standard Library
from unittest.mock import patch

# Third-Party Imports
from django.apps import apps
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

# App Imports
from api.serializers import AssetSerializer
from api.tests import APIBaseTestCase
from api.tests.test_user import User
from core.models import AllocationHistory, AssetStatus

client = APIClient()


class DepartmentTeamTestCase(APIBaseTestCase):
    """
    Test department teams api
    """

    def setUp(self):
        self.departmental_team = apps.get_model(
            "core", "DepartmentalTeam"
        ).objects.create(name="Accounts", department=self.department)
        self.departmental_team_1 = apps.get_model(
            "core", "DepartmentalTeam"
        ).objects.create(name="Travels", department=self.department)
        self.departmental_teams_url = reverse("departmental-teams-list")
        self.asset_assignee_team = apps.get_model(
            "core", "AssetAssignee"
        ).objects.create(team=self.departmental_team)

    def test_non_authenticated_user_get_department_teams(self):
        response = client.get(self.departmental_teams_url)
        self.assertEqual(
            response.data, {"detail": "Authentication credentials were not provided."}
        )

    @patch("api.authentication.auth.verify_id_token")
    def test_authenticated_user_get_department_teams(self, mock_verify_token):
        mock_verify_token.return_value = {"email": self.admin_user.email}
        response = client.get(
            self.departmental_teams_url,
            HTTP_AUTHORIZATION="Token {}".format(self.token_user),
        )
        data = response.json()
        # return types assertions
        self.assertTrue(isinstance(data['results'], list))
        self.assertTrue(isinstance(data['results'][0], dict))
        # results field assertions
        self.assertEqual(data['results'][0]['name'], self.departmental_team.name)
        self.assertEqual(
            data['results'][0]['description'], self.departmental_team.description
        )
        self.assertEqual(
            data['results'][0]['department'], self.departmental_team.department.id
        )
        self.assertEqual(
            data['count'],
            apps.get_model("core", "DepartmentalTeam").objects.all().count(),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("api.authentication.auth.verify_id_token")
    def test_authenticated_user_get_specific_department_teams_with_no_assets_assigned(
        self, mock_verify_token
    ):
        mock_verify_token.return_value = {"email": self.admin_user.email}
        url = "{}/{}/".format(self.departmental_teams_url, self.departmental_team_1.id)
        response = client.get(
            url, HTTP_AUTHORIZATION="Token {}".format(self.token_user)
        )
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue("assets_assigned" in data)
        self.assertEqual(
            data['assets_assigned']["count"], len(data['assets_assigned']['results'])
        )

    @patch("api.authentication.auth.verify_id_token")
    def test_authenticated_user_get_specific_department_teams_with_assets_assigned(
        self, mock_verify_token
    ):
        # add an asset with and assign it to a team
        new_asset = apps.get_model("core", "Asset").objects.create(
            asset_code="IC001489",
            serial_number="SN00123489",
            purchase_date="2018-07-10",
            model_number=self.assetmodel,
            asset_location=self.centre,
            department=self.department,
            team_name=self.departmental_team,
        )
        AssetStatus.objects.create(asset=new_asset, current_status="Available")
        allocation = AllocationHistory.objects.create(
            asset=new_asset, current_assignee=self.asset_assignee_team
        )
        # authenticate a user
        mock_verify_token.return_value = {"email": self.admin_user.email}
        url = "{}/{}/".format(self.departmental_teams_url, self.departmental_team.id)
        team_response = client.get(
            url, HTTP_AUTHORIZATION="Token {}".format(self.token_user)
        )

        data = team_response.json()
        self.assertEqual(team_response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['department']['id'], self.departmental_team.department.id)
        self.assertEqual(
            data['department']['name'], self.departmental_team.department.name
        )

        self.assertTrue("assets_assigned" in data)
        self.assertEqual(len(data['assets_assigned']['results']), 1)

        AllocationHistory.objects.get(id=allocation.id).delete()

    def test_new_asset_has_team_name_field(self):
        # add an asset with and assign it to a team
        asset = apps.get_model("core", "Asset").objects.create(
            asset_code="IC001489",
            serial_number="SN00123489",
            purchase_date="2018-07-10",
            model_number=self.assetmodel,
            asset_location=self.centre,
            department=self.department,
            team_name=self.departmental_team,
        )
        AssetStatus.objects.create(asset=asset, current_status="Available")
        AllocationHistory.objects.create(
            asset=asset, current_assignee=self.asset_assignee_team
        )
        asset = AssetSerializer(asset).data
        self.assertEqual(asset['assigned_to']['name'], self.departmental_team.name)
        self.assertEqual(asset['team_name'], self.departmental_team.name)

    @patch("api.authentication.auth.verify_id_token")
    def test_get_team_members(self, mock_verify_token):
        new_user = User.objects.create(
            email="test-user@andela.com",
            cohort=20,
            password="devpassword",
            team=self.departmental_team,
        )
        mock_verify_token.return_value = {"email": self.admin_user.email}
        url = "{}/{}/".format(self.departmental_teams_url, self.departmental_team.id)
        team_response = client.get(
            url, HTTP_AUTHORIZATION="Token {}".format(self.token_user)
        )
        data = team_response.json()
        self.assertTrue("members" in data)
        self.assertEqual(len(data["members"]["results"]), 1)
        self.assertEqual(data["members"]["results"][0]["email"], new_user.email)
        self.assertEqual(data["members"]["results"][0]["cohort"], new_user.cohort)
        self.assertEqual(team_response.status_code, status.HTTP_200_OK)

    @patch("api.authentication.auth.verify_id_token")
    def test_authenticated_user_add_department_teams(self, mock_verify_token):
        mock_verify_token.return_value = {"email": self.admin_user.email}
        payload = {
            "name": "Team 1",
            "description": "string",
            "department": self.department.id,
        }
        response = client.post(
            self.departmental_teams_url,
            data=payload,
            HTTP_AUTHORIZATION="Token {}".format(self.token_user),
        )
        data = response.json()

        self.assertTrue(isinstance(data, dict))
        self.assertEqual(data['name'], payload['name'])
        self.assertEqual(data['description'], payload['description'])
        self.assertEqual(data['department'], payload['department'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
