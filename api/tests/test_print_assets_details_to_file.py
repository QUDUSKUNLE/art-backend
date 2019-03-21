# Standard Library
from unittest.mock import patch

# Third-Party Imports
from django.apps import apps
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

# App Imports
from api.tests import APIBaseTestCase
from core.models import Asset

User = get_user_model()
client = APIClient()


class PrintAssetsDetailsTestCase(APIBaseTestCase):
    def test_non_authenticated_user_print_assets(self):
        response = client.get(self.print_asset_url)
        self.assertEqual(
            response.data, {"detail": "Authentication credentials were not provided."}
        )

    @patch("api.authentication.auth.verify_id_token")
    def test_non_admin_cannot_print_asset(self, mock_verify_id_token):
        mock_verify_id_token.return_value = {"email": self.user.email}
        response = client.get(
            self.print_asset_url, HTTP_AUTHORIZATION="Token {}".format(self.token_user)
        )
        self.assertEqual(response.status_code, 403)

    @patch("api.authentication.auth.verify_id_token")
    def test_authenticated_admin_can_print_assets(self, mock_verify_id_token):
        mock_verify_id_token.return_value = {"email": self.admin_user.email}
        response = client.get(
            self.print_asset_url, HTTP_AUTHORIZATION="Token {}".format(self.token_admin)
        )
        Asset.objects.count()
        self.assertEqual(response.status_code, 200)

    @patch("api.authentication.auth.verify_id_token")
    def test_authenticated_admin_cant_print_assets_in_diffrent_location(
        self, mock_verify_id_token
    ):
        country = apps.get_model("core", "Country").objects.create(name="Nigeria")
        centre = apps.get_model("core", "AndelaCentre").objects.create(
            name="Epic Towers", country=country
        )
        admin_user = User.objects.create_superuser(
            email="newadmin@site.com",
            cohort=2,
            slack_handle="@admin",
            password="adminZpassword",
            location=centre,
        )
        token_admin = "admintesttoken"
        mock_verify_id_token.return_value = {"email": admin_user.email}
        response = client.get(
            self.print_asset_url, HTTP_AUTHORIZATION="Token {}".format(token_admin)
        )
        self.assertEqual(response.status_code, 400)

    @patch("api.authentication.auth.verify_id_token")
    def test_authenticated_admin_put_not_allowed(self, mock_verify_id_token):
        mock_verify_id_token.return_value = {"email": self.admin_user.email}
        data = {}
        response = client.put(
            self.print_asset_url,
            data=data,
            HTTP_AUTHORIZATION="Token {}".format(self.token_admin),
        )
        self.assertEqual(response.data, {"detail": 'Method "PUT" not allowed.'})
        self.assertEqual(response.status_code, 405)

    @patch("api.authentication.auth.verify_id_token")
    def test_authenticated_admin_patch_not_allowed(self, mock_verify_id_token):
        mock_verify_id_token.return_value = {"email": self.admin_user.email}
        data = {}
        response = client.patch(
            self.print_asset_url,
            data=data,
            HTTP_AUTHORIZATION="Token {}".format(self.token_admin),
        )
        self.assertEqual(response.data, {"detail": 'Method "PATCH" not allowed.'})
        self.assertEqual(response.status_code, 405)

    @patch("api.authentication.auth.verify_id_token")
    def test_authenticated_admin_delete_not_allowed(self, mock_verify_id_token):
        mock_verify_id_token.return_value = {"email": self.admin_user.email}
        response = client.delete(
            self.print_asset_url, HTTP_AUTHORIZATION="Token {}".format(self.token_admin)
        )
        self.assertEqual(response.data, {"detail": 'Method "DELETE" not allowed.'})
        self.assertEqual(response.status_code, 405)
