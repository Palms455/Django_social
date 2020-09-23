from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile


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
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            # set_password зашифровывает пароль
            # create profile
            Profile.objects.create(user=new_user)
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})

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
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(isinstance=request.user, data=request.POST)
        profile_form = ProfileEditForm(isinstance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm()
        profile_form = ProfileEditForm()
    return render(request, 'account/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form})
