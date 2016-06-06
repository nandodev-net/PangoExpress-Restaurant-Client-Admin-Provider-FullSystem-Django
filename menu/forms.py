from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import PERFIL, USUARIO, CLIENTE, PROVEEDOR

months={
    1:_('Enero'), 2:_('Febrero'), 3:_('Marzo'), 4:_('Abril'),
    5:_('Mayo'), 6:_('Junio'), 7:_('Julio'), 8:_('Agosto'),
    9:_('Septiembre'), 10:_('Octubre'), 11:_('Noviembre'), 12:_('Diciembre')
}



class FormRegistrarUsuario(forms.ModelForm):
	'''
	email = forms.CharField(label='e-mail', max_length=100)
	passwd = forms.CharField(label='Constrasena', widget=forms.PasswordInput)
	'''
	#tipo = forms.ChoiceField(label= 'Tipo', choices = [(1, 'cliente'), (2, 'proveedor')])

	class Meta:
		model = PERFIL
		fields = ['pseudonimo']

class FormRegistrarUsuario2(forms.ModelForm):
	tipo = forms.ChoiceField(label='Tipo', choices=[(1, 'Cliente'), (2, 'Proveedor')])
	
	class Meta:
		model = USUARIO
		fields = ['contrasenia', 'email']
		labels = {
            'contrasenia': _('Contraseña'),
            'email': _('Email'),
        }
		widgets = {
        	'contrasenia': forms.widgets.PasswordInput,
        }

        

class FormRegistrarCliente(forms.ModelForm):
	class Meta:
		model = CLIENTE
		fields = ['nombre', 'apellido', 'telefono', 'ci']#,'fechaNacimiento']
		labels = {
            'nombre': _('Nombres'),
            'apellido': _('Apellidos'),
            'telefono': _('Teléfono'),
            #'fechaNacimiento': _('Fecha de Nacimiento'),
        }
		widgets = {
        	#'fechaNacimiento' : forms.widgets.SelectDateWidget(months = months ),
        }



class FormRegistrarProveedor(forms.ModelForm):
	class Meta:
		model = PROVEEDOR
		fields = ['nombre', 'rif']
		labels = {
            'nombre': _('Nombre'),
            'rif': _('RIF')
        }

class FormEditarPerfilCliente(forms.ModelForm):
	pseudonimo = forms.CharField(label='Pseudonimo')
	

	class Meta:
		model = CLIENTE
		fields = ['nombre', 'apellido', 'telefono']
		labels = {
            'nombre': _('Nombres'),
            'apellido': _('Apellidos'),
            'telefono': _('Teléfono')

        }

class FormEditarPerfilProveedor(forms.ModelForm):
	pseudonimo = forms.CharField(label='Pseudonimo')

	class Meta:
		model = PROVEEDOR
		fields = ['nombre', 'rif']
		labels = {
            'nombre': _('Nombre'),
            'rif': _('RIF')
        }


class FormIniciarSesion(forms.Form):
	pseudonimo = forms.CharField(label='Pseudonimo', max_length = 50)
	passwd = forms.CharField(label='Constraseña', widget=forms.PasswordInput)