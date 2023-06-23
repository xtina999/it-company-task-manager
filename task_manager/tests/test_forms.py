from django.test import TestCase

from task_manager.forms import (
    WorkerCreateForm,
    WorkerUpdateForm,
    WorkerAccountsUpdateForm
)
from task_manager.models import Position


class FormsTests(TestCase):

    def test_worker_creation_form_with_position_first_last_name_is_valid(
            self
    ):
        position = Position.objects.create(name="PositionTests")
        form_data = {
            "username": "new_user",
            "password": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "position": position
        }
        form = WorkerCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_worker_update_form_last_name_position_is_valid(
            self
    ):
        position = Position.objects.create(name="PositionTests")
        form_data = {
            "last_name": "Test last",
            "position": position
        }
        form = WorkerUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_worker_update_form_for_account(
            self
    ):
        position = Position.objects.create(name="PositionTests")
        form_data = {
            "username": "new_user",
            "email": "em@gmail.com",
            "position": position,
            "first_name": "Test first",
            "last_name": "Test last",
        }
        form = WorkerAccountsUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
