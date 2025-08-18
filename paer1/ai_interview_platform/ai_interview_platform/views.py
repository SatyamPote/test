from django.shortcuts import render

def homepage_view(request):
    """
    Renders the main homepage with links to all available tools.
    """
    return render(request, 'homepage.html')