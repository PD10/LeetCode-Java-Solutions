from fastapi import Depends
from starlette.requests import Request
from app.commons.service import BaseService
from app.commons.providers.dsj_client import DSJClient
from app.payout.core.account.processor import PayoutAccountProcessors
from app.payout.repository.bankdb import payout, stripe_payout_request
from app.payout.repository.maindb import (
    payment_account,
    stripe_transfer,
    transfer,
    managed_account_transfer,
)

__all__ = [
    "create_payout_account_processors",
    "PayoutService",
    "PaymentAccountRepository",
    "PaymentAccountRepositoryInterface",
    "TransferRepository",
    "TransferRepositoryInterface",
    "PayoutRepository",
    "PayoutRepositoryInterface",
    "StripePayoutRequestRepository",
    "StripePayoutRequestRepositoryInterface",
    "ManagedAccountTransferRepository",
    "ManagedAccountTransferRepositoryInterface",
]

PaymentAccountRepositoryInterface = payment_account.PaymentAccountRepositoryInterface
TransferRepositoryInterface = transfer.TransferRepositoryInterface
PayoutRepositoryInterface = payout.PayoutRepositoryInterface
StripePayoutRequestRepositoryInterface = (
    stripe_payout_request.StripePayoutRequestRepositoryInterface
)
StripeTransferRepositoryInterface = stripe_transfer.StripeTransferRepositoryInterface
ManagedAccountTransferRepositoryInterface = (
    managed_account_transfer.ManagedAccountTransferRepositoryInterface
)


class PayoutService(BaseService):
    service_name = "payout-service"
    payment_accounts: payment_account.PaymentAccountRepository
    transfers: transfer.TransferRepository
    payouts: payout.PayoutRepository
    stripe_payout_requests: stripe_payout_request.StripePayoutRequestRepository
    stripe_transfers: stripe_transfer.StripeTransferRepository
    managed_account_transfers: managed_account_transfer.ManagedAccountTransferRepository
    dsj_client: DSJClient

    def __init__(self, request: Request):
        super().__init__(request)

        # maindb
        maindb = self.app_context.payout_maindb
        self.payment_accounts = payment_account.PaymentAccountRepository(maindb)
        self.transfers = transfer.TransferRepository(maindb)
        self.stripe_transfers = stripe_transfer.StripeTransferRepository(maindb)
        self.managed_account_transfers = managed_account_transfer.ManagedAccountTransferRepository(
            maindb
        )

        # bankdb
        bankdb = self.app_context.payout_bankdb
        self.payouts = payout.PayoutRepository(bankdb)
        self.stripe_payout_requests = stripe_payout_request.StripePayoutRequestRepository(
            bankdb
        )

        # dsj_client
        self.dsj_client = self.app_context.dsj_client


async def GetPayoutService(request: Request):
    return PayoutService(request)


def PaymentAccountRepository(
    payout_service: PayoutService = Depends(GetPayoutService)
) -> payment_account.PaymentAccountRepositoryInterface:
    return payout_service.payment_accounts


def TransferRepository(
    payout_service: PayoutService = Depends(GetPayoutService)
) -> transfer.TransferRepository:
    return payout_service.transfers


def PayoutRepository(
    payout_service: PayoutService = Depends(GetPayoutService)
) -> payout.PayoutRepositoryInterface:
    return payout_service.payouts


def StripePayoutRequestRepository(
    payout_service: PayoutService = Depends(GetPayoutService)
) -> stripe_payout_request.StripePayoutRequestRepositoryInterface:
    return payout_service.stripe_payout_requests


def StripeTransferRepository(
    payout_service: PayoutService = Depends(GetPayoutService)
) -> stripe_transfer.StripeTransferRepositoryInterface:
    return payout_service.stripe_transfers


def ManagedAccountTransferRepository(
    payout_service: PayoutService = Depends(GetPayoutService)
) -> managed_account_transfer.ManagedAccountTransferRepositoryInterface:
    return payout_service.managed_account_transfers


def DSJClientHandle(payout_service: PayoutService = Depends(GetPayoutService)):
    return payout_service.dsj_client


def create_payout_account_processors(
    payout_service: PayoutService = Depends(GetPayoutService)
):
    return PayoutAccountProcessors(
        logger=payout_service.log,
        payment_account_repo=payout_service.payment_accounts,
        stripe_transfer_repo=payout_service.stripe_transfers,
        stripe_payout_request_repo=payout_service.stripe_payout_requests,
    )
