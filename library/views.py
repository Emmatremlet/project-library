
from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from django.contrib.contenttypes.models import ContentType
from .models import Member, Book, DVD, CD, BoardGame, Borrow
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('username')
        UserModel = get_user_model()
        user = UserModel.objects.filter(email=email).first()

        if user is None:
            raise forms.ValidationError("Cet email n'existe pas.")

        return cleaned_data

class MemberUpdateForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'email']
        


        
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']
        
class CDForm(forms.ModelForm):
    class Meta:
        model = CD
        fields = ['title', 'artist']
        

class DVDForm(forms.ModelForm):
    class Meta:
        model = DVD
        fields = ['title', 'director']
        

class BoardGameForm(forms.ModelForm):
    class Meta:
        model = BoardGame
        fields = ['title', 'creator']
        

def base_views(request): 
    return render(request, 'base.html', {'user': request.user})


class MemberCreationForm(forms.ModelForm):
    
    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'email', 'is_staff')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
    
    
def register_view(request):
    if request.method == 'POST':
        form = MemberCreationForm(request.POST)
        if form.is_valid():
            member = form.save()
            member.is_active = True
            member.save()
            login(request, member)
            return redirect('home')
    else:
        form = MemberCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Vous êtes connecté avec succès.', extra_tags='login')
            return redirect('home')
        else:
            messages.error(request, 'Identifiants invalides.', extra_tags='login')
    else:
        form = EmailAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def home_view(request):

    members = Member.objects.all()
    media_type = request.GET.get('media_type', None)
    
    if media_type == "book":
        medias = Book.objects.all()
        return render(request, 'home.html', {'medias': medias, 'members': members, 'user': request.user})
    elif media_type == "cd":
        medias = CD.objects.all()
        return render(request, 'home.html', {'medias': medias, 'members': members, 'user': request.user})
    elif media_type == "dvd": 
        medias = DVD.objects.all()
        return render(request, 'home.html', {'medias': medias, 'members': members, 'user': request.user})
    elif media_type == "boardgame": 
        medias = BoardGame.objects.all()
        return render(request, 'home.html', {'medias': medias, 'members': members, 'user': request.user})
    else:
        books = Book.objects.all()
        dvds = DVD.objects.all()
        cds = CD.objects.all()
        board_games = BoardGame.objects.all()
        medias = list(books) + list(dvds) + list(cds) + list(board_games)

    return render(request, 'home.html', {'medias': medias, 'members': members, 'user': request.user})


def add_media(request):
    media_type = request.GET.get('media_type', None)
    form = BookForm(request.POST)
    
    if media_type == "book":
        if request.method == 'POST':
            form = BookForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')  
        else:
            form = BookForm()    
    elif media_type == "cd":
        if request.method == 'POST':
            form = CDForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')  
        else:
            form = CDForm()    
    elif media_type == "dvd": 
        if request.method == 'POST':
            form = DVDForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')  
        else:
            form = DVDForm()
    elif media_type == "boardgame": 
        if request.method == 'POST':
            form = BoardGameForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')  
        else:
            form = BoardGameForm()

    return render(request, 'media_form.html', {'form': form})


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
        return redirect('home')
    return render(request, 'member_form.html', {'member': member})

@login_required
def member_update(request, pk):
    member = get_object_or_404(Member, pk=pk)

    if request.method == 'POST':
        form = MemberUpdateForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MemberUpdateForm(instance=member)

    return render(request, 'member_form.html', {'form': form})

def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    member.delete()
    return redirect('home')


def borrow_delete(request, pk):
    borrow = get_object_or_404(Borrow, pk=pk)

    media = borrow.media
    media.is_borrowed = False
    media.save()

    member = borrow.member
    member.too_much -= 1
    member.save()

    borrow.delete()

    messages.success(request, 'Emprunt supprimé avec succès.',  extra_tags='borrow')
    return redirect('borrow_create')

def borrow_return (request, pk):
    borrow = get_object_or_404(Borrow, pk=pk)
    borrow.return_media = True
    borrow.save()
    
    messages.success(request, 'Emprunt retourné avec succès.', extra_tags='borrow')
    return redirect('borrow_create')
    

def default_return_date(date):
    return date + timedelta(weeks=1)

@login_required
def borrow_create(request):
    members = Member.objects.all()
    books = Book.objects.filter(is_borrowed=False)
    dvds = DVD.objects.filter(is_borrowed=False)
    cds = CD.objects.filter(is_borrowed=False)
    user = request.user
    borrows = Borrow.objects.all()
    

    if request.method == "POST":
        member_id = request.POST['member']
        media_id = request.POST['media']
        media_type = request.POST['media_type']

        member = get_object_or_404(Member, id=member_id)
        content_type = get_object_or_404(ContentType, model=media_type)
        media_class = content_type.model_class()
        media = get_object_or_404(media_class, id=media_id)
        
        has_late_returns = Borrow.objects.filter(
            member=member,
            return_date__lt=timezone.now().date()
        ).exists()
        
        if has_late_returns:
            messages.error(request, 'Vous avez au moins un emprunt en retard.', extra_tags='borrow')
            return redirect('borrow_create')
        elif member.too_much >= 3:
            messages.error(request, 'Vous avez déjà 3 emprunts.', extra_tags='borrow')
            return redirect('borrow_create')
        else:
            member.too_much += 1
            member.save()
            
            media.is_borrowed = True
            media.save()
            
            borrow = Borrow(member=member, content_type=content_type, object_id=media_id)
            borrow.save()
            
            messages.success(request, 'Emprunt effectué avec succès.', extra_tags='borrow')
            return redirect('borrow_create')

    return render(request, 'borrow_form.html', {
        'books': books,
        'cds': cds,
        'dvds': dvds,
        'members': members,
        'borrows': borrows,
    })
    
def member_create(request):
    if request.method == 'POST':
        form = MemberCreationForm(request.POST)
        if form.is_valid():
            member = form.save()
            member.is_active = True
            member.save()
            messages.success(request, 'Membre créé avec succès.', extra_tags='member')
            return redirect('member_create')
    else:
        form = MemberCreationForm()
    return render(request, 'member_create.html', {'form': form})