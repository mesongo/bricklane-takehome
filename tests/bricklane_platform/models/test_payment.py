import unittest
from datetime import datetime

from bricklane_platform.models.bank import Bank
from bricklane_platform.models.card import Card
from bricklane_platform.models.payment import Payment


class TestPayment(unittest.TestCase):

    def test_init(self):
        payment = Payment()

        self.assertIsNone(payment.customer_id)
        self.assertIsNone(payment.date)
        self.assertIsNone(payment.amount)
        self.assertIsNone(payment.fee)
        self.assertIsNone(payment.card_id)

    def test_init_with_data(self):

        data = {
            "source": "card",
            "amount": "2000",
            "card_id": "45",
            "card_status": "processed",
            "customer_id": "123",
            "date": "2019-02-01",
        }

        payment = Payment(data)

        self.assertEqual(payment.customer_id, 123)
        self.assertEqual(payment.date, datetime(2019, 2, 1))
        self.assertEqual(payment.amount, 1960)
        self.assertEqual(payment.fee, 40)

        card = payment.card

        self.assertIsInstance(card, Card)
        self.assertEqual(card.card_id, 45)
        self.assertEqual(card.status, "processed")

    def test_bank_is_successful(self):
        bank = Bank()
        payment = Payment()
        payment.source = "bank"
        payment.bank = bank

        self.assertTrue(payment.is_successful())

    def test_card_is_successful(self):
        card = Card()
        card.status = "processed"
        payment = Payment()
        payment.source = "card"
        payment.card = card

        self.assertTrue(payment.is_successful())

    def test_card_is_successful_declined(self):
        card = Card()
        card.status = "declined"
        payment = Payment()
        payment.source = "card"
        payment.card = card

        self.assertFalse(payment.is_successful())

    def test_card_is_successful_errored(self):
        card = Card()
        card.status = "errored"
        payment = Payment()
        payment.source = "card"
        payment.card = card

        self.assertFalse(payment.is_successful())

    def test_no_source_is_not_successful(self):
        card = Card()
        payment = Payment()
        payment.card = card

        self.assertFalse(payment.is_successful())
