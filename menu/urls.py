from django.conf.urls import url
from . import views

app_name = "menu"
urlpatterns = [
	#/menu/
	url(r'^$', views.index, name='index'),

	url(r'^menu/$', views.menu, name='menu'),

	#/menu/720/
	url(r'^(?P<id_plato>[0-9]+)/$', views.detail, name='detail'),

	#/menu/registro/
	url(r'^registro/$', views.FormularioRegistro.as_view(), name='registro'),

	#/menu/registro/cliente/
	url(r'^registro/cliente$', views.FormularioRegistroCliente.as_view(), name='registrar_cliente'),

	#/menu/registro/proveedor/
	url(r'^registro/proveedor$', views.FormularioRegistroProveedor.as_view(), name='registrar_proveedor'),

	#/menu/perfil/
	url(r'^perfil/$', views.ver_perfil, name = 'perfil'),

	#/menu/perfil/editar/
	url(r'^perfil/editar/$', views.EditarPerfil.as_view(), name = 'editar_perfil'),
	
    #/menu/perfil/billetera
    url(r'^perfil/billetera/$', views.gestionar_billetera, name = 'gestionar_billetera'),

    #/menu/perfil/billetera/crear
    url(r'^perfil/billetera/crear/$', views.CrearBilletera.as_view(), name = 'crear_billetera'),

    #/menu/perfil/billetera/recargar
    url(r'^perfil/billetera/recargar/$', views.RecargarBilletera.as_view(), name = 'crear_billetera'),

	#/menu/verclientes/
	url(r'^verclientes/$', views.ver_clientes, name = 'ver_clientes'),

	#/menu/iniciarsesion/
	url(r'^iniciarsesion/$', views.IniciarSesion.as_view(), name = 'iniciar_sesion'),

	#/menu/cerrarsesion/
	url(r'^cerrarsesion/$', views.cerrar_sesion, name = 'cerrar_sesion'),

	#/menu/layoutbootstrap/
	url(r'^layoutbootstrap/$', views.layout_bootstrap, name = 'layout_bootstrap'),


]
