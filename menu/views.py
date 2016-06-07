from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import View
from django.db import IntegrityError

from .forms import *
from .models import PERFIL, USUARIO, CLIENTE, PROVEEDOR, PLATO


def index(request):
	all_platos = PLATO.objects.all()
	return render(request, 'menu/slider.html', {'all_platos': all_platos})

def menu(request):
	all_platos = PLATO.objects.all()
	return render(request,'menu/index.html', {'all_platos' : all_platos})


def detail(request, id_plato):
	plato = get_object_or_404(PLATO, pk=id_plato)
	return render(request, 'menu/detail.html', {'plato': plato})


''' Formulario general de registro de usuario,
	de aqui redirecciono a cliente o proveedor '''
class FormularioRegistro(View):
	template_name = 'menu/registro.html'

	def get(self, request):
		form = FormRegistrarUsuario()
		form2 = FormRegistrarUsuario2()
		context = {'form' : form, 'form2' : form2 }
		return render(request, self.template_name, context)

	def post(self, request):
		form = FormRegistrarUsuario(request.POST)
		form2 = FormRegistrarUsuario2(request.POST)

		if (form.is_valid() and form2.is_valid()):

			try:
				perfil = form.save()
				request.session['logged'] = True
				request.session['pid'] = perfil.id

				usuario = USUARIO(
					email=form2.cleaned_data['email'],
					contrasenia=form2.cleaned_data['contrasenia'],
					perfil=perfil
				)


				if(form2.cleaned_data['tipo'] == '1'):
					usuario.es_cliente = True
					usuario.save()
					return redirect('/menu/registro/cliente')
				else:
					usuario.save()
					return redirect('/menu/registro/proveedor')

			except IntegrityError:
				print("Integrity Error\n")

				request.session['logged'] = False
				request.session['pid'] = -1
				return redirect('/menu/registro/')

		else:
			# Agregar mensaje de error en formulario
			# creo que se puede especificar donde ocurrio el error
			print('Error en formulario\n')

		return redirect('/menu/registro/')


''' Formularuio de registro de cliente '''
class FormularioRegistroCliente(View):

	def get(self, request):
		form = FormRegistrarCliente()
		return render(request, 'menu/registroCliente.html', {'form' : form})

	def post(self, request):
		form = FormRegistrarCliente(request.POST)

		if form.is_valid():
			try:
				perfil = PERFIL.objects.get(id=request.session['pid'])
				usuario = USUARIO.objects.get(perfil=perfil)
				cliente = CLIENTE(
						usuario=usuario,
						ci=form.cleaned_data['ci'],
						nombre=form.cleaned_data['nombre'],
						apellido=form.cleaned_data['apellido'],
						telefono=form.cleaned_data['telefono'],
						billetera_id=None
						)
				cliente.save()

				return redirect('/menu/')

			except IntegrityError:
				print('marico no lo logra\n')
				return redirect('/menu/registro/cliente')
		else:
			print('formulario invalido\n')
			return redirect('/menu/registro/cliente')


''' Formulario de registro de proveedor'''
class FormularioRegistroProveedor(View):

	def get(self, request):
		form = FormRegistrarProveedor()
		return render(request, 'menu/registroProveedor.html', {'form' : form})

	def post(self, request):
		form = FormRegistrarProveedor(request.POST)

		if form.is_valid():
			try:
				perfil = PERFIL.objects.get(id=request.session['pid'])
				usuario = USUARIO.objects.get(perfil=perfil)
				proveedor = PROVEEDOR(
						usuario=usuario,
						rif = form.cleaned_data['rif'],
						nombre = form.cleaned_data['nombre']
						)
				proveedor.save()

				return redirect('/menu/')

			except IntegrityError:
				print('marico no lo logra\n')
				return redirect('/menu/registro/proveedor')
		else:
			print('formulario invalido\n')
			return redirect('/menu/registro/proveedor')


