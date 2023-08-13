import random
from django.shortcuts import render
from markdown2 import Markdown
markdowner = Markdown()
from django.shortcuts import redirect


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

def randompage(request):
    randomentry = random.choice(util.list_entries())

    return redirect("/wiki/"+randomentry)