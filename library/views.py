
from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from .models import Member, Book, DVD, CD, BoardGame, Borrow, Media
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

class MemberCreationForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'email')

def register_view(request):
    if request.method == 'POST':
        form = MemberCreationForm(request.POST)
        if form.is_valid():
            member = form.save()
            login(request, member)
            member.is_active == True
            return redirect('home')
    else:
        form = MemberCreationForm()
    return render(request, 'register.html', {'form': form})


class LoginView(auth_views.LoginView):
    template_name = 'login.html'

# def login_view(request):
    # if request.method == 'POST':
    #     form = AuthenticationForm(request, data=request.POST)
    #     if form.is_valid():
    #         email = form.cleaned_data.get('username')
    #         password = form.cleaned_data.get('password')
    #         member = authenticate(email=email, password=password)
    #         if user is not None:
    #             login(request, member)
    #             return redirect('home')
    #         else:
    #             messages.error(request, 'Mot de passe ou email invalide.')
    #             return render(request, 'register.html', {'form': form, 'error': 'Authentication failed.'})

    #     else:
    #         messages.error(request, 'Mot de passe ou email invalide.')
    # else:
    #     form = AuthenticationForm()
    # return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def home_view(request):
    books = Book.objects.all()
    dvds = DVD.objects.all()
    cds = CD.objects.all()
    board_games = BoardGame.objects.all()
    
    medias = list(books) + list(dvds) + list(cds) + list(board_games)
    
    members = Member.objects.all()
    return render(request, 'home.html', {'medias': medias, 'members': members})

def menu():
    return redirect('media_list')

def menu_librarian():
    return redirect ('member_list')


def member_list(request):
    members = Member.objects.all()
    return render(request, 'member_list.html', {'members': members})


def member_create(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        member = Member(first_name=first_name, last_name=last_name, email=email)
        member.save()
        return redirect('member_list')
    return render(request, 'member_form.html')


def member_update(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == "POST":
        member.first_name = request.POST['first_name']
        member.last_name = request.POST['last_name']
        member.email = request.POST['email']
        member.save()
        return redirect('member_list')
    return render(request, 'member_form.html', {'member': member})


def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    member.delete()
    return redirect('member_list')


def media_list(request):
    books = Book.objects.all()
    dvds = DVD.objects.all()
    cds = CD.objects.all()
    boardgames = BoardGame.objects.all()
    return render(request, 'media_list.html', {
        'books': books, 'dvds': dvds, 'cds': cds, 'boardgames': boardgames
    })


def borrow_create(request):
    if request.method == "POST":
        member_id = request.POST['member']
        media_type = request.POST['media_type']
        media_id = request.POST['media']
        return_date = request.POST['return_date']

        member = get_object_or_404(Member, id=member_id)
        content_type = get_object_or_404(ContentType, model=media_type)
        media = get_object_or_404(content_type.model_class(), id=media_id)

        borrow = Borrow(member=member, content_type=content_type, object_id=media_id, return_date=return_date)
        borrow.save()
        return redirect('media_list')
    return render(request, 'borrow_form.html')
