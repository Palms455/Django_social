from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from actions.utils import create_action
from actions.models import Action


"""
LoginView - обрабочик входа
LogoutView - выход поль из под уч записи
PasswordChangeView - обраб формы смены пароля
PasswordChangeDoneView - обработчик на который будет перенаправлен п. после смены пароля
PasswordResetView - восстановл пароля
PasswordResetDoneView - перенаправл после смены пароля
PasswordResetConfirmView - указ новый пароль
PasswordResetCompView - сообщение об успешной смене пароля 
"""



def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            create_action(new_user, 'зарегистрировался')
            return render(request,
                          'registration/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'registration/register.html',
                  {'user_form': user_form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, # проверка пользователя
                                username=cd['username'],
                                password=cd['password'])
            if user:
                if user.is_active:
                    login(request, user) # сохраняет сессю пользователя
                    return HttpResponse('Вход выполнен')
                else:
                    return HttpResponse('Пользователен заблокирован')
            else:
                return HttpResponse('Неверный логин\пароль')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

@login_required
def dashboard(request):
    # По умолчанию отображаем все действия.
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',
                                                       flat=True)
    if following_ids:
        # Если текущий пользователь подписался на кого-то,
        # отображаем только действия этих пользователей.
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile') \
                  .prefetch_related('target')[:10]

    return render(request,
                  'account/dashboard.html',
                  {'section' : 'dashboard',
                   'actions' : actions})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})
# success()– сообщение об успешном завершении действия;
# info()– информационное сообщение;
# warning() – что-то пошло не так, но пока ошибка не критична;
# error()– действие не завершилось или произошла ошибка;
# debug() – отладочное сообщение, которое не будет отображаться в боевом окружении


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'account/user/list.html',
                  {'section': 'people',
                   'user': users})
@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'account/user/detail.html',
                  {'section': 'people',
                   'user': user})

@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, 'подписался на ', user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except UserDoesNotExist:
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status' : 'ok'})