from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError

from .models import *
from .forms import *

def index(request):

    context = {}
    return render(request, 'administracion/index.html', context)

def gestionar_platos(request):
    platos = PLATO.objects.all()
    context = { 'platos' : platos }

    return render(request, 'administracion/gestionarPlatos.html', context)

def agregar_plato(request):

    if request.method == 'GET':
        form = FormAgregarPlato()
        context = {'form' : form }

    elif request.method == 'POST':
        form = FormAgregarPlato(request.POST, request.FILES)
        context = {'form': form}

        if form.is_valid():
            try:
                plato = PLATO(nombre = form.cleaned_data['nombre'],
                              precio = form.cleaned_data['precio'],
                              descripcion = form.cleaned_data['descripcion'],
                              path_img = form.cleaned_data['path_img'],
                              establecimiento=form.cleaned_data['establecimiento']
                              )
                plato.save()
            except IntegrityError:
                return redirect('/administracion/gestionar_platos/agregar/')

            return redirect('/administracion/gestionar_platos/agregar/ingredientes/'+str(plato.id)+'/')
        elif form.errors:
            print('error magueo')
            print(form.errors)

    return render(request, 'administracion/agregarPlato.html', context)

def agregar_ingredientes(request, id_plato):
    plato = PLATO.objects.get(id = id_plato)

    if request.method == 'POST':
        form = FormAgregarIngrediente(request.POST)

        if form.is_valid():
            relacion = Ingredientes(plato = plato,
                                    producto = form.cleaned_data['ingrediente'],
                                    cantidad = form.cleaned_data['cantidad']
                                    )
            try:
                relacion.save()
            except IntegrityError:
                relacion = Ingredientes.objects.get(plato = plato,
                                                    producto=form.cleaned_data['ingrediente']
                                                    )
                relacion.cantidad = form.cleaned_data['cantidad']
                relacion.save()

        elif form.errors:
            print(form.errors)

    form = FormAgregarIngrediente()
    ingredientes = Ingredientes.objects.filter(plato = plato)
    context = {'form' : form,
               'ingredientes' : ingredientes,
               'plato' : plato
               }
    return render(request, 'administracion/agregarIngredientes.html', context)

def eliminar_plato(request, id_plato):
    plato = PLATO.objects.get(id = id_plato).delete()

    return redirect('/administracion/gestionar_platos/')

def eliminar_ingrediente(request, id_ingrediente):
    ingrediente = Ingredientes.objects.get(id = id_ingrediente)
    ingrediente.delete()

    return redirect('/administracion/gestionar_platos/editar/'+str(ingrediente.plato.id)+'/')

def editar_plato(request, id_plato):
    oldPlato = PLATO.objects.get(id = id_plato)
    ingredientes = Ingredientes.objects.filter(plato = oldPlato)

    if request.method == 'GET':
        form = FormAgregarPlato(instance = oldPlato)
        #print(form.path_img)
        form.fields['path_img'].required = False

    elif request.method == 'POST':
        form = FormAgregarPlato(request.POST, request.FILES)
        form.fields['path_img'].required = False

        if form.is_valid():
            plato = PLATO.objects.get(id = id_plato)
            plato.nombre = form.cleaned_data['nombre']
            plato.descripcion = form.cleaned_data['descripcion']
            plato.precio = form.cleaned_data['precio']
            plato.establecimiento = form.cleaned_data['establecimiento']

            if(form.cleaned_data['path_img']):
                plato.path_img = form.cleaned_data['path_img']
            elif(request.FILES.get('path_img')):
                plato.img_path = request.FILES.get('path_img')
            else:
                plato.path_img = oldPlato.path_img

            plato.save()

        elif form.errors:
            print('error')
            print(form.errors)

    form2 = FormAgregarIngrediente()
    context = {'form' : form,
               'form2' : form2,
               'ingredientes' : ingredientes,
               'plato' : oldPlato
               }

    return render(request, 'administracion/editarPlato.html', context)

def agregar_ingrediente2(request, id_plato):
    plato = PLATO.objects.get(id=id_plato)

    if request.method == 'POST':
        form = FormAgregarIngrediente(request.POST)

        if form.is_valid():
            relacion = Ingredientes(plato=plato,
                                    producto=form.cleaned_data['ingrediente'],
                                    cantidad=form.cleaned_data['cantidad']
                                    )
            try:
                relacion.save()
            except IntegrityError:
                relacion = Ingredientes.objects.get(plato=plato,
                                                    producto=form.cleaned_data['ingrediente']
                                                    )
                relacion.cantidad = form.cleaned_data['cantidad']
                relacion.save()

        elif form.errors:
            print(form.errors)

    form = FormAgregarIngrediente()
    ingredientes = Ingredientes.objects.filter(plato=plato)

    return redirect('/administracion/gestionar_platos/editar/'+str(plato.id)+'/')

