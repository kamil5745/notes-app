from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import View
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout
from document.models import Category, Note, Tag


class NoteSingleView(View):
    def get(self, request, slug):
        note = get_object_or_404(Note, slug=slug)
        return render(request, 'document/single.html', context={'note': note})

class NoteFilterView(View):
    def get(self, request):
        notes = Note.objects.all()

        category_slug = request.GET.get('category')
        if category_slug:
            notes = notes.filter(category__slug=category_slug)

        tags_slug = request.GET.getlist('tags')
        if tags_slug:
            notes = notes.filter(tags__slug__in=tags_slug)

        from_date = request.GET.get('from')
        if from_date:
            notes = notes.filter(created_at__date__gte=from_date)

        to_date = request.GET.get('to')
        if to_date:
            notes = notes.filter(created_at__date__lte=to_date)


        categories = Category.objects.all()
        tags = Tag.objects.all()

        return render(request, 'document/list.html', {
            'notes': notes,
            'categories': categories,
            'tags': tags,
            'selected_category': category_slug,
            'selected_tags': tags_slug,
        })


class NoteCreateView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login-view')
        categories = Category.objects.all()
        return render(request, 'document/create.html', context={'categories': categories})

#class NoteListView(View):
#    def get(self, request):
#        return render(request, 'document/list.html')


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