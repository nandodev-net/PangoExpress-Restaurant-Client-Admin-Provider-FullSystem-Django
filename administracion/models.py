from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from  django.core.validators import EmailValidator


# Dado que comparte la misma base que al aplicacion menu
# solo importo el modelo de esta aplicacion
from menu.models import *