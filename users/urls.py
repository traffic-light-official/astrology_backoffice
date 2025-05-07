from django.shortcuts import redirect
from django.urls import path, include
from . import views

urlpatterns = [
    path('', lambda request: redirect('users', permanent=True)),
    path('users', views.users, name='users'),
    path('users/<int:user_id>', views.users_detail, name='users_detail'),
    path('users/<int:user_id>/update', views.update_user_info, name='user_info_update'),
    path('users/<int:user_id>/delete', views.delete_user, name='delete_user'),
    path('users/<int:dialog_id>/dialog/view', views.view_dialogs, name='view_dialog'),
    path('users/<int:dialog_id>/dialog/update', views.update_dialog, name='update_dialog'),
    path('users/<int:dialog_id>/<int:user_id>/dialog/delete', views.delete_dialog, name='delete_dialog'),
]
