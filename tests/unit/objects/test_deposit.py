import unittest

from quickbooks import QuickBooks
from quickbooks.objects.deposit import Deposit, DepositLine, CashBackInfo, DepositLineDetail
from quickbooks.objects.base import LinkedTxn


class DepositTests(unittest.TestCase):
    def test_unicode(self):
        deposit = Deposit()
        deposit.TotalAmt = 100

        self.assertEqual(str(deposit), "100")

    def test_valid_object_name(self):
        obj = Deposit()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)


class DepositLineTests(unittest.TestCase):
    def test_unicode(self):
        deposit = DepositLine()
        deposit.Amount = 100

        self.assertEqual(str(deposit), "100")

    def test_init_no_detail_type(self):
        deposit_line = DepositLine()
        self.assertFalse(hasattr(deposit_line, 'DetailType'))

    def test_to_dict_with_linked_txn(self):
        deposit_line = DepositLine()
        deposit_line.Amount = 100

        linked_txn = LinkedTxn()
        linked_txn.TxnId = "123"
        linked_txn.TxnType = "Payment"
        linked_txn.TxnLineId = 0
        deposit_line.LinkedTxn.append(linked_txn)

        result = deposit_line.to_dict()
        self.assertNotIn('DetailType', result)
        self.assertEqual(result['Amount'], 100)
        self.assertEqual(len(result['LinkedTxn']), 1)


class CashBackInfoTests(unittest.TestCase):
    def test_init(self):
        cash_back_info = CashBackInfo()

        self.assertEqual(cash_back_info.Amount, 0)
        self.assertEqual(cash_back_info.Memo, "")
        self.assertEqual(cash_back_info.AccountRef, None)


class DepositLineDetailTests(unittest.TestCase):
    def test_init(self):
        detail = DepositLineDetail()

        self.assertEqual(detail.Entity, None)
        self.assertEqual(detail.ClassRef, None)
        self.assertEqual(detail.AccountRef, None)
        self.assertEqual(detail.PaymentMethodRef, None)
        self.assertEqual(detail.CheckNum, "")
        self.assertEqual(detail.TxnType, None)
