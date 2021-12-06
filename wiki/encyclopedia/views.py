import re
import random
import markdown2
from django.http.response import HttpResponse
from django.shortcuts import render
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def create(request):
    # if the user created the entry
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        entry = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": entry
        })
    return render(request, "encyclopedia/create.html")


def search(request):
    # if the user is searching for an entry
    title = request.POST["q"]
    entry = util.get_entry(title)
    if entry != None:
        entry = markdown2.markdown(entry)
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "title": title
        })
    entries_list = []
    for entry in util.list_entries():
        if title.lower() in entry.lower():
            entries_list.append(entry)
            break
    return render(request, "encyclopedia/searchresult.html", {
        "entries_list": entries_list
    })


def entry(request, title):
    # if the user clicked or wrote the entire https
    entry = util.get_entry(title)
    entry = markdown2.markdown(entry) if entry is not None else None
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": entry
    })


def random_entry(request):
    entries_list = util.list_entries()
    l = len(entries_list)
    ind = random.randrange(0, l)
    title = entries_list[ind]
    entry = util.get_entry(title)
    entry = markdown2.markdown(entry)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": entry
    })


def edit(request, title):
    # if the user edited the content
    if request.method == "POST":
        content = request.POST["content"]
        util.save_entry(title, content)
        entry = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": entry
        })
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "content": content,
        "title": title
    })
