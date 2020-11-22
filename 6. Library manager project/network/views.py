import json
import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Author, Loan, Genre, Books



def index(request):
    if request.method == "POST":
        query = request.POST["content"]
        author_results = Author.objects.filter(first_name__icontains=query) | Author.objects.filter(
            last_name__icontains=query)
        book_results = Books.objects.filter(title__icontains=query)
        genre_results = Genre.objects.filter(name__icontains=query)

        all_authors = Author.objects.all()

        return render(request, "network/index.html",
                      {'all_authors': all_authors, 'author_results': author_results, 'book_results': book_results, 'genre_results': genre_results})
    else:

        all_authors = Author.objects.all()
        return render(request, "network/index.html", {'all_authors': all_authors})


def author_profile(request, first_name, last_name):
    try:
        authors_profile = Author.objects.get(first_name=first_name, last_name=last_name)
        books_written = Books.objects.filter(author=authors_profile)
        return render(request, "network/profile.html",
                      {"profile": "author", "authors_profile": authors_profile, "books_written": books_written})
    except Author.DoesNotExist:
        return render(request, "network/error.html", {"error": "Author does not exist"})


def book_profile(request, book_title):
    try:
        book = Books.objects.get(title=book_title)
        loans_of_book = Loan.objects.filter(books=book).order_by('date_due')
        return render(request, "network/book_profile.html", {"user": request.user, "book": book, "loans_list": loans_of_book})
    except Books.DoesNotExist:
        return render(request, "network/error.html", {"error": "Book does not exist"})

def genre_profile(request, genre_name):
    try:
        genre = Genre.objects.get(name=genre_name)
        books_by_genre = Books.objects.filter(genre=genre)

        return render(request, "network/index.html",
                      {'genre': genre, 'book_results': books_by_genre})
    except Genre.DoesNotExist:
        return render(request, "network/error.html", {"error": "No books written of this genre"})



def profile(request):
    user_loans = Loan.objects.filter(member=request.user.username)
    return render(request, "network/profile.html", {'user': request.user,'profile': 'user', 'user_loans': user_loans})


def new_loan(request, book):
    if request.method == "POST":
        query = request.POST["loan"].split('-')
        date = datetime.date(int(query[0]), int(query[1]), int(query[2]))

        #check the day is yet to come
        if date < datetime.datetime.now().date():
            return render(request, "network/error.html", {"error": "We have already lived that day"})

        #check the member has not the maximum number of loaned books
        max_loans = 4
        if Loan.objects.filter(member=request.user.username).count() == max_loans:
            return render(request, "network/error.html", {"error": "Maximum number of books loaned."})

        if int(query[1]) == 12:
            due_date = datetime.date(int(query[0]) + 1, 1, int(query[2]))
        elif int(query[2]) == 1:
            due_date = datetime.date(int(query[0]), int(query[1]) + 1, int(query[2]))
        else:
            due_date = datetime.date(int(query[0]), int(query[1]) + 1, int(query[2])-1)

        is_loaned = Loan.objects.filter(date_of_loan__range=[date, due_date], books=Books.objects.get(title=book)) | Loan.objects.filter(date_due__range=[date, due_date], books=Books.objects.get(title=book))
        if is_loaned.exists():
            return render(request, "network/error.html", {"error": "Your loan interferences with an already existing one"})

        new_loan = Loan()
        new_loan.member = request.user.username
        new_loan.books = Books.objects.get(title=book)
        new_loan.date_of_loan = date
        new_loan.date_due = due_date
        new_loan.save()

        return HttpResponseRedirect(reverse("book_profile", kwargs={'book_title': book}))

    else:
        return HttpResponseRedirect(reverse("book_profile", kwargs={'book_title': book}))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
@login_required
def delete_loan(request, loan_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            loan = Loan.objects.get(id=data["loan"])
            loan.delete()
            return HttpResponse(status=204)

        except Loan.DoesNotExist:
            return render(request, "network/error.html", {"error": 'error while deleting'})
            #return JsonResponse({"error": "Requested loan does not exist"}, status=404)