def gestionar_menus(request):
    menus = MENU.objects.all()
    context = {'menus' : menus }

    return render(request, 'administracion/gestionarMenus.html', context)

def agregar_menu(request):
    if request.method == 'GET':
        form = FormAgregarMenu()

    elif request.method == 'POST':
        form = FormAgregarMenu(request.POST)

        if form.is_valid():
            try:
                menu = form.save()
            except IntegrityError:
                pass

            return redirect('/administracion/gestionar_menus/agregar/platos/'+str(menu.id)+'/')

        elif form.errors:
            print('error magueo')
            print(form.errors)

    context = {'form': form}
    return render(request, 'administracion/agregarMenu.html', context)

def agregar_platos_menu(request, id_menu):
    menu = MENU.objects.get(id=id_menu)

    if request.method == 'POST':
        form = FormAgregarPlatoMenu(request.POST)

        if form.is_valid():
            relacion = Plato_en_menu(menu = menu,
                                     plato = form.cleaned_data['plato']
                                    )
            try:
                relacion.save()
            except IntegrityError:
                pass

        elif form.errors:
            print(form.errors)

    form = FormAgregarPlatoMenu()
    platos = Plato_en_menu.objects.filter(menu=menu)
    context = {'form': form,
               'platos': platos,
               'menu': menu
               }
    return render(request, 'administracion/agregarPlatosMenu.html', context)

def eliminar_menu(request, id_menu):
    MENU.objects.get(id = id_menu).delete()

    return redirect('/administracion/gestionar_menus/')

def editar_menu(request, id_menu):
    menu = MENU.objects.get(id=id_menu)
    platos = Plato_en_menu.objects.filter(menu=menu)

    if request.method == 'GET':
        form = FormAgregarMenu(instance=menu)

    elif request.method == 'POST':
        form = FormAgregarMenu(request.POST)
        if form.is_valid():
            newMenu = MENU.objects.get(id = id_menu)
            newMenu.nombre = form.cleaned_data['nombre']
            newMenu.activo = form.cleaned_data['activo']
            newMenu.save()

        elif form.errors:
            print(form.errors)


    form2 = FormAgregarPlatoMenu()
    context = {'form': form,
               'form2' : form2,
               'platos' : platos,
               'menu' : menu
               }

    return render(request, 'administracion/editarMenu.html', context)

def agregar_plato_menu2(request, id_menu):
    menu = MENU.objects.get(id=id_menu)

    if request.method == 'POST':
        form = FormAgregarPlatoMenu(request.POST)

        if form.is_valid():
            relacion = Plato_en_menu(menu = menu,
                                     plato = form.cleaned_data['plato']
                                     )
            try:
                relacion.save()
            except IntegrityError:
                relacion = Plato_en_menu.objects.get(menu = menu,
                                                     plato=form.cleaned_data['plato']
                                                     )
                relacion.save()

        elif form.errors:
            print(form.errors)

    return redirect('/administracion/gestionar_menus/editar/'+str(menu.id)+'/')

def eliminar_plato_menu(request, id_plato_en_menu):
    plato_en_menu = Plato_en_menu.objects.get(id = id_plato_en_menu)
    plato_en_menu.delete()

    return redirect('/administracion/gestionar_menus/editar/'+str(plato_en_menu.menu.id)+'/')


def gestionar_productos(request):
    productos = PRODUCTO.objects.all()

    if request.method == 'POST':
        form = FormAgregarProducto(request.POST)

        if form.is_valid():
            try:
                producto = form.save()
            except IntegrityError:
                pass

        elif form.errors:
            print('error magueo')
            print(form.errors)

    form = FormAgregarProducto()
    context = {'productos' : productos,
               'form' : form
               }
    return render(request, 'administracion/gestionarProductos.html', context)

def agregar_producto(request):
    if request.method == 'GET':
        form = FormAgregarMenu()

    elif request.method == 'POST':
        form = FormAgregarMenu(request.POST)

        if form.is_valid():
            menu = form.save()
            return redirect('/administracion/gestionar_menus/agregar/platos/' + str(menu.id) + '/')

        elif form.errors:
            print('error magueo')
            print(form.errors)

    context = {'form': form}
    return render(request, 'administracion/agregarMenu.html', context)

def eliminar_producto(reuqest, id_producto):
    PRODUCTO.objects.get(id = id_producto).delete()

    return redirect('/administracion/gestionar_productos/')


def ver_inventario(request):
    productos_disponibles = Inventario.objects.all()

    context = {"productos_disponibles" : productos_disponibles }

    return render(request, "administracion/verInventario.html", context)