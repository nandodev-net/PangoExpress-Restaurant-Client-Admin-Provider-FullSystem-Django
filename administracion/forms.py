from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from .models import *

class FormAgregarPlato(forms.ModelForm):
    establecimiento = forms.ModelChoiceField(RESTAURANT.objects, label="Establecimiento")

    class Meta:
        model = PLATO
        fields = ['nombre', 'precio', 'path_img', 'descripcion']

class FormAgregarIngrediente(forms.Form):
    ingrediente = forms.ModelChoiceField(PRODUCTO.objects, label='Ingrediente')
    cantidad = forms.IntegerField()

class FormSeleccionarPlato(forms.Form):
    plato = forms.ModelChoiceField(PLATO.objects, label='Seleccione un plato')

class FormAgregarMenu(forms.ModelForm):
    class Meta:
        model = MENU
        fields = ['nombre', 'activo']

class FormAgregarPlatoMenu(forms.Form):
    plato = forms.ModelChoiceField(PLATO.objects, label='Plato')

class FormAgregarProducto(forms.ModelForm):
    class Meta:
        model = PRODUCTO
        fields = ['nombre']