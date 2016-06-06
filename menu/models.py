from django.db import models

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
	ci = models.CharField(max_length=50, unique=True)
	nombre = models.CharField(max_length=50)
	apellido = models.CharField(max_length=50)
	telefono = models.CharField(max_length=50)
	#fechaNacimiento = models.DateField(null = False)
	billetera = models.ForeignKey(BILLETERA, null = True)

	def __str__(self):
		return self.usuario.perfil.pseudonimo

class PROVEEDOR(models.Model):
	usuario = models.ForeignKey(USUARIO, primary_key=True)
	rif = models.CharField(max_length=50, unique=True)
	nombre = models.CharField(max_length=50)

	def __str__(self):
		return self.usuario.perfil.pseudonimo
	
class RESTAURANT(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=50)
	RIF = models.CharField(max_length=50,unique=True)
	direccion = models.CharField(max_length=50)

	def __str__(self):
		return str(self.nombre) +", "+ str(self.direccion)
	
class TELEFONOS_RESTAURANT(models.Model):
	establecimiento = models.ForeignKey(RESTAURANT, primary_key=True)
	telefono = models.CharField(max_length=50, unique=True)

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
	nombre = models.CharField(max_length=50)
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
	nombre = models.CharField(max_length = 100, null = False)

	def __str__(self):
		return self.nombre

class Plato_en_menu(models.Model):
	plato = models.ForeignKey(PLATO)
	menu = models.ForeignKey(MENU)
	class Meta:
		unique_together = ('plato', 'menu')

	def __str__(self):
		return str(self.plato.nombre)+"-->"+str(self.menu.nombre)