from django.contrib.auth.models import AbstractUser
from django.db import models


# Author: id, firstname, lastname
class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


# Genre: id, name
class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Book: id, title, author (from the author table), publisher (from the publisher table), genre (from the genre
# table), year
class Books(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.title


# Loan: id, member (from the Member table), books (from the book table), date of loan out, date due
class Loan(models.Model):
    member = models.CharField(max_length=60)
    books = models.ForeignKey(Books, on_delete=models.CASCADE)
    date_of_loan = models.DateField()
    date_due = models.DateField()

    def __str__(self):
        return 'Loan: ' + self.books.title + ' by ' + self.member


class User(AbstractUser):
    loans = models.ManyToManyField("Loan", related_name="user_loans")

    def serialize(self):
        return {
            "loans": [loans.id for loans in self.loans.all()],
            "num_loans": self.posts.count()
        }

    def get_loans(self):
        return self.loans.all()
