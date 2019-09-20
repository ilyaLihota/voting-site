from django.shortcuts import render


# Create your views here.
def posts_list(request):
    n = ['Ilya', 'OLeg', 'Petya']
    return render(request, 'poll/index.html', context={'names': n})
