from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from  django.core.validators import EmailValidator

#Validadores
#Validar nombre válido.
def validate_nombre(valor):
    for x in valor:
        if not x.isalpha() and x!=' ':
            raise ValidationError(
            _('%(valor)s No es válido, tiene que ser caracteres'),
            params={'valor': valor},
            )

#Validar pin de la billetera
def validate_PIN(pin):
    aux = pin
    try:
        int(pin)
        if(len(aux)!=4 or int(aux)<0):
            assert(False)
    except:
        raise ValidationError(
            _('%(pin)s No es válido, tienen que ser 4 números.'),
            params={'pin': pin},
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
    if not 5<len(rif)<9:
        raise ValidationError(
            _('%(rif)s No es válido, la longitud debe ser de 6 a 8'),
            params={'rif': rif},
            )

#Validar psudónimo.
def validate_pseudonimo(pseudonimo):
    for x in pseudonimo:
        if x== ' ':
            raise ValidationError(
            _('%(pseudonimo)s No es válido, no debe tener espacios.'),
            params={'pseudonimo': pseudonimo},
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
def validate_nombreProveedor(valor):
    for x in valor:
        if not x.isalpha() and x not in ["-"," ","_"] and not x.isdigit():
            raise ValidationError(
            _('%(valor)s No es válido, tiene que ser caracteres'),
            params={'valor': valor},
            )

def validate_correo(correo):
    arroba = False
    punto = False
    j = 0
    k = -2
    for i in range(0,len(correo)):
        if correo[i]==' ':
            raise ValidationError(
            _('%(correo)s Email inválido, no puede haber espacios.'),
            params={'correo': correo},
            )
        if arroba:
            if correo[i]=='@':
                raise ValidationError(
            _('%(correo)s Email inválido, no puede haber más de una arroba.'),
            params={'correo': correo},
            )
            elif punto and correo[i]=='.' and i==k+1:
                raise ValidationError(
            _('%(correo)s Email inválido, no puede haber más de un punto seguido después del arroba'),
            params={'correo': correo},
            )
            elif correo[i]=='.':
                punto = True
                k = i

        if correo[i] == '@':
            if i == 0:
                raise ValidationError(
            _('%(correo)s Email inválido, debe haber algo antes del arroba.'),
            params={'correo': correo},
            )
            j=i
            arroba = True
    if not arroba:
        raise ValidationError(
            _('%(correo)s Email inválido, debe haber arroba.'),
            params={'correo': correo},
            )
    elif not punto:
        raise ValidationError(
            _('%(correo)s Email inválido, después del arroba, debe haber un punto.'),
            params={'correo': correo},
            )
    if k == len(correo)-1 or j == len(correo)-1 or not arroba or not punto:
        raise ValidationError(
            _('%(correo)s Email inválido, debe haber algo después del arroba y después del punto.'),
            params={'correo': correo},
            )

def validate_monto(monto):
    if monto<=0:
        raise ValidationError(
            _('%(monto)s Monto inválido, debe ser un monto positivo.'),
            params={'monto': monto},
            )

# Create your models here.
class PERFIL(models.Model):
    id = models.AutoField(primary_key=True)
    pseudonimo = models.CharField(max_length=100, unique = True,
        error_messages={"unique":"Este pseudónimo ya está en uso."}, validators=[validate_pseudonimo])
    foto = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.pseudonimo

class INTERES_PERFIL(models.Model):
    perfil = models.ForeignKey(PERFIL, primary_key=True)
    interes = models.CharField(max_length=50)

class USUARIO(models.Model):
    email = models.CharField(max_length=200, primary_key=True,
        validators=[validate_correo],
        error_messages={"unique":"Ese email ya está en uso."})
    contrasenia = models.CharField(max_length=50)
    es_cliente = models.BooleanField(default = False)
    perfil = models.ForeignKey(PERFIL)

    def __str__(self):
        return self.perfil.pseudonimo

class BILLETERA(models.Model):
    id = models.AutoField(primary_key=True)
    PIN = models.CharField(max_length=4,validators=[validate_PIN])
    nombre = models.CharField(max_length=50, validators=[validate_nombre])
    apellido = models.CharField(max_length=50, validators=[validate_nombre])
    saldo = models.FloatField()

class CLIENTE(models.Model):
    usuario = models.ForeignKey(USUARIO, primary_key=True)
    ci = models.CharField(max_length=8, unique=True, validators=[validate_ci], error_messages={"unique":"El CI ya está en uso"})
    nombre = models.CharField(max_length=50, validators=[validate_nombre])
    apellido = models.CharField(max_length=50, validators=[validate_nombre])
    telefono = models.CharField(max_length=11, validators=[validate_telefono])
    fechaNacimiento = models.DateField(null = False)
    billetera = models.ForeignKey(BILLETERA, null = True)

    def __str__(self):
        return self.usuario.perfil.pseudonimo

class PROVEEDOR(models.Model):
    usuario = models.ForeignKey(USUARIO, primary_key=True)
    rif = models.CharField(max_length=8, unique=True,validators=[validate_rif])
    nombre = models.CharField(max_length=50, validators=[validate_nombreProveedor])

    def __str__(self):
        return self.usuario.perfil.pseudonimo

class RESTAURANT(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50,validators=[validate_nombre])
    RIF = models.CharField(max_length=50,unique=True,validators=[validate_rif])
    direccion = models.CharField(max_length=50)

    def __str__(self):
        return str(self.nombre) +", "+ str(self.direccion)

class TELEFONOS_RESTAURANT(models.Model):
    establecimiento = models.ForeignKey(RESTAURANT, primary_key=True)
    telefono = models.CharField(max_length=50, unique=True, validators=[validate_telefono])

#Problema, clave primaria compuesta, hace falta artilugio. Seguir investigando.	
class TRANSACCION(models.Model):
    establecimiento = models.ForeignKey(RESTAURANT, null=True)
    billetera = models.ForeignKey(BILLETERA)
    tipo = models.CharField(max_length=50)
    monto = models.FloatField(validators=[validate_monto])
    fecha = models.DateField()
    class Meta:
        unique_together = ('establecimiento', 'billetera')

class PRODUCTO(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    fecha_vencimiento = models.DateField()

    def __str__(self):
        return self.nombre

#Problema, clave primaria compuesta, hace falta artilugio. Seguir investigando.	
class PLATO(models.Model):
    id = models.AutoField(primary_key=True)
    establecimiento = models.ForeignKey(RESTAURANT, null = True)
    nombre = models.CharField(max_length=50)
    precio = models.FloatField()
    path_img = models.FileField()
    descripcion = models.CharField(max_length = 500)

    class Meta:
        unique_together = ('establecimiento', 'nombre')

    def __str__(self):
        return self.nombre

#Problema, clave primaria compuesta, hace falta artilugio. Seguir investigando.	
class Inventario(models.Model):
    establecimiento = models.ForeignKey(RESTAURANT)
    producto = models.ForeignKey(PRODUCTO)
    cantidad = models.IntegerField()
    class Meta:
        unique_together = ('establecimiento', 'producto')

#Problema, clave primaria compuesta, hace falta artilugio. Seguir investigando.	
class Pedido(models.Model):
    establecimiento = models.ForeignKey(RESTAURANT)
    producto = models.ForeignKey(PRODUCTO)
    email = models.ForeignKey(PROVEEDOR)
    precio = models.FloatField()
    cantidad = models.IntegerField()
    class Meta:
        unique_together = ('establecimiento', 'producto', 'email')

#Problema, clave primaria compuesta, hace falta artilugio. Seguir investigando.
class Ofrece(models.Model):
    proveedor = models.ForeignKey(PROVEEDOR)
    producto = models.ForeignKey(PRODUCTO)
    precio = models.FloatField()
    class Meta:
        unique_together = ('proveedor', 'producto')

#Gran problema. DJANGO no soporta claves foraneas compuestas. Por lo que he leido no hay artilugio que lo resuelva.
class Ingredientes(models.Model):
    plato = models.ForeignKey(PLATO)
    producto = models.ForeignKey(PRODUCTO)
    cantidad = models.IntegerField(default = 0)
    class Meta:
        unique_together = ('plato', 'producto')


class MENU(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 100, null = False,validators=[validate_nombre])

    def __str__(self):
        return self.nombre

class Plato_en_menu(models.Model):
    plato = models.ForeignKey(PLATO)
    menu = models.ForeignKey(MENU)
    class Meta:
        unique_together = ('plato', 'menu')

    def __str__(self):
        return str(self.plato.nombre)+"-->"+str(self.menu.nombre)

class CUENTA(models.Model):
    cliente = models.ForeignKey(CLIENTE)
    total = models.FloatField(default = 0)
    pagada = models.BooleanField(default = False)

class PedidoEnCuenta(models.Model):
    plato = models.ForeignKey(PLATO)
    cantidad = models.IntegerField(default = 1)
    cuenta = models.ForeignKey(CUENTA)
    class Meta:
        unique_together = ("plato", "cuenta")
