from django.shortcuts import redirect
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.transactions, name='transactions'),
    path('<str:trans_id>', views.transaction_details, name='transaction_details'),
    path('check/webhook', views.my_webhook_view, name='transactions_webhook'),
]
