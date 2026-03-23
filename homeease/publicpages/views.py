from django.shortcuts import render

# Create your views here.
def Home(request):
    """
    Home page view
    """
    return render(request, "PublicPages/index.html")