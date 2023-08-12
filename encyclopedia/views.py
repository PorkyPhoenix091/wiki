from django.shortcuts import render
from markdown2 import Markdown
markdowner = Markdown()

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry(request, entry):
    return render(request,"encyclopedia/entry.html",{
        "code": markdowner.convert(util.get_entry(entry)),
        "entry": entry
    })
def newpage(request):
    return render(request,"encyclopedia/newpage.html",{})
