from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from . import dao
from .forms import UserInfo, UserDialogs, Prompts


dialogs_titles = ['Role', 'Content']


def pagination_dialogs(request, user_id: int):
    user_dialogs = dao.get_user_dialogs(user_id=user_id)
    paginator = Paginator(user_dialogs, 20)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj


def pagination_users(request, users: tuple):
    paginator = Paginator(users, 20)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    return render(request, 'main/index.html')


def users(request):
    query = request.GET.get('q', '')
    list_titles = ['TelegramID', 'Name', 'Birth date', 'Birth time', 'Place of birth', 'Zodiac sign',
                   'Chinese zodiac', 'Gender', 'Language']
    if query:
        users = dao.get_search_for_users(query=query)
    else:
        users = dao.get_users()
    users_page_obj = pagination_users(request=request, users=users)
    return render(request, 'main/users.html', {'users_page_obj': users_page_obj,
                                               'list_titles': list_titles, })


def users_detail(request, user_id: int):
    activity = dao.get_user_activity(user_id=user_id)
    interest = dao.get_user_interest(user_id=user_id)
    last_request = dao.get_user_last_request(user_id=user_id)
    additional_data = dao.get_additional_data(user_id=user_id)
    dialogs_page_obj = pagination_dialogs(request=request, user_id=user_id)
    user_details = {'activity': activity, 'additional_data': additional_data, 'interest': interest,
                    'last_request': last_request, 'dialogs_page_obj': dialogs_page_obj}
    activity_titles = ['Engagement level', 'Last active date', 'Preferred communication',
                       'Notification opt in']
    additional_titles = ['User time zone', 'Lunar phase preference', 'Retrograde warning',
                         'Preferred astrology type']
    interest_titles = ['Interest love', 'Interest career', 'Interest money', 'Interest health',
                       'Interest family', 'Interest travel', 'Interest spirituality', 'Interest self development',
                       'Interest daily horoscope', 'Interest compatibility']
    last_request_titles = ['Last topic', 'Last question', 'Last advice given']
    context = {'user_details': user_details, 'activity_titles': activity_titles, 'additional_titles': additional_titles,
               'interest_titles': interest_titles, 'last_request_titles': last_request_titles,
               'dialogs_titles': dialogs_titles}
    return render(request, 'main/users_detail.html', context)


def update_user_info(request, user_id: int):
    error = ''
    user_info = dao.get_dictionary_user_info(user_id=user_id)
    form = UserInfo(data=user_info)

    context = {'form': form, 'error': error}

    if request.method == 'POST':
        form = UserInfo(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            data.pop('csrfmiddlewaretoken', None)
            dao.update_user_info(values=data, user_id=user_id)
            context['form'] = form
        else:
            context['error'] = 'The form is filled out incorrectly'

    return render(request, 'main/edit.html', context)


def view_dialogs(request, dialog_id: int):
    user_dialog = dao.get_dictionary_user_dialog(dialog_id)
    form = UserDialogs(data=user_dialog, readonly=True)

    context = {'form': form}

    return render(request, 'main/dialogs.html', context)


def update_dialog(request, dialog_id: int):
    error = ''
    user_dialog = dao.get_dictionary_user_dialog(dialog_id)
    form = UserDialogs(data=user_dialog)

    context = {'form': form, 'error': error, 'add_button': True}

    if request.method == 'POST':
        form = UserDialogs(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            data.pop('csrfmiddlewaretoken', None)
            dao.update_dialog(values=data, dialog_id=dialog_id)
            context['form'] = form
        else:
            context['error'] = 'The form is filled out incorrectly'

    return render(request, 'main/dialogs.html', context)


def delete_user(request, user_id: int):
    if request.method == 'POST':
        dao.remove_user(user_id=user_id)
        return redirect(f'/users')
    return render(request, 'main/delete_items.html')


def delete_dialog(request, dialog_id: int, user_id: int):
    if request.method == 'POST':
        dao.remove_dialog(dialog_id=dialog_id)
        return redirect(f'/users/{user_id}')
    return render(request, 'main/delete_items.html')


def ai_settings(request):
    prompts_titles = ['SystemPrompt', 'SoftPrompt']
    prompts = dao.get_prompts()

    context = {'prompts': prompts, 'prompts_titles': prompts_titles}

    return render(request, 'ai_settings/ai_settings.html', context)


def view_prompts(request):
    prompts = dao.get_dictionary_prompts()
    form = Prompts(data=prompts, readonly=True)

    context = {'form': form}

    return render(request, 'main/dialogs.html', context)


def update_prompts(request, prompts_id: int):
    error = ''
    prompts = dao.get_dictionary_prompts()
    form = Prompts(data=prompts)

    context = {'form': form, 'error': error, 'add_button': True}

    if request.method == 'POST':
        form = Prompts(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            data.pop('csrfmiddlewaretoken', None)
            dao.update_prompts(values=data, prompts_id=prompts_id)
            context['form'] = form
        else:
            context['error'] = 'The form is filled out incorrectly'

    return render(request, 'main/dialogs.html', context)
