from django.shortcuts import redirect, render, HttpResponse
from tv_shows_app.models import Network, TvShow
from time import gmtime, strftime, localtime
from datetime import datetime
from django.contrib import messages

def index(request):
    reset_var_session(request)

    context = {
                'tvshows' : TvShow.objects.all(),
                }
    return render(request, 'index.html', context)

#======================== NETWORK =======================
def networks(request):
    reset_var_session(request)

    context = {
                'networks':  Network.objects.all()
                }
    return render(request, 'networks/networks.html', context) 

def new_network(request):
    if request.method == 'GET':
        return render(request, 'networks/new_network.html')
    
    elif request.method == 'POST':
        new_network = Network.objects.create(
                                        name = request.POST['name'],
                                        description = request.POST['description'],
                                        )
        return redirect(f'/networks')


def edit_network(request, id_network):
    network =  Network.objects.get(id=id_network)
    if request.method == 'GET':
        context = {
                'network':  network,
                }
        return render(request, 'networks/edit_network.html', context)
    
    elif request.method == 'POST':
        network.name = request.POST['name'] 
        network.description = request.POST['description']
        network.save()

        return redirect(f'/networks')


def delete_network(request, id_network):
    network =  Network.objects.get(id=id_network)
    network.delete()

    return redirect(f'/networks')

#======================== SHOW =======================
def new_show(request):
    if request.method == 'GET':
        context = {
                'networks':  Network.objects.all()
                }
        return render(request, 'new.html', context)
    
    elif request.method == 'POST':
        print(request.POST)
        # pasar los datos al método que escribimos y guardar la respuesta en una variable llamada errors
        errors = TvShow.objects.validador_basico(request.POST)

        if TvShow.objects.filter(title=request.POST['title']).exists():
            errors['existe_registro'] = "este título ya existe"; 
        # compruebe si el diccionario de errores tiene algo en él
        if len(errors) > 0:
            # si el diccionario de errores contiene algo, recorra cada par clave-valor y cree un mensaje flash
            for key, value in errors.items():
                messages.error(request, value);
            # redirigir al usuario al formulario para corregir los errores
            
            #si el usuario ingresó network lo guardamos en una varible de sesion 
            if request.POST['network'] != "Open this select menu":
                network = Network.objects.get(id=request.POST['network'])
                request.session['show_network'] = network.name

            request.session['show_title'] = request.POST['title']
            request.session['show_release_date'] = request.POST['release_date']
            request.session['show_description'] = request.POST['description']

            return redirect('/shows/new')
        else:
            # si el objeto de errores está vacío, eso significa que no hubo errores.
            new_show = TvShow.objects.create(
                                        title = request.POST['title'],
                                        network = Network.objects.get(id=request.POST['network']),
                                        release_date = request.POST['release_date'],
                                        description = request.POST['description'],
                                        )
            #reset_var_session()

            messages.success(request, f"Show {new_show.id} was added successfully ")
            # redirigir a la ruta de exito
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
                'networks':  Network.objects.all(),
                'release_date' :  show.release_date.strftime("%Y-%m-%d")
                }
        return render(request, 'edit.html', context)
    
    elif request.method == 'POST':
        errors = TvShow.objects.validador_basico(request.POST)

        # compruebe si el diccionario de errores tiene algo en él
        if len(errors) > 0:
            # si el diccionario de errores contiene algo, recorra cada par clave-valor y cree un mensaje flash
            for key, value in errors.items():
                messages.error(request, value);
            # redirigir al usuario al formulario para corregir los errores
            
            #si el usuario ingresó network lo guardamos en una varible de sesion 
            if request.POST['network'] != "Open this select menu":
                network = Network.objects.get(id=request.POST['network'])
                request.session['show_network'] = network.name

            request.session['show_title'] = request.POST['title']
            request.session['show_release_date'] = request.POST['release_date']
            request.session['show_description'] = request.POST['description']

            return redirect(f'/shows/{show.id}/edit')

        else:
            # si el objeto de errores está vacío, eso significa que no hubo errores.
            show.title = request.POST['title'] 
            show.network = Network.objects.get(id=request.POST['network'])
            show.release_date = request.POST['release_date']   
            show.description = request.POST['description']

            show.save()
            #reset_var_session()

            messages.success(request, f"Show {show.id} was successfully edited.")
            # redirigir a la ruta de exito
            return redirect(f'/shows/{show.id}')


def delete_show(request, id_show):
    show =  TvShow.objects.get(id=id_show)
    show.delete()

    return redirect(f'/shows')


#======================= RESET ==============================
def reset_var_session(request):
    request.session['show_title'] = ""
    request.session['show_network'] = ""
    request.session['show_network_id'] = ""
    request.session['show_release_date'] = ""
    request.session['show_description'] = ""

    return    
    
