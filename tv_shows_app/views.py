from django.shortcuts import redirect, render, HttpResponse
from tv_shows_app.models import TvShow
from time import gmtime, strftime, localtime
from datetime import datetime

def index(request):
    context = {
                'tvshows' : TvShow.objects.all()
                }
    return render(request, 'index.html', context)


def new_show(request):
    if request.method == 'GET':
        return render(request, 'new.html')
    
    elif request.method == 'POST':
        new_show = TvShow.objects.create(
                                        title = request.POST['title'],
                                        network = request.POST['network'],
                                        release_date = request.POST['release_date'],
                                        description = request.POST['description'],
                                        )
        return redirect(f'/shows/{new_show.id}')


def view_show(request, id_show):
    context = {
                'show':  TvShow.objects.get(id=id_show)
                }
    return render(request, 'view.html', context)  


def edit_show(request, id_show):
    show =  TvShow.objects.get(id=id_show)
    if request.method == 'GET':
        context = {
                'show':  show,
                'release_date' :  show.release_date.strftime("%Y-%m-%d")
                }
        return render(request, 'edit.html', context)
    
    elif request.method == 'POST':
        show.title = request.POST['title'] 
        show.network = request.POST['network']
        show.release_date = request.POST['release_date']   
        show.description = request.POST['description']

        show.save()

        return redirect(f'/shows/{show.id}')


def delete_show(request, id_show):
    show =  TvShow.objects.get(id=id_show)
    show.delete()

    return redirect(f'/shows')
    
