
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from markdown2 import Markdown
from . import util
from django.urls import reverse
import random

class NavBarForm(forms.Form):
    name = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia', 'class': "search"}))

class CreateForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    content = forms.CharField(widget=forms.Textarea)

class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NavBarForm()
    })


def entry(request, title):
    theEntry = util.get_entry(title)
    if theEntry is not None:
        markdowner = Markdown()
        return render(request, "encyclopedia/entries.html", {
            "content": markdowner.convert(theEntry),
            "title": title,
            "form": NavBarForm()
        })
    else:
        sublist = [i for i in util.list_entries() if title in i]
        if not sublist:
            return render(request, "encyclopedia/error_page.html", {
                "error": "The required title does not yet exist."
            })
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": sublist,
                "form": NavBarForm()
            })


def entry2(request):
    if request.method == "POST":
        form = NavBarForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["name"]
            return HttpResponseRedirect(reverse("entry", args=[title]))
        else:
            return render(request, "encyclopedia/error_page.html", {
                "error": "There's been an error with the form. Please try again.",
                "form": NavBarForm()
            })
    else:
        return HttpResponseRedirect(reverse("index"))


def random_page(request):
    entries_list = util.list_entries()
    choice = random.choice(entries_list)
    return HttpResponseRedirect(reverse("entry", args=[choice]))


def create_page(request):
    if request.method == "POST":
        create_post = CreateForm(request.POST)
        if create_post.is_valid():
            title = create_post.cleaned_data["title"]
            if title in util.list_entries():
                return render(request, "encyclopedia/error_page.html", {
                    "error": "This title already exists"
                })
            content = create_post.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=[title]))

        else:
            return render(request, "encyclopedia/error_page.html", {
                "error": "There has been an error with the Creation Form"
            })
    else:
        return render(request, "encyclopedia/create.html", {
            "form": NavBarForm(),
            "create": CreateForm()
        })


def edit(request, title):
    if request.method == "POST":
        edit_post = EditForm(request.POST)
        if edit_post.is_valid():
            content = edit_post.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=[title]))
        else:
            return render(request, "encyclopedia/error_page.html", {
                "error": "There has been an error with the Edit Form"
            })
    else:
        content = util.get_entry(title)
        form = EditForm()
        form.fields['content'].initial = content
        return render(request, 'encyclopedia/edit.html', {
            "title": title,
            "edit": form
        })

