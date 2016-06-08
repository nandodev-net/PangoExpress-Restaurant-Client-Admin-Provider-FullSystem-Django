from django import forms
from .models import *

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
	tipo = forms.ChoiceField(label='Tipo', choices=[(1, 'cliente'), (2, 'proveedor')])

	class Meta:
		model = USUARIO
		fields = ['contrasenia', 'email']

class FormRegistrarCliente(forms.ModelForm):
	class Meta:
		model = CLIENTE
		fields = ['nombre', 'apellido', 'telefono', 'ci']

class FormRegistrarProveedor(forms.ModelForm):
	class Meta:
		model = PROVEEDOR
		fields = ['nombre', 'rif']

class FormEditarPerfilCliente(forms.ModelForm):
	pseudonimo = forms.CharField(label='Pseudonimo')

	class Meta:
		model = CLIENTE
		fields = ['nombre', 'apellido', 'telefono']

class FormEditarPerfilProveedor(forms.ModelForm):
	pseudonimo = forms.CharField(label='Pseudonimo')

	class Meta:
		model = PROVEEDOR
		fields = ['nombre', 'rif']


class FormIniciarSesion(forms.Form):
	pseudonimo = forms.CharField(label='Pseudonimo', max_length = 50)
	passwd = forms.CharField(label='Constrasena', widget=forms.PasswordInput)
	
class FormCrearBilletera(forms.ModelForm):
    class Meta:
        model = BILLETERA
        fields = ['nombre', 'apellido', 'PIN']

class FormRecargaBilletera(forms.Form):
    PIN = forms.CharField(max_length=50)
    monto = forms.FloatField(label='Monto')
    
    
