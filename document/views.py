from django.shortcuts import render, redirect
from django.views.generic.detail import View
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout
from document.models import Category


class NoteCreateView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login-view')
        categories = Category.objects.all()
        return render(request, 'document/create.html', context={'categories': categories})

class NoteListView(View):
    def get(self, request):
        url_api = "/api/note/"
        url_search = "/notes/"
        return render(request, 'document/list.html', context={'url_api': url_api, 'url_search': url_search})


class LikedNoteListView(View):
    def get(self, request):
        url_api = "/api/note/liked/"
        url_search = "/notes/liked/"
        return render(request, 'document/list.html', context={'url_api': url_api, 'url_search': url_search})


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "document/register.html", context={
            "form": form,
        })

    def post(self, request):
        form = RegisterForm(request.POST)
        for fieldname in ['username', 'password1', 'password2']:
            form.fields[fieldname].help_text = None
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list-view')

        return render(request, "document/register.html", context={"form": form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "document/login.html", context={
            "form": form,
        })

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('list-view')
        return render(request, "document/login.html", context={"form": form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("login-view")