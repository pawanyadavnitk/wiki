import re
import markdown

from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
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
        # can use name.lowe() == entry.lower() as well
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