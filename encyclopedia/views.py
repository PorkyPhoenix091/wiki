import random
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.http import HttpResponse


from markdown2 import Markdown
markdowner = Markdown()



from . import util

class EntryForm(forms.Form):
    name = forms.CharField(label="Entry name")
    content = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'form-control w-75'}))
class EditEntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'form-control w-75'}))

    

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def search(request):
    q = request.GET['q']
    if util.get_entry(q) is not None:
        return redirect("/wiki/"+q)
    else:
        pEntries = [s for s in util.list_entries() if q in s]
        return render(request,"encyclopedia/search.html",{
            "q" : q,
            "possibleEntries" : pEntries
        })
def entry(request, entry):
    try:
        return render(request,"encyclopedia/entry.html",{
        "code": markdowner.convert(util.get_entry(entry)),
        "entry": entry
    })
    except TypeError:
        return render(request, "encyclopedia/error.html",{
                    "errormsg" : "Sorry, this page does not exist"
                })
    
def newpage(request):
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = EntryForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the task from the 'cleaned' version of form data
            name = form.cleaned_data["name"]
            content = form.cleaned_data["content"]

            # Add the new task to our list of tasks
            if util.get_entry(name) is None:
                util.save_entry(name, content)
                # Redirect user to list of tasks
                return redirect(reverse('entry', args=(name)))
            else:
                return render(request, "encyclopedia/error.html",{
                    "errormsg" : "Sorry, this page already exists"
                } )

        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "tasks/add.html", {
                "form": form
            })
    return render(request,"encyclopedia/newpage.html",{
        "form" : EntryForm()
    })

def randompage(request):
    randomentry = random.choice(util.list_entries())

    return redirect("/wiki/"+randomentry)
def editpage(request,entry):
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = EditEntryForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the task from the 'cleaned' version of form data
            content = form.cleaned_data["content"]

            # Add the new task to our list of tasks
            if util.get_entry(entry) is not None:

                util.save_entry(entry, content)
                    # Redirect user to list of tasks
                return redirect(reverse('entry', kwargs={"entry":entry}))
            else:
                return render(request, "encyclopedia/error.html",{
                    "errormsg" : "Sorry, this page does not exist and thus cannot be edited"
                })
    form = EditEntryForm(initial={'content': util.get_entry(entry)})
    return render(request,"encyclopedia/editpage.html",{
        "form":form,
        "entry":entry
    })