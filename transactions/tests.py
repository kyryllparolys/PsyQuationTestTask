from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse

from accounts.models import Account

from transactions.models import Transaction
from transactions.serializers import TransactionSerializer, TransactionAccIdSerializer

client = Client()


class CreateNewTransactionTest(TestCase):

    def setUp(self) -> None:
        Account.objects.create(name="Test")

        self.valid_payload = {"account": 1, "amount": 200, "type": "C"}
        self.invalid_payload = {"amount": 150, "type": "D"}

    def test_create_valid_payload(self):
        respone = client.post(
            reverse("transactions-list"),
            data=self.valid_payload,
            content_type="application/json",
        )
        self.assertEqual(respone.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_payload(self):
        response = client.post(
            reverse("transactions-list"),
            data=self.invalid_payload,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetAllTransactionsTest(TestCase):

    def setUp(self) -> None:
        self.account = Account.objects.create(name="Test")
        Transaction.objects.create(account=self.account, amount=300, type="C")
        Transaction.objects.create(account=self.account, amount=100, type="D")

    def test_get_all_transactions(self):
        response = client.get(reverse("transactions-list"))

        transactions = Transaction.objects.get_queryset().order_by("id")
        serializer = TransactionAccIdSerializer(transactions, many=True)

        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetFilteredTransactionsTest(TestCase):

    def setUp(self) -> None:
        self.account = Account.objects.create(name="Test")
        self.account2 = Account.objects.create(name="Test2")

        Transaction.objects.create(account=self.account, amount=300, type="C")
        Transaction.objects.create(account=self.account2, amount=300, type="C")

        Transaction.objects.create(account=self.account, amount=200, type="D")
        Transaction.objects.create(account=self.account2, amount=50, type="D")

    def test_filter_by_account(self):
        response = client.get(reverse("transactions-list") + f"?account={self.account.id}")

        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_by_amount(self):
        response = client.get(reverse("transactions-list") + "?amount=300")

        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_by_type(self):
        response = client.get(reverse("transactions-list") + "?type=C")
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleTransactionTest(TestCase):

    def setUp(self) -> None:
        self.account1 = Account.objects.create(name="Test")

        self.transaction1 = Transaction.objects.create(account=self.account1, amount=300, type="C")

    def test_get_single_transaction(self):
        response = client.get(reverse("transactions-detail", kwargs={"pk": self.transaction1.id}))
        serializer = TransactionAccIdSerializer(self.transaction1)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_transaction(self):
        response = client.get(reverse("transactions-detail", kwargs={"pk": 2}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateTransactionTest(TestCase):

    def setUp(self) -> None:
        self.account1 = Account.objects.create(name="Test")
        self.transaction1 = Transaction.objects.create(account=self.account1, amount=300, type="C")

        self.valid_payload = {
            "account": self.account1.id,
            "amount": 500,
            "type": "C"
        }
        self.invalid_payload = {
            "amount": 0,
            "type": "A"
        }

    def test_valid_update(self):
        response = client.put(reverse("transactions-detail", kwargs={'pk': self.transaction1.id}),
                              data=self.valid_payload,
                              content_type="application/json")

        serializer = TransactionAccIdSerializer(self.transaction1)

        self.assertNotEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_payload(self):
        response = client.put(reverse("transactions-detail", kwargs={'pk': self.transaction1.id}),
                              data=self.invalid_payload,
                              content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PatchTransactionTest(TestCase):

    def setUp(self) -> None:
        self.account1 = Account.objects.create(name="Test")
        self.transaction1 = Transaction.objects.create(account=self.account1, amount=300, type="C")

        self.valid_payload = {
            "amount": 500,
            "type": "C"
        }
        self.invalid_payload = {
            "type": "A"
        }

    def test_patch_valid_payload(self):
        response = client.patch(reverse("transactions-detail", kwargs={'pk': self.transaction1.id}),
                                data=self.valid_payload,
                                content_type="application/json")

        serializer = TransactionAccIdSerializer(self.transaction1)

        self.assertNotEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_invalid_payload(self):
        response = client.patch(reverse("transactions-detail", kwargs={'pk': self.transaction1.id}),
                                data=self.invalid_payload,
                                content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteTransactionTest(TestCase):

    def setUp(self) -> None:
        self.account1 = Account.objects.create(name="Test")

        self.transaction1 = Transaction.objects.create(account=self.account1, amount=300, type="C")

    def test_delete_existent_transaction(self):
        response = client.delete(reverse("transactions-detail", kwargs={'pk': self.transaction1.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_nonexistent_transaction(self):
        response = client.delete(reverse("transactions-detail", kwargs={'pk': 2}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
