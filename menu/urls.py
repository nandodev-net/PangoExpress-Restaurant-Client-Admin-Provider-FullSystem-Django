from django.conf.urls import url
from . import views

app_name = "menu"
urlpatterns = [
	#/
	url(r'^$', views.index, name='index'),
	
	#/menu/
	url(r'^menu/$', views.menu, name='menu'),

	#/menu/720/
	url(r'^(?P<id_plato>[0-9]+)/$', views.detail, name='detail'),
	
	#/menu/ordenar/120
    url(r'^ordenar/(?P<id_plato>[0-9]+)/$', views.hacer_pedido, name='pedido'),

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
    
    #/menu/perfil/inventario
    url(r'^perfil/inventario/$', views.VerInventario.as_view(), name="ver_inventario"),

    #/menu/perfil/inventario/eliminar/23
    url(r'^perfil/inventario/eliminar/(?P<id_ofrece>[0-9]+)/$', views.eliminar_producto_inventario, name="eliminar_producto_inventario"),
    
    #/menu/verpedido
    url(r'^verpedido/$', views.ver_pedido, name = 'ver_pedido'),

    #/menu/verpedido/pagar
    url(r'^verpedido/pagar/(?P<cuenta_id>[0-9]+)$', views.pagar_cuenta, name = 'pagar_pedido'),

	#/menu/verclientes/
	url(r'^verclientes/$', views.ver_clientes, name = 'ver_clientes'),

	#/menu/iniciarsesion/
	url(r'^iniciarsesion/$', views.IniciarSesion.as_view(), name = 'iniciar_sesion'),

	#/menu/cerrarsesion/
	url(r'^cerrarsesion/$', views.cerrar_sesion, name = 'cerrar_sesion'),

    #/menu/transacciones_rest/
	url(r'^transacciones_rest/$', views.ver_transacciones_restaurant, name = 'transacciones_restaurant'),

    #/menu/hacer_pedidos/
	url(r'^hacer_pedidos/$', views.HacerPedidos.as_view(), name = 'hacer_pedidos'),

    #/menu/confirmar_compra/
	url(r'^confirmar_compra/(?P<monto>[0-9]+,[0-9]+)/$', views.hacer_compra, name = 'aux_confirm'),

	#/menu/layoutbootstrap/
	url(r'^layoutbootstrap/$', views.layout_bootstrap, name = 'layout_bootstrap'),


]
