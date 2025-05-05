import stripe


def checkout_transaction(session_id: str):
    # if session_id in bd:
        # return

    checkout_session = stripe.checkout.Session.retrieve(
        session_id,
        expand=['line_items'],
    )

    if checkout_session.payment_status == 'paid':
        # save transactions
        # save additional user info
        # save astrals user
        pass
