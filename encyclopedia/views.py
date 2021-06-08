import re
import markdown

from django import forms
from django.forms.fields import CharField
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util


class NewSearchForm(forms.Form):
    query = CharField(label="Search")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "form": NewSearchForm(),
        "entries": util.list_entries()
    })

def display_entry_page(request, name):
    title, content = get_page_content(name)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })

def get_page_content(name):
    entries = util.list_entries()
    is_page_present = False
    for entry in entries:
        # can use name.lower() == entry.lower() as well
        if re.fullmatch(entry, name, re.IGNORECASE):
            name = entry
            is_page_present = True
            break
    if is_page_present:
        title = name
        content = util.get_entry(name)
        content = markdown.markdown(content)
    else:
        title = "Not Found"
        content = "<h1>Page not found</h1>"
    return title, content

def display_search_results(request):
    if request.method == "GET":
        form = NewSearchForm(request.GET)

        if form.is_valid():
            searchquery = form.cleaned_data["query"].lower()
            all_entries = util.list_entries()

            files = [
                filename for filename in all_entries
                if searchquery in filename.lower()
            ]

            for filename in files:
                if filename.lower() == searchquery:
                    redirect_url = reverse("encyclopedia:display_entry_page",
                                           kwargs={"name": filename})
                    return HttpResponseRedirect(redirect_url)

            return render(request,"encyclopedia/search_results.html",{
                    'search_results' : files,
                    "form":form
                })
