
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from .models import Member, Book, DVD, CD, BoardGame, Borrow
from django.utils import timezone


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
