from enum import Enum


class MxTransactionType(str, Enum):
    """
    Enum definition of mx_transaction type.
    """

    MERCHANT_DELIVERY = "merchant_delivery"
    STORE_PAYMENT = "store_payment"
    DELIVERY_ERROR = "delivery_error"
    MICRO_DEPOSIT = "micro_deposit"
    NEGATIVE_BALANCE_ROLLOVER = "negative_balance_rollover"


class MxLedgerType(str, Enum):
    """
    Enum definition of mx_ledger type.
    """

    SCHEDULED = "scheduled"
    MICRO_DEPOSIT = "micro_deposit"
    MANUAL = "manual"


class MxLedgerStateType(str, Enum):
    """
    Enum definition of mx_ledger state.
    """

    OPEN = "open"
    PROCESSING = "processing"
    PAID = "paid"
    FAILED = "failed"
    ROLLED = "rolled"
    REVERSED = "reversed"
    SUBMITTED = "submitted"


class MxScheduledLedgerIntervalType(str, Enum):
    """
    Enum definition of mx_scheduled_ledger interval type.
    """

    WEEKLY = "weekly"
    DAILY = "daily"
