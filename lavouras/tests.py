from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase


class BootstrapAdminTests(TestCase):
    credentials = {
        "DJANGO_SUPERUSER_USERNAME": "adminJG",
        "DJANGO_SUPERUSER_PASSWORD": "Temporary-Test!4829-Field",
    }

    def run_command(self, credentials):
        output = StringIO()
        with patch.dict("os.environ", credentials, clear=True):
            call_command("bootstrap_admin", stdout=output)
        return output.getvalue()

    def test_creates_admin_who_can_log_in(self):
        output = self.run_command(self.credentials)
        user = get_user_model().objects.get(username="adminJG")
        self.assertTrue(user.is_staff and user.is_superuser and user.is_active)
        self.assertEqual(user.email, "")
        self.assertTrue(self.client.login(
            username="adminJG", password=self.credentials["DJANGO_SUPERUSER_PASSWORD"]
        ))
        self.assertEqual(self.client.get("/admin/").status_code, 200)
        self.assertNotIn(self.credentials["DJANGO_SUPERUSER_PASSWORD"], output)

    def test_repeated_deploy_preserves_password_and_email(self):
        self.run_command(self.credentials)
        self.run_command({**self.credentials, "DJANGO_SUPERUSER_PASSWORD": "Changed!7592", "DJANGO_SUPERUSER_EMAIL": "other@example.com"})
        user = get_user_model().objects.get(username="adminJG")
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertTrue(user.check_password(self.credentials["DJANGO_SUPERUSER_PASSWORD"]))
        self.assertEqual(user.email, "")

    def test_does_not_promote_existing_regular_user(self):
        user = get_user_model().objects.create_user(username="adminJG", password="Existing!3728")
        self.run_command(self.credentials)
        user.refresh_from_db()
        self.assertFalse(user.is_staff or user.is_superuser)
        self.assertTrue(user.check_password("Existing!3728"))

    def test_unconfigured_deploy_skips_creation(self):
        self.run_command({})
        self.assertFalse(get_user_model().objects.exists())

    def test_partial_configuration_fails_without_creating_user(self):
        for name in self.credentials:
            with self.subTest(missing=name):
                values = dict(self.credentials)
                del values[name]
                with self.assertRaises(CommandError):
                    self.run_command(values)
                self.assertFalse(get_user_model().objects.exists())

    def test_invalid_credentials_fail_without_exposing_password(self):
        invalid_values = (
            {"DJANGO_SUPERUSER_USERNAME": "invalid user"},
            {"DJANGO_SUPERUSER_EMAIL": "invalid-email"},
            {"DJANGO_SUPERUSER_PASSWORD": "12345678"},
        )
        for values in invalid_values:
            with self.subTest(values=values):
                credentials = {**self.credentials, **values}
                with self.assertRaises(CommandError) as error:
                    self.run_command(credentials)
                self.assertNotIn(credentials["DJANGO_SUPERUSER_PASSWORD"], str(error.exception))
                self.assertFalse(get_user_model().objects.exists())
