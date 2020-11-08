from django.test import TestCase, Client
from django.utils.datetime_safe import datetime, date
from rest_framework import status
from django.urls import reverse

from accounts.models import Account
from accounts.serializers import AccountSerializer

from transactions.models import Transaction

client = Client()


class CreateNewAccountTest(TestCase):

    def setUp(self) -> None:
        self.valid_payload = {"name": "Test", }
        self.invalid_payload = {"names": "Test2", }

    def test_create_valid_payload(self):
        response = client.post(reverse("accounts-list"),
                               data=self.valid_payload,
                               content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_payload(self):
        response = client.post(reverse("accounts-list"),
                               data=self.invalid_payload,
                               content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetAllAccountsTest(TestCase):

    def setUp(self) -> None:
        self.account = Account.objects.create(name="Test")
        self.account2 = Account.objects.create(name="Test2")

    def test_get_all_accounts(self):
        response = client.get(reverse("accounts-list"))

        accounts = Account.objects.get_queryset().order_by('id')
        serializer = AccountSerializer(accounts, many=True)

        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetFilteredAccountsTest(TestCase):

    def setUp(self) -> None:
        self.account = Account.objects.create(name="Test")
        self.account_open_date = self.account.opened_at

        self.account2 = Account.objects.create(name="Test2")
        self.account3 = Account.objects.create(name="Test3", opened_at=datetime(2020, 10, 10))

        Transaction.objects.create(account=self.account,
                                   amount=300,
                                   type="C")

    def test_filter_by_name(self):
        response = client.get(reverse("accounts-list") + f"?name={self.account2.name}")

        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_opening_date(self):
        response = client.get(reverse("accounts-list") + f"?opened_at={self.account_open_date}")

        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_new_accounts(self):
        response = client.get(reverse("accounts-list") + f"?is_new=true")

        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_active_accounts(self):
        response = client.get(reverse("accounts-list") + f"?is_active=true")

        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleAccountTest(TestCase):

    def setUp(self) -> None:
        self.account = Account.objects.create(name="Test")

    def test_get_single_account(self):
        response = client.get(reverse('accounts-detail', kwargs={'pk': self.account.id}))

        serializer = AccountSerializer(self.account)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_account(self):
        response = client.get(reverse('accounts-detail', kwargs={'pk': 2}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetTopAccountsTest(TestCase):

    def setUp(self) -> None:
        self.account = Account.objects.create(name="Test")
        self.account2 = Account.objects.create(name="Test2")
        self.account3 = Account.objects.create(name="Test3")
        self.account4 = Account.objects.create(name="Test4")
        self.account5 = Account.objects.create(name="Test5")

        Transaction.objects.create(account=self.account, amount=300, type="C")
        Transaction.objects.create(account=self.account2, amount=500, type="C")
        Transaction.objects.create(account=self.account3, amount=100, type="D")

    def test_get_top_account(self):
        response = client.get(reverse("accounts-list-get-top"))

        self.assertEqual(response.data['count'], 2)


class UpdateAccountTest(TestCase):

    def setUp(self) -> None:
        self.account = Account.objects.create(name="Test")

        self.valid_payload = {
            "name": "Test1",
            "opened_at": date.today()
        }
        self.invalid_payload = {
            "names": "Test1",
            "opened_at": date.today()
        }

    def test_valid_update_account(self):
        response = client.put(reverse("accounts-detail", kwargs={'pk': self.account.id}),
                              data=self.valid_payload,
                              content_type="application/json")

        serializer = AccountSerializer(self.account)

        self.assertNotEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_account(self):
        response = client.put(reverse("accounts-detail", kwargs={'pk': self.account.id}),
                              data=self.invalid_payload,
                              content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PatchAccountTest(TestCase):

    def setUp(self) -> None:
        self.account = Account.objects.create(name="Test")

        self.valid_payload = {
            "name": "Test1",
        }
        self.invalid_payload = {
            "opened_at": "today"
        }

    def test_valid_patch_account(self):
        response = client.patch(reverse("accounts-detail", kwargs={'pk': self.account.id}),
                                data=self.valid_payload,
                                content_type="application/json")

        serializer = AccountSerializer(self.account)

        self.assertNotEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_patch_account(self):
        response = client.patch(reverse("accounts-detail", kwargs={'pk': self.account.id}),
                                data=self.invalid_payload,
                                content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteAccountTest(TestCase):

    def setUp(self) -> None:
        self.account = Account.objects.create(name="Test")

    def test_delete_existent_account(self):
        response = client.delete(reverse("accounts-detail", kwargs={'pk': self.account.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_nonexistent_account(self):
        response = client.delete(reverse("accounts-detail", kwargs={'pk': 2}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
