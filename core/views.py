from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View

from core.forms import AuthForm
from core.models import User


def index(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(pk=user_id)
        context = {'is_auth': True, 'login': user.login}
    else:
        context = {'is_auth': False}
    return render(request, 'core/index.html', context=context)


class SignInView(View):
    def get(self, request):
        form = AuthForm()
        is_log_in = True
        context = {'form': form, 'is_log_in': is_log_in}
        return render(request, 'core/auth.html', context=context)

    def post(self, request):
        form = AuthForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(
                login=form.cleaned_data['login'],
                password=form.cleaned_data['password'],
            )
            context = {
                'is_auth': True,
                'login': new_user.login,
            }
            request.session['user_id'] = new_user.id
            return redirect(reverse('main'), context=context)
        else:
            context = {'form': form}
            return render(request, 'core/auth.html', context=context)


def logout_user(request):
    logout(request)
    request.session['user_id'] = False
    return redirect('main')


class LogInView(LoginView):
    form_class = AuthenticationForm
    template_name = 'core/auth.html'
    context = {'form': form_class}

    def get_success_url(self):
        return reverse_lazy('main')  # TODO привести к однообразию вход и регистрацию через django
