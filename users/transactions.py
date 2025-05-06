import stripe
from . import dao
from .schemas import TransactionInfo


def checkout_transaction(session_id: str):
    if session_id == dao.get_id_transaction(transaction_id=session_id):
        return

    checkout_session = stripe.checkout.Session.retrieve(
        session_id,
        expand=['line_items'],
    )

    transaction_info = TransactionInfo.model_validate(obj=checkout_session)

    if checkout_session.payment_status == 'paid':
        dao.create_transactions(values=transaction_info)
        dao.update_user_info(values={'email': transaction_info.email, 'country': transaction_info.country},
                             user_id=transaction_info.client_reference_id)
        astrals = dao.get_user_astrals(user_id=transaction_info.client_reference_id)
        astrals += transaction_info.quantity
        dao.update_astrals(values={'astrals': astrals}, user_id=transaction_info.client_reference_id)
