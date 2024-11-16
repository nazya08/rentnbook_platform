from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages

from .forms import SignupForm, LoginForm


class HomeView(TemplateView):
    """
    Вигляд головної сторінки
    """
    template_name = 'default_auth/home.html'


class SignupView(FormView):
    """
    Вигляд реєстрації
    """
    template_name = 'default_auth/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form) -> HttpResponseRedirect:
        """
        Обробка даних після їх успішної валідації.
        :param form: екземпляр форми з перевіреними даними користувача.
        :return: HttpResponseRedirect: редирект на URL, зазначений в 'get_success_url'.
        """
        user = form.save(commit=False)
        user.is_active = True
        user.password = make_password(form.cleaned_data['password'])
        user.save()

        login(self.request, user)

        return HttpResponseRedirect(self.get_success_url())


class LoginView(FormView):
    """
    Обробка авторизації користувача.
    """
    template_name = 'default_auth/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """
        Авторизує та входить користувача.
        """
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Невірний email або пароль.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        """
        Обробка помилок форми.
        """
        messages.error(self.request, 'Будь ласка, виправте помилки нижче.')
        return self.render_to_response(self.get_context_data(form=form))


@login_required
def check_user(request):
    """
    Перевірка, чи авторизований користувач.
    :param request: Запит користувача.
    :return: редирект на інформаційну панель, якщо користувач авторизований, в іншому випадку редирект на головну сторінку.
    """
    user = request.user
    is_authenticated = user.is_authenticated

    context = {
        'user': user,
        'is_authenticated': is_authenticated,
    }
    return render(request, 'default_auth/home.html', context)


def logout_view(request):
    """
    Вигляд виходу з системи.
    :return: редирект на головну сторінку.
    """
    logout(request)
    return redirect(reverse_lazy('home'))
