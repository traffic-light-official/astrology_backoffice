from django.shortcuts import render
from . import dao
from . import forms


def ai_settings(request):
    prompts_titles = ['SystemPrompt', 'SoftPrompt']
    prompts = dao.get_prompts()

    context = {'prompts': prompts, 'prompts_titles': prompts_titles}

    return render(request, 'ai_settings/ai_settings.html', context)


def view_prompts(request):
    prompts = dao.get_dictionary_prompts()
    form = forms.Prompts(data=prompts, readonly=True)

    context = {'form': form}

    return render(request, 'users/dialogs.html', context)


def update_prompts(request, prompts_id: int):
    error = ''
    prompts = dao.get_dictionary_prompts()
    form = forms.Prompts(data=prompts)

    context = {'form': form, 'error': error, 'add_button': True}

    if request.method == 'POST':
        form = forms.Prompts(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            data.pop('csrfmiddlewaretoken', None)
            dao.update_prompts(values=data, prompts_id=prompts_id)
            context['form'] = form
        else:
            context['error'] = 'The form is filled out incorrectly'

    return render(request, 'users/dialogs.html', context)
