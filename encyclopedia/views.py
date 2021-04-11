from django.shortcuts import render
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

from markdown2 import markdown
import re
from random import randint

from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Entry Title"}))
    content = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Write content in Markdown syntax"}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def view_entry(request, title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/request_not_found.html", 
                {"title": title})
    else:
        entry_data = markdown(util.get_entry(title))
        return render(request, "encyclopedia/view_entry.html", 
                    {"entry_data": entry_data,
                    "title": title})

def search(request):
    _, filenames = default_storage.listdir("entries")
    available_entries = list(sorted(re.sub(r"\.md$", "", filename)
                            for filename in filenames if filename.endswith(".md")))
    for entry in available_entries:
        title = str.lower(request.POST.get("query"))
        if title == str.lower(entry):
            return HttpResponseRedirect(reverse("encyclopedia:view_entry", args=(title,)))
        else:
            regexp = re.compile(title)
            matches = []
            for entry in available_entries:
                if regexp.search(str.lower(entry)):
                    matches.append(entry)

            return render(request, "encyclopedia/search_results.html", 
                        {"matches": matches, "title": title})

def write_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:view-entry", args=(title,)))
        else:
            return render(request, "encyclopedia/write_entry.html",
                        {"form": form})
    else:
        form = NewEntryForm()
        return render(request, "encyclopedia/write_entry.html",
                    {"form": form})

def edit_entry(request, title):
    content = util.get_entry(title.strip())
    form = NewEntryForm()
    form.content = content
    form.title = title
    return render(request, "encyclopedia/edit_entry.html", 
            {"content": content, "title": title})

def get_random_entry(request):
    entries = util.list_entries()
    rand_idx = randint(0, len(entries) - 1)
    return HttpResponseRedirect(reverse("encyclopedia:view-entry", args=(entries[rand_idx],)))