''' Vista de perfil '''
def ver_perfil(request):
	if(request.session.get('logged', default = False)):
		# Obtengo perfil y usuario logeado
		perfil = PERFIL.objects.get(id = request.session['pid'])
		usuario = USUARIO.objects.get(perfil = perfil)
		context = { 'pseudonimo' : perfil.pseudonimo,
					'email' : usuario.email,
					}

		if(usuario.es_cliente):
			extra = CLIENTE.objects.get(usuario=usuario)

			context['nombre'] = extra.nombre
			context['apellido'] = extra.apellido
			context['ci'] = extra.ci
			context['telefono'] = extra.telefono
		else:
			extra = PROVEEDOR.objects.get(usuario=usuario)

			context['nombre'] = extra.nombre
			context['rif'] = extra.rif
	else:
		context = {}
		print('no iniciaste perro\n')

	return render(request, 'menu/verPerfil.html', context)


''' Edicion de perfil '''
class EditarPerfil(View):

	def get(self, request):

		perfil = PERFIL.objects.get(id=request.session['pid'])
		usuario = USUARIO.objects.get(perfil=perfil)
		data = { 'pseudonimo' : perfil.pseudonimo}

		if(usuario.es_cliente):
			cliente = CLIENTE.objects.get(usuario = usuario)
			data['nombre'] = cliente.nombre
			data['apellido'] = cliente.apellido
			data['telefono'] = cliente.telefono

			form = FormEditarPerfilCliente(data, instance = cliente)
		else:
			proveedor = PROVEEDOR.objects.get(usuario = usuario)
			data['nombre'] = proveedor.nombre
			data['rif'] = proveedor.rif

			form = FormEditarPerfilProveedor(data, instance = proveedor)

		context = {'form' : form }

		return render(request, 'menu/editarPerfil.html', context)

	def post(self, request):
		perfil = PERFIL.objects.get(id = request.session['pid'])
		usuario = USUARIO.objects.get(perfil=perfil)

		if(usuario.es_cliente):
			cliente = CLIENTE.objects.get(usuario = usuario)
			form = FormEditarPerfilCliente(request.POST, instance = cliente)

			if form.is_valid():
				try:
					cliente = form.save()
					perfil.pseudonimo = form.cleaned_data['pseudonimo']
					perfil.save()
				except IntegrityError:
					print('Integriry Error\n')
			else:
				print('Error en formulario weon\n')
				# cuando encuentra error pasa por aqui, enviar un mensaje
		else:
			proveedor = PROVEEDOR.objects.get(usuario = usuario)
			form = FormEditarPerfilProveedor(request.POST, instance = proveedor)

			if form.is_valid():
				try:
					proveedor = form.save()
					perfil.pseudonimo = form.cleaned_data['pseudonimo']
					perfil.save()
				except IntegrityError:
					print('Integrity Error\n')
			else:
				print('Error en el formulario\n')
				# cuando falla pasa por aqui, dar mensaje

		return redirect('/menu/perfil')


''' Lista todos los clientes registrados en el sistema '''
def ver_clientes(request):
	perfiles = PERFIL.objects.all()
	usuarios = USUARIO.objects.all()
	lista_usuarios = []

	for p in perfiles:
		lista_usuarios.append({ 'pseudonimo' : p.pseudonimo,
								'passwd' : USUARIO.objects.get(perfil = p).contrasenia,
								'email' : USUARIO.objects.get(perfil = p).email
								})

	context = {'lista_usuarios' : lista_usuarios}

	return render(request, 'menu/verClientes.html', context)


''' Muestra formulario de inicio de sesion y hace operaciones
	necesarias para realizar esta accion                     '''
class IniciarSesion(View):

	def get(self, request):
		form = FormIniciarSesion()

		return render(request, 'menu/iniciarSesion.html', {'form' : form })

	def post(self, request):
		form = FormIniciarSesion(request.POST)

		if form.is_valid():
			try:
				perfil = PERFIL.objects.get(pseudonimo = form.cleaned_data['pseudonimo'])
				usuario = USUARIO.objects.get(perfil = perfil)

				if(usuario.contrasenia == form.cleaned_data['passwd']):
					request.session['logged'] = True
					request.session['pid'] = perfil.id
					return redirect('/menu/')

				else:
					print('No coinciden perrito')
					request.session['logged'] = False
					request.session['pid'] = -1
					return redirect('/menu/iniciarsesion')

			except PERFIL.DoesNotExist:
				print('El perfil no existe')
				request.session['logged'] = False
				request.session['pid'] = -1
				return redirect('/menu/iniciarsesion')

		else:
			print('Error en formulario\n')


