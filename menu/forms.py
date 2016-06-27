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
    if len(rif)<6 or len(rif)>8:
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
    elif monto == 666:
        raise ValidationError(
            _('%(monto)s Monto inválido, no se meta con cosas del diablo'),
            params={'monto': monto}
        )

def validate_pseudonimo(pseudonimo):
    for x in pseudonimo:
        if x== ' ':
            raise ValidationError(
            _('%(pseudonimo)s No es válido, no debe tener espacios.'),
            params={'pseudonimo': pseudonimo},
            )

def validate_tarjeta(numero):
    try:
        aux = int(numero)
        if(aux<=0 or len(numero) != 16 or numero[0] == '+'):
            raise ValidationError(
                _('%(numero)s No es válido, debe ser un número de tarjeta válido.'),
                params={'numero': numero},
        )
    except:
        raise ValidationError(
            _('%(numero)s No es válido, debe ser un número de tarjeta válido.'),
            params={'numero': numero},
        )

def validate_pintarjeta(pin):
    try:
        aux = int(pin)
        print('converti int')
        print(aux == 666)
        print(aux)
        print(pin)
        if (aux <= 0 or len(pin) != 3 or pin[0] == '+'):
            raise ValidationError(
                _('%(pin)s No es válido, debe ser un pin válido.'),
                params={'pin': pin}
            )
    except:
        print("culo")
        raise ValidationError(
            _('%(pin)s No es válido, debe ser un pin válido.'),
            params={'pin': pin}
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


class FormEditarPerfilCliente(forms.Form):
    pseudonimo = forms.CharField(label='Pseudonimo', validators =[validate_pseudonimo])
    nombre = forms.CharField(label='Nombre')
    apellido = forms.CharField(label='Apellido')
    telefono = forms.CharField(label='Telefono', validators = [validate_telefono])

    nombre.widget = forms.widgets.TextInput(attrs={'readonly': 'readonly'})
    apellido.widget = forms.widgets.TextInput(attrs={'readonly': 'readonly'})


class FormEditarPerfilProveedor(forms.Form):
    pseudonimo = forms.CharField(label='Pseudonimo', validators = [validate_pseudonimo])
    rif = forms.CharField(label='RIF', validators = [validate_rif])
    nombre = forms.CharField(label='Nombre')

    nombre.widget = forms.widgets.TextInput(attrs={'readonly': 'readonly'})


class FormIniciarSesion(forms.Form):
    pseudonimo = forms.CharField(label='Pseudonimo', max_length = 50)
    passwd = forms.CharField(label='Constrasena', widget=forms.PasswordInput)

class FormCrearBilletera(forms.ModelForm):
    class Meta:
        model = BILLETERA
        fields = ['nombre', 'apellido', 'PIN']

class FormRecargaBilletera(forms.Form):
    monto = forms.FloatField(label='Monto', validators = [validate_monto])
    numero_de_tarjeta = forms.CharField(max_length=16, validators = [validate_tarjeta])
    pin_de_la_tarjeta = forms.CharField(max_length=3, validators = [validate_pintarjeta])
    tipo_de_tarjeta = forms.ChoiceField( choices = [(1, 'Visa'), (2, 'MasterCard')])
    PIN = forms.CharField(max_length=50)


class FormConfirmacionPIN(forms.Form):
    PIN = forms.CharField(max_length=50)

class FormAgregarProductoProveedor(forms.ModelForm):
    producto = forms.ModelChoiceField(PRODUCTO.objects)
    precio = forms.FloatField()

    class Meta:
        model = Ofrece
        fields = ['producto', 'precio']

class FormSeleccionarMes(forms.Form):

    fecha1 = forms.DateField(widget= forms.widgets.SelectDateWidget(years=range(2014, 2016), months=months),
                             label='Desde: ')
    fecha2 = forms.DateField(widget= forms.widgets.SelectDateWidget(years=range(2014, 2017), months=months),
                             label='Hasta: ')


class FormSeleccionarProveedor(forms.Form):

    proveedor = forms.ModelChoiceField(PROVEEDOR.objects, label='Seleccione un proveedor')

class FormSeleccionarProductos(forms.ModelForm):
    cantidad = forms.IntegerField(label='', initial=0)

    class Meta:
        model = Ofrece
        fields =[]
