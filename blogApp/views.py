from django.shortcuts import render

def firstPage(request):
    context={
        
    }
    return render(request, "blogApp/firstPage.html", context)
