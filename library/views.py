
from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from django.contrib.contenttypes.models import ContentType
from .models import Member, Book, DVD, CD, BoardGame, Borrow
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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


def base_views(request): 
    return render(request, 'base.html', {'user': request.user})


class MemberCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
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


# class LoginView(auth_views.LoginView):
#     template_name = 'login.html'


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
        return redirect('home')
    return render(request, 'member_form.html', {'member': member})


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

    messages.success(request, 'Emprunt supprimé avec succès.')
    return redirect('borrow_create')

def media_list(request):
    books = Book.objects.all()
    dvds = DVD.objects.all()
    cds = CD.objects.all()
    boardgames = BoardGame.objects.all()
    return render(request, 'media_list.html', {
        'books': books, 'dvds': dvds, 'cds': cds, 'boardgames': boardgames
    })

@login_required
def borrow_create(request):
    members = Member.objects.all()
    books = Book.objects.filter(is_borrowed=False)
    dvds = DVD.objects.filter(is_borrowed=False)
    cds = CD.objects.filter(is_borrowed=False)
    user = request.user
    borrows = Borrow.objects.filter(member=user)

    if request.method == "POST":
        member_id = request.POST['member']
        media_id = request.POST['media']
        media_type = request.POST['media_type']

        member = get_object_or_404(Member, id=member_id)
        content_type = get_object_or_404(ContentType, model=media_type)
        media_class = content_type.model_class()
        media = get_object_or_404(media_class, id=media_id)
        
        if member.borrowing_late:
            messages.error(request, 'Vous avez déjà un emprunt en retard.', extra_tags='borrow')
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