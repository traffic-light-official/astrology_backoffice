import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.paginator import Paginator
from decouple import config


from .transactions import checkout_transaction
from . import dao


def pagination_transactions(request, users: tuple):
    paginator = Paginator(users, 20)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj


def transactions(request):
    query = request.GET.get('q', '')
    list_titles = ['TelegramID', 'Created', 'Payments Status', 'Amount', 'Currency']
    if query:
        users = dao.get_search_for_transactions(query=query)
    else:
        users = dao.get_transactions()
    transactions_page_obj = pagination_transactions(request=request, users=users)
    return render(request, 'transactions/transactions.html',
                  {'transactions_page_obj': transactions_page_obj, 'list_titles': list_titles})


def transaction_details(request, trans_id: str):
    list_titles = ['ID', 'TelegramID', 'Created', 'Currency', 'Presentment Amount', 'Presentment Currency', 'Payment Status',
                   'Amount Total', 'Quantity', 'Payments Account']
    transactions_details = dao.get_transactions_by_id(trans_id=trans_id)
    return render(request, 'transactions/transactions_detail.html',
                  {'transactions_details': transactions_details, 'list_titles': list_titles})


@csrf_exempt
def my_webhook_view(request):
    endpoint_secret = config('STRIPE_ENDPOINT_SECRET')
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
          payload, sig_header, endpoint_secret
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed' or event['type'] == 'checkout.session.async_payment_succeeded':
        checkout_transaction(event['data']['object']['id'])

    return HttpResponse(status=200)