''' Realiza operaciones necesarias para el cierre de sesion '''
def cerrar_sesion(request):

	request.session['logged'] = False
	request.session['pid'] = -1

	return redirect('/menu/')
	

''' Realiza operaciones necesaras para registrar un pedido '''
def hacer_pedido(request, plato_id):
    pass


''' Crea y asocia a un usuario una billetera electronica '''
def gestionar_billetera(request):
    perfil = PERFIL.objects.get(id = request.session['pid'])
    usuario = USUARIO.objects.get(perfil = perfil)
    cliente = CLIENTE.objects.get(usuario = usuario)

    if cliente.billetera == None:
        return redirect('/menu/perfil/billetera/crear')

    else:
        context = {'nombre': cliente.nombre,
                   'apellido': cliente.apellido,
                   'saldo': cliente.billetera.saldo
                   }
        return render(request, 'menu/mostrarBilletera.html', context)


class CrearBilletera(View):
    def get(self, request):
        perfil = PERFIL.objects.get(id=request.session['pid'])
        usuario = USUARIO.objects.get(perfil=perfil)
        cliente = CLIENTE.objects.get(usuario=usuario)
        data = {'nombre' : cliente.nombre,
                'apellido' : cliente.apellido
                }
        form = FormCrearBilletera(data)
        form.fields['nombre'].widget.attrs['readonly'] = True
        form.fields['apellido'].widget.attrs['readonly'] = True

        return render(request, 'menu/crearBilletera.html', {'form' : form})

    def post(self, request):
        perfil = PERFIL.objects.get(id=request.session['pid'])
        usuario = USUARIO.objects.get(perfil=perfil)
        cliente = CLIENTE.objects.get(usuario=usuario)
        form = FormCrearBilletera(request.POST)

        if form.is_valid():
            try:
                billetera = BILLETERA(nombre = form.cleaned_data['nombre'],
                                      apellido = form.cleaned_data['apellido'],
                                      PIN = form.cleaned_data['PIN'],
                                      saldo = 0
                                      )
                billetera.save()
                cliente.billetera = billetera
                cliente.save()

            except IntegrityError:
                print('Integrity Error\n')

            return redirect('/menu/perfil/billetera/')

        else:
            print("Error en formulario\n")
            return redirect('/menu/perfil/billetera/crear/')


''' Formulario de recarga, recarga la billetera '''
class RecargarBilletera(View):
    def get(self, request):
        form = FormRecargaBilletera()

        return render(request, 'menu/recargarBilletera.html', {'form' : form })

    def post(self, request):
        form = FormRecargaBilletera(request.POST)

        if form.is_valid():
            perfil = PERFIL.objects.get(id=request.session['pid'])
            usuario = USUARIO.objects.get(perfil=perfil)
            cliente = CLIENTE.objects.get(usuario=usuario)
            billetera = BilleteraElectronica(ident=cliente.billetera.id,
                                             nombres=cliente.billetera.nombre,
                                             apellidos=cliente.billetera.apellido,
                                             pin=cliente.billetera.PIN,
                                             saldoIni=cliente.billetera.saldo
                                             )

            aux = billetera.recargar(pin=form.cleaned_data['PIN'],
                                     ident=cliente.billetera.id,
                                     ano=datetime.datetime.now().year,
                                     mes=datetime.datetime.now().month,
                                     dia=datetime.datetime.now().day,
                                     monto=form.cleaned_data['monto']
                                     )
            if(aux == 1):
                print('Monto invalido')
            elif(aux == 2):
                print('Error en la fecha')
            elif(aux == 3):
                print('PIN incorrecto')
            else:
                try:
                    cliente.billetera.saldo = billetera.balance
                    cliente.billetera.save()

                    return redirect('/menu/perfil/billetera/')
                except IntegrityError:
                    print("Integrity Error\n")

            print('fallo la recarga')
            return redirect('/menu/perfil/billetera/recargar/')

        else:
            print('Eror en el formulario\n')
            redirect('/menu/perfil/billetera/recargar/')



''' Dummy para hacer pruebas con el layout '''
def layout_bootstrap(request):

	form = FormRegistrarUsuario()

	return render(request, 'menu/layoutBootstrap.html', {'form' : form })
