**Library Manager Project**


This is the library manager project. It is a library manager website, where users can see all the books
and their availability. If the user registers to the website
they will be able to loan up to 4 different books for a whole month.

It can be run by using 'python manage.py runserver'

For the implementation of this project, I have created 4 new models Author, Loan, Genre and Books
and overwritten the AbstractUser model called User.

The webpage consists on 4 mainpages:
 1. Index: where a animated carousel shows the authors of the library books,
    it also shows the retrieved information of the search form queries (index.html and style.css)
 2. An author's profile site where all their works are displayed (profile.html and profile.css)
 3. A book's place where everyone can see the books' loan history and a place 
    where users can request for a new loan. (book_profile.html and book.css)
 4. User's profile, where their loans are showed and they can choose to delete one of them
    since there is a maximum of loans per person (4) (profile.html, profile.css and delete_loan.js)
    

The book's data extracted to complete this project was from: 
https://gist.github.com/jaidevd/23aef12e9bf56c618c41#file-books-csv


