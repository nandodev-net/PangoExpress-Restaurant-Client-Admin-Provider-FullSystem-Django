from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from .models import PERFIL, USUARIO, CLIENTE, PROVEEDOR, BILLETERA, PRODUCTO, Ofrece

#Validadores
#Validar nombre válido.
def validate_nombre(valor):
	for x in valor:
		if not x.isalpha():
			raise ValidationError(
            _('%(valor)s No es válido, tiene que ser caracteres'),
            params={'valor': valor},
            )

#Validar cédula válida.
def validate_ci(ci):
	if len(ci)>8:
		raise ValidationError(
            _('%(ci)s No es válido, máximo 8 dígitos'),
            params={'ci': ci},
            )
	try:
		ci = int(ci)
		if ci<=0:
			raise ValidationError(
            _('%(ci)s No es válido,debe ser mayor a cero (0)'),
            params={'ci': ci},
            )
	except:
		raise ValidationError(
			_('%(ci)s No es válido, sólo puede ingresar números'),
			params={'ci': ci},
			)

#Validar teléfono válida.
def validate_telefono(telf):
	if not 9<len(telf)<12:
		raise ValidationError(
            _('%(telf)s No es válido, la longitud debe ser de 10 o 11'),
            params={'telf': telf},
            )
	try:
		telf = int(telf)
		if telf<0:
			raise ValidationError(
            _('%(telf)s No es válido,debe ser mayor o igual a cero (0)'),
            params={'telf': telf},
            )
	except:
		raise ValidationError(
			_('%(telf)s No es válido, sólo puede ingresar números'),
			params={'telf': telf},
			)

#Validar rif válida.
def validate_rif(rif):
	#Siguiendo la especificacion, rif debe estar entre 6 a 8 caracteres
	if 5<len(rif)<9:
		raise ValidationError(
            _('%(rif)s No es válido, la longitud debe ser de 6 a 8'),
            params={'rif': rif},
            )
	"""
		try:
		letra=rif[0]
		if letra.isalpha() is not in ["V","J","E"]:
			raise ValidationError(
            _('%(rif)s Debe Empezar con V, J o E)'),
            params={'rif': rif},
            )
		
		
	except:
		raise ValidationError(
			_('%(rif)s No es válido, sólo puede ingresar números'),
			params={'rif':rif},
			)
	"""
	
def validate_monto(monto):
	if monto<=0:
		raise ValidationError(
            _('%(monto)s Monto inválido, debe ser un monto positivo.'),
            params={'monto': monto},
            )



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
		nombre = forms.CharField(validators=[validate_nombre])
		apellido = forms.CharField(validators=[validate_nombre])
		telefono = forms.CharField(validators=[validate_telefono])
		fields = ['nombre', 'apellido', 'telefono', 'ci','fechaNacimiento']
		labels = {
            'nombre': _('Nombres'),
            'apellido': _('Apellidos'),
            'telefono': _('Teléfono'),
            'fechaNacimiento': _('Fecha de Nacimiento'),
        }
		widgets = {
        	'fechaNacimiento' : forms.widgets.SelectDateWidget(
        		years=range(1890, 2015), months = months ),

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
	#pseudonimo = forms.CharField(label='Pseudonimo')
	

	class Meta:
		model = CLIENTE
		fields = ['nombre', 'apellido', 'telefono']
		widgets = {
        	'nombre' : forms.widgets.TextInput(attrs={'readonly': 'readonly'}),
        	'apellido' : forms.widgets.TextInput(attrs={'readonly': 'readonly'}),
      
        }
        
        
		labels = {
			'nombre': _('Nombres'),
			'apellido': _('Apellidos'),
			'telefono': _('Teléfono'),
        }

        
class FormEditarPerfil(forms.ModelForm):
	class Meta:
		model = PERFIL
		fields = ['pseudonimo']
			
	


class FormEditarPerfilProveedor(forms.ModelForm):
	pseudonimo = forms.CharField(label='Pseudonimo')

	class Meta:
		model = PROVEEDOR
		fields = ['nombre', 'rif']
		widgets = {
        	'nombre' : forms.widgets.TextInput(attrs={'disabled': 'disabled'}),
        }
		labels = {
            'nombre': _('Nombre'),
            'rif': _('RIF')
        }


class FormIniciarSesion(forms.Form):
	pseudonimo = forms.CharField(label='Pseudonimo', max_length = 50)
	passwd = forms.CharField(label='Constrasena', widget=forms.PasswordInput)
	
class FormCrearBilletera(forms.ModelForm):
    class Meta:
        model = BILLETERA
        fields = ['nombre', 'apellido', 'PIN']

class FormRecargaBilletera(forms.Form):
    PIN = forms.CharField(max_length=50)
    monto = forms.FloatField(label='Monto', validators = [validate_monto])

class FormConfirmacionPIN(forms.Form):
    PIN = forms.CharField(max_length=50)

class FormAgregarProductoProveedor(forms.ModelForm):
    producto = forms.ModelChoiceField(PRODUCTO.objects)
    precio = forms.FloatField()

    class Meta:
        model = Ofrece
        fields = ['producto', 'precio']

