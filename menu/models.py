from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

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
	if not 5<len(rif)<9:
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
# Create your models here.
class PERFIL(models.Model):
	id = models.AutoField(primary_key=True)
	pseudonimo = models.CharField(max_length=100, unique = True)
	foto = models.CharField(max_length=100)
	descripcion = models.CharField(max_length=100)

	def __str__(self):
		return self.pseudonimo
	
class INTERES_PERFIL(models.Model):
	perfil = models.ForeignKey(PERFIL, primary_key=True)
	interes = models.CharField(max_length=50)
	
class USUARIO(models.Model):
	email = models.EmailField(max_length=200, primary_key=True, unique = True)
	contrasenia = models.CharField(max_length=50)
	es_cliente = models.BooleanField(default = False)
	perfil = models.ForeignKey(PERFIL)

	def __str__(self):
		return self.perfil.pseudonimo
	
class BILLETERA(models.Model):
	id = models.AutoField(primary_key=True)
	PIN = models.CharField(max_length=50)
	saldo = models.FloatField()
	
class CLIENTE(models.Model):
	usuario = models.ForeignKey(USUARIO, primary_key=True)
	ci = models.CharField(max_length=50, unique=True, validators=[validate_ci])
	nombre = models.CharField(max_length=50, validators=[validate_nombre])
	apellido = models.CharField(max_length=50, validators=[validate_nombre])
	telefono = models.CharField(max_length=50, validators=[validate_telefono])
	fechaNacimiento = models.DateField(null = False)
	billetera = models.ForeignKey(BILLETERA, null = True)

	def __str__(self):
		return self.usuario.perfil.pseudonimo

class PROVEEDOR(models.Model):
	usuario = models.ForeignKey(USUARIO, primary_key=True)
	rif = models.CharField(max_length=50, unique=True,validators=[validate_rif])
	nombre = models.CharField(max_length=50,validators=[validate_nombre])

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
	establecimiento = models.ForeignKey(RESTAURANT)
	billetera = models.ForeignKey(BILLETERA)
	tipo = models.CharField(max_length=50)
	monto = models.FloatField()
	fecha = models.DateField()
	class Meta:
		unique_together = ('establecimiento', 'billetera')
	
class PRODUCTO(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=50)
	fecha_vencimiento = models.DateField()

#Problema, clave primaria compuesta, hace falta artilugio. Seguir investigando.	
class PLATO(models.Model):
	id = models.AutoField(primary_key=True)
	establecimiento = models.ForeignKey(RESTAURANT)
	nombre = models.CharField(max_length=50,validators=[validate_nombre])
	precio = models.FloatField()
	#path_img = models.FileField(max_length=500, null = True)
	#  ^-- Esto es raro pal cono
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
	email = models.ForeignKey(PROVEEDOR)
	producto = models.ForeignKey(PRODUCTO)
	precio = models.FloatField()
	class Meta:
		unique_together = ('email', 'producto')
		
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