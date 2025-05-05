from django.shortcuts import redirect
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ai_settings, name='ai_settings'),
    path('prompts', views.view_prompts, name='view_prompts'),
    path('prompts/<int:prompts_id>', views.update_prompts, name='update_prompts'),
]
