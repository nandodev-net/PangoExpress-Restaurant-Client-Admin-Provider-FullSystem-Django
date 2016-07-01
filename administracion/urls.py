from django.conf.urls import url
from . import views

app_name = "administracion"

urlpatterns = [
    # /
    url(r'^$', views.index, name='index'),

    #gestionar_platos/
    url(r'^gestionar_platos/$', views.gestionar_platos, name='gestionar_platos'),

    # gestionar_platos/agregar
    url(r'^gestionar_platos/agregar/$', views.agregar_plato, name='agregar_plato'),

    # gestionar_platos/agregar
    url(r'^gestionar_platos/agregar/ingredientes/(?P<id_plato>[0-9]+)/$', views.agregar_ingredientes, name='agregar_ingredientes'),

    #
url(r'^gestionar_platos/editar/agregar_ingrediente/(?P<id_plato>[0-9]+)/$', views.agregar_ingrediente2, name='agregar_ingrediente2'),

    # gestionar_platos/eliminar/23
    url(r'^gestionar_platos/eliminar/(?P<id_plato>[0-9]+)/$', views.eliminar_plato, name='eliminar_plato'),

    # gestionar_platos/editar/23
    url(r'^gestionar_platos/editar/(?P<id_plato>[0-9]+)/$', views.editar_plato, name='editar_plato'),

    # gestionar_platos/editar/23/eliminar_ingrediente/23
    url(r'^gestionar_platos/editar/eliminar_ingrediente/(?P<id_ingrediente>[0-9]+)/$', views.eliminar_ingrediente, name='eliminar_ingrediente'),

    # gestionar_menus/
    url(r'^gestionar_menus/$', views.gestionar_menus, name='gestionar_menus'),

    # gestionar_menus/agregar/
    url(r'^gestionar_menus/agregar/$', views.agregar_menu, name='agregar_menu'),

    # gestionar_menus/agregar/platos/
    url(r'^gestionar_menus/agregar/platos/(?P<id_menu>[0-9]+)/$', views.agregar_platos_menu, name='agregar_platos_menu'),

    # gestionar_menus/editar/23
    url(r'^gestionar_menus/editar/(?P<id_menu>[0-9]+)/$', views.editar_menu, name='editar_menu'),

    # gestionar_menus/editar/agregar_plato/23
    url(r'^gestionar_menus/editar/agregar_plato/(?P<id_menu>[0-9]+)/$', views.agregar_plato_menu2, name='agregar_plato_menu2'),

    # gestionar_menus/editar/eliminar_plato/23
    url(r'^gestionar_menu/editar/eliminar_plato_menu/(?P<id_plato_en_menu>[0-9]+)/$', views.eliminar_plato_menu, name='eliminar_plato_menu'),

    # gestionar_productos/
    url(r'^gestionar_productos/$', views.gestionar_productos, name='gestionar_productos'),

    # gestionar_productos/
    url(r'^gestionar_productos/eliminar/(?P<id_producto>[0-9]+)/$', views.eliminar_producto, name='eliminar_producto'),

    # gestionar_platos/editar/23
    url(r'^gestionar_menus/eliminar/(?P<id_menu>[0-9]+)/$', views.eliminar_menu, name='eliminar_menu'),

    # ver_inventario/
    url(r'^ver_inventario/$', views.ver_inventario, name='ver_inventario'),